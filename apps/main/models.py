from django.db import models
from solo.models import SingletonModel

class Contact(models.Model):
    subject = models.CharField("موضوع",max_length=256)
    content = models.TextField("توضیحات",max_length=10240)
    phone_number = models.CharField("شماره تلفن",max_length=13, null=True, blank=True)
    created_at = models.DateTimeField("تاریخ ایجاد",auto_now_add=True)

    def __str__(self):
        return self.subject

    class Meta:
        verbose_name = "پیغام"
        verbose_name_plural = "پیغام ها"


class SiteSettings(SingletonModel):
    weblog_status = models.BooleanField("وبلاگ فعال باشد ؟", default=True)
    reserve_status = models.BooleanField("رزرو کردن دستگاه ها فعال باشد ؟", default=True)

    def __str__(self):
        return "تنظیمات سایت"

    class Meta:
        verbose_name = "نظیمات سایت"