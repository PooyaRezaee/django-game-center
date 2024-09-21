from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from .forms import LoginForm, RegisterForm
from .models import User
from .mixins import LoginRequiredMixin, NoLoginRequiredMixin, SuperUserOnlyMixin


class EnterView(NoLoginRequiredMixin, View):
    def get(self, request):
        context = {
            "register_form": RegisterForm,
            "login_form": LoginForm,
            "state": "login",
        }

        return render(request, "account/enter.html", context)


class RegisterView(NoLoginRequiredMixin, View):
    form_class = RegisterForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                user = User.objects.create_user(
                    phone_number=data["phone_number"],
                    password=data["password"],
                    full_name=data["name"],
                )
                login(request, user)
                return redirect("main:home")
            except IntegrityError:
                messages.warning("این شماره تلفن قبلا ثبت نام شده است")
                return redirect("account:enter")
        else:
            messages.error(request, form.errors)
            return redirect("account:enter")


class LoginView(NoLoginRequiredMixin, View):
    form_class = LoginForm

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(
                request, username=data["phone_number"], password=data["password"]
            )
            if user is None:
                messages.error(request, "شماره یا رمز اشتباه میباشد")
                return redirect("account:enter")
            else:
                messages.success(request, "وارد شدید")
                login(request, user)
            return redirect("main:home")
        else:
            messages.error(request, form.errors)
            return redirect("account:enter")


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, "خارج شدید")
        return redirect("main:home")
