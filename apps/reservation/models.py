from django.db import models
import random


class Device(models.Model):
    DEVICE_TYPES = (
        ("ps4", "PS4"),
        ("ps5", "PS5"),
        ("pc", "PC"),
    )

    name = models.CharField("نام دستگاه", max_length=128)
    type = models.CharField("نوع دستگاه", choices=DEVICE_TYPES, max_length=4, db_index=True)
    status = models.BooleanField("آیا دستگاه فعال است؟", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ بروزرسانی", auto_now=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.name}"
    
    class Meta:
        verbose_name = "دستگاه"
        verbose_name_plural = "دستگاه ها"


class Game(models.Model):
    name = models.CharField("نام بازی", max_length=256)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="games", verbose_name="دستگاه")
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    def __str__(self):
        return self.name


class Reserve(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="reserves", verbose_name="دستگاه")
    date_reserve = models.DateField("تاریخ رزرو")
    time_start = models.PositiveIntegerField("ساعت شروع")
    time_end = models.PositiveIntegerField("ساعت پایان")
    count_controller = models.PositiveIntegerField("تعداد دسته", default=1)
    customer_id = models.CharField("کد رهگیری", max_length=32, unique=True, blank=True, null=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.customer_id:
            self.customer_id = f"{random.randint(10,99)}{self.id or '0'}{random.randint(10,99)}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.device} - {self.date_reserve} ({self.time_start}-{self.time_end})"

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزروها"
