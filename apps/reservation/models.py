from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


class PS4(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PS4"
        verbose_name_plural = "PS4s"

    def __str__(self):
        return self.name


class PS5(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PS5"
        verbose_name_plural = "PS5s"

    def __str__(self):
        return self.name


class PC(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PC"
        verbose_name_plural = "PCs"

    def __str__(self):
        return self.name


class Game(models.Model):
    name = models.CharField("نام", max_length=256)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PS4Game(Game):
    device = models.ForeignKey(
        PS4, on_delete=models.CASCADE, related_name="games",verbose_name="دستگاه"
    )


class PS5Game(Game):
    device = models.ForeignKey(
        PS5, on_delete=models.CASCADE, related_name="games",verbose_name="دستگاه"
    )


class PCGame(Game):
    device = models.ForeignKey(
        PC, on_delete=models.CASCADE, related_name="games",verbose_name="دستگاه"
    )
