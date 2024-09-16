from django import forms
from django.forms import ValidationError
import re


class RegisterForm(forms.Form):
    name = forms.CharField(max_length=128)
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput())

    def clean_phone_number(self):
        data = self.cleaned_data["phone_number"]
        phone_pattern = re.compile(r'^09\d{9}$')
        
        if not phone_pattern.match(data):
            raise ValidationError("شماره تلفن معتبر نمی‌باشد")
        
        return data

    def clean_password(self):
        data = self.cleaned_data["password"]
        
        if len(data) < 4:
            raise ValidationError("رمز عبور کوتاه میباشد")
        
        return data


class LoginForm(forms.Form):
    phone_number = forms.CharField(max_length=11)
    password = forms.CharField(widget=forms.PasswordInput())
