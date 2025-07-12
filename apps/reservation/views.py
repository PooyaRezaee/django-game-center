from typing import Any
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.db import IntegrityError
from apps.account.mixins import LoginRequiredMixin
from apps.main.models import SiteSettings
from .forms import ReserveForm
from .services.reserve import reserve_device, calculate_price
from .selectors.devices import get_devices
from .selectors.reserve import time_reserved
from .models import Device


class ListReserveView(View):
    def dispatch(self, request, *args, **kwargs):
        if not SiteSettings.get_solo().reserve_status:
            messages.warning(request, "رزرو آنلاین غیرفعال است")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, "reservation/index.html", {"state": "reserve","config": SiteSettings.get_solo(),  **get_devices()})


class BaseReserveView(LoginRequiredMixin, View):
    form_class = ReserveForm
    device_type = None

    def setup(self, request, *args, **kwargs):
        self.config = SiteSettings.get_solo()
        self.device_price, self.controller_price = {
            "pc":  (self.config.price_pc, 0),
            "ps4": (self.config.price_ps4, self.config.price_per_controoler_ps4),
            "ps5": (self.config.price_ps5, self.config.price_per_controoler_ps5),
        }[self.device_type]
        self.count_controller_needed = self.device_type != "pc"
        return super().setup(request, *args, **kwargs)

    def get_device(self, pk):
        return get_object_or_404(Device, pk=pk, type=self.device_type)

    def render(self, request, ctx):
        return render(request, "reservation/reserve.html", ctx)

    def get(self, request, device_pk):
        device = self.get_device(device_pk)
        ctx = {
            "form": self.form_class,
            "device": device,
            "count_controller": self.count_controller_needed,
            "controller_price": self.controller_price,
            "device_price": self.device_price,
        }
        return self.render(request, ctx)

    def post(self, request, device_pk):
        form = self.form_class(data=request.POST)
        device = self.get_device(device_pk)
        ctx = {
            "form": form,
            "device": device,
            "count_controller": self.count_controller_needed,
            "controller_price": self.controller_price,
            "device_price": self.device_price,
        }
        if form.is_valid():
            cd = form.cleaned_data
            controllers = cd.get("count_controller") or 1
            try:
                cid = reserve_device(
                    device,
                    request.user,
                    cd["date"],
                    cd["start_at"],
                    cd["end_at"],
                    controllers,
                )
                messages.success(request, "رزرو با موفقیت ثبت شد")
                return render(
                    request,
                    "reservation/factor.html",
                    {
                        "device": device,
                        "count_controller": (False if self.device_type == "pc" else controllers),
                        "date": cd["date"],
                        "start": cd["start_at"],
                        "end": cd["end_at"],
                        "customer_id": cid,
                        "price": calculate_price(cd["start_at"], cd["end_at"], device, controllers),
                    },
                )
            except IntegrityError as e:
                ctx |= {
                    "string_date": cd["date"],
                    "times": time_reserved(device, cd["date"]),
                }
                messages.error(request, str(e))
        else:
            for errs in form.errors.values():
                for err in errs:
                    messages.error(request, err)
        return self.render(request, ctx)


class PCReserveView(BaseReserveView):
    device_type = "pc"


class PS4ReserveView(BaseReserveView):
    device_type = "ps4"


class PS5ReserveView(BaseReserveView):
    device_type = "ps5"
