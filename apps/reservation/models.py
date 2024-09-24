from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class Reserve(models.Model):
    user = models.ForeignKey("account.User", on_delete=models.SET_NULL, null=True)
    date_reserve = models.DateField("تاریخ رزرو")
    time_start = models.PositiveIntegerField("ساعت شروع")
    time_end = models.PositiveIntegerField("ساعت پایان")
    created_at = models.DateTimeField("تاریخ ایجاد رزرو", auto_now_add=True)

    content_type = models.ForeignKey(
        ContentType,
        verbose_name="content type",
        related_name="content_type_set_for_%(class)s",
        on_delete=models.CASCADE,
    )
    object_pk = models.CharField("object ID", db_index=True, max_length=64)
    content_object = GenericForeignKey(ct_field="content_type", fk_field="object_pk")

    def __str__(self):
        return f"{self.date_reserve} - {self.time_start}-{self.time_end}"

    class Meta:
        verbose_name = "رزرو"
        verbose_name_plural = "رزرو ها"


class PS4(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    reserves = GenericRelation(
        Reserve, related_name="ps4_reserves", object_id_field="object_pk"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PS4"
        verbose_name_plural = "PS4s"

    def __str__(self):
        return f"PS4 {self.name}"


class PS5(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    reserves = GenericRelation(
        Reserve, related_name="ps5_reserves", object_id_field="object_pk"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PS5"
        verbose_name_plural = "PS5s"

    def __str__(self):
        return f"PS5 {self.name}"


class PC(models.Model):
    name = models.CharField("نام", max_length=128)
    status = models.BooleanField("آيا دستگاه فعال است؟", default=True)
    reserves = GenericRelation(
        Reserve, related_name="pc_reserves", object_id_field="object_pk"
    )
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت", auto_now=True)

    class Meta:
        verbose_name = "PC"
        verbose_name_plural = "PCs"

    def __str__(self):
        return f"PC {self.name}"


class Game(models.Model):
    name = models.CharField("نام", max_length=256)
    created_at = models.DateTimeField("تاریخ ایجاد", auto_now_add=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class PS4Game(Game):
    device = models.ForeignKey(
        PS4, on_delete=models.CASCADE, related_name="games", verbose_name="دستگاه"
    )


class PS5Game(Game):
    device = models.ForeignKey(
        PS5, on_delete=models.CASCADE, related_name="games", verbose_name="دستگاه"
    )


class PCGame(Game):
    device = models.ForeignKey(
        PC, on_delete=models.CASCADE, related_name="games", verbose_name="دستگاه"
    )
