from django.shortcuts import redirect
from django.http import HttpResponseForbidden
from django.contrib import messages


class NoLoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.warning(request, "شما قبلا لاگین کرده اید")
            return redirect("main:home")

        return super().dispatch(request, *args, **kwargs)


class LoginRequiredMixin:
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "ابتدا باید ورود کنید")
            return redirect("account:enter")
        return super().dispatch(request, *args, **kwargs)


class SuperUserOnlyMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)

        return HttpResponseForbidden()
