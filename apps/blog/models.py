from django.db import models
from django.urls import reverse
from django_ckeditor_5.fields import CKEditor5Field
from django.db.models.signals import post_delete
from django.dispatch import receiver


class Article(models.Model):
    title = models.CharField("عنوان",max_length=128)
    thumbnail = models.ImageField("تصویر",upload_to="article")
    content = CKEditor5Field("محتوا")
    slug = models.SlugField("اسلاگ",unique=True,allow_unicode=True)
    is_draft = models.BooleanField("پیش نویس است ؟",default=False)

    created_at = models.DateTimeField("تاریخ ایجاد",auto_now_add=True)
    updated_at = models.DateTimeField("تاریخ اپدیت",auto_now=True)

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


@receiver(post_delete, sender=Article)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.thumbnail and instance.thumbnail.name:
        instance.thumbnail.delete(save=False)
