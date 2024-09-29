from django import forms
from django.forms import ValidationError
from datetime import date
import jdatetime


class ReserveForm(forms.Form):
    date = forms.CharField()
    start_at = forms.IntegerField(min_value=8,max_value=22)
    end_at = forms.IntegerField(min_value=8,max_value=22)

    def clean_date(self):
        data = self.cleaned_data["date"]
        
        try:
            year = int(data.split("/")[0])
            month = int(data.split("/")[1])
            day = int(data.split("/")[2])
            selected_date = jdatetime.date(year=year,month=month,day=day)
            now = jdatetime.date.today()
        except Exception:
            raise ValidationError("تاریخ معتبر نمیباشد")
        
        if selected_date < now:
            raise ValidationError("تاریخ معتبر نمیباشد")
        
        return data

    def clean(self):
        cleaned_data = super().clean()
        start_at = cleaned_data.get("start_at")
        end_at = cleaned_data.get("end_at")

        if start_at is None or end_at is None:
            raise ValidationError("زمان شروع و پایان را مشخص کنید")
        if start_at >= end_at:
            raise ValidationError("ساعت شروع نباید جلوتر یا مساوی از ساعت پایان باشد")
        
        return cleaned_data