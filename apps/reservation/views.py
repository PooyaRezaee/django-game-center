from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from apps.account.mixins import LoginRequiredMixin
from django.contrib import messages
from django.db import IntegrityError
from .selectors.devices import get_devices
from .services.reserve import reserve_device
from .selectors.reserve import time_reserved
from .forms import ReserveForm
from .models import PC, PS4, PS5


class ListReserveView(View):
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

    def get(self, request, device_pk):
        device = get_object_or_404(self.model, pk=device_pk)
        context = {
            "form": self.form_class,
            "device": device,
        }

        return self.render(request, context)

    def post(self, request, device_pk):
        form = self.form_class(data=request.POST)
        device = get_object_or_404(self.model, pk=device_pk)
        context = {
            "form": form,
            "device": device,
        }
        if form.is_valid():
            cd = form.cleaned_data
            string_date = cd["date"]
            start_at = cd["start_at"]
            end_at = cd["end_at"]
            try:
                reserve_device(device, request.user, string_date, start_at, end_at)
                messages.success(request, "با موفقیت رزرو انجام شد")
                # return redirect("main:home") TODO back
                return self.render(request, context)
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
