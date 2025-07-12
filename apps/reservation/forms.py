from django import forms
from django.forms import ValidationError
import jdatetime

class ReserveForm(forms.Form):
    date = forms.CharField()
    start_at = forms.IntegerField(min_value=8, max_value=22)
    end_at   = forms.IntegerField(min_value=8, max_value=22)
    count_controller = forms.IntegerField(min_value=1, max_value=8, required=False)

    def clean_date(self):
        data = self.cleaned_data["date"]
        try:
            y, m, d = map(int, data.split("/"))
            selected = jdatetime.date(year=y, month=m, day=d)
            now = jdatetime.date.today()
        except Exception:
            raise ValidationError("تاریخ معتبر نیست")
        if selected < now:
            raise ValidationError("تاریخ گذشته است")
        return data

    def clean(self):
        cd = super().clean()
        s = cd.get("start_at")
        e = cd.get("end_at")
        if s is None or e is None:
            raise ValidationError("ساعت شروع و پایان الزامی است")
        if s >= e:
            raise ValidationError("ساعت شروع باید کمتر از ساعت پایان باشد")
        return cd
