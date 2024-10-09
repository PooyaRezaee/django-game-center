from typing import Any
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.account.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from apps.main.models import SiteSettings
from .selectors.devices import get_devices
from .services.reserve import reserve_device, calculate_price
from .selectors.reserve import time_reserved
from .forms import ReserveForm
from .models import PC, PS4, PS5


class ListReserveView(View):
    def dispatch(self, request, *args, **kwargs):
        config = SiteSettings.get_solo()
        if not config.reserve_status:
            messages.warning(request, "در حال حاضر رزرو از طریق سایت غیرفعال میباشد")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        context = {
            "state": "reserve",
            **get_devices(),
        }

        return render(request, "reservation/index.html", context)

    def post(self, request):
        context = {
            "state": "reserve",
        }

        return render(request, "reservation/index.html", context)


class ReserveView(View):
    form_class = ReserveForm
    model = None

    def dispatch(self, request, *args, **kwargs):
        if self.config.reserve_status:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.warning(request, "در حال حاضر رزرو از طریق سایت غیرفعال میشود")
            return redirect("main:home")
    
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.config = SiteSettings.get_solo()

        if self.model is PC:
            self.count_controller = False
            self.device_price = self.config.price_pc
            self.controller_price = 0
        else:
            if self.model is PS4:
                self.device_price = self.config.price_ps4
                self.controller_price = self.config.price_per_controoler_ps4
            elif self.model is PS5:
                self.controller_price = self.config.price_per_controoler_ps5
                self.device_price = self.config.price_ps5
            
            self.count_controller = True


        return super().setup(request, *args, **kwargs)

    def get(self, request, device_pk):
        device = get_object_or_404(self.model, pk=device_pk)

        context = {
            "form": self.form_class,
            "device": device,
            "count_controller": self.count_controller,
            "controller_price": self.controller_price,
            "device_price": self.device_price,
        }

        return self.render(request, context)

    def post(self, request, device_pk):
        form = self.form_class(data=request.POST)
        device = get_object_or_404(self.model, pk=device_pk)

        context = {
            "form": form,
            "device": device,
            "count_controller": self.count_controller,
            "controller_price": self.controller_price,
            "device_price": self.device_price,
        }
        if form.is_valid():
            cd = form.cleaned_data
            string_date = cd["date"]
            start_at = cd["start_at"]
            end_at = cd["end_at"]

            if self.model is PC:
                count_controller = 1
            else:
                count_controller = cd["count_controller"]

            try:
                customer_id = reserve_device(
                    device,
                    request.user,
                    string_date,
                    start_at,
                    end_at,
                    count_controller,
                )
                messages.success(request, "با موفقیت رزرو انجام شد")
                return render(
                    request,
                    "reservation/factor.html",
                    {
                        "device": device,
                        "count_controller": (
                            False if self.model is PC else count_controller
                        ),
                        "date": string_date,
                        "start": start_at,
                        "end": end_at,
                        "customer_id": customer_id,
                        "price": calculate_price(
                            start_at, end_at, device, count_controller
                        ),
                    },
                )
            except IntegrityError as e:
                times = time_reserved(device, string_date)
                context["string_date"] = string_date
                context["times"] = times
                messages.error(request, str(e))
                return self.render(request, context)
        else:
            error_data = form.errors.as_data()
            for key, values in error_data.items():
                for value in values:
                    messages.error(request, value.message)
            return self.render(request, context)

    def render(self, request, context):
        return render(request, "reservation/reserve.html", context)


class PCReserveView(LoginRequiredMixin, ReserveView):
    model = PC


class PS4ReserveView(LoginRequiredMixin, ReserveView):
    model = PS4


class PS5ReserveView(LoginRequiredMixin, ReserveView):
    model = PS5
