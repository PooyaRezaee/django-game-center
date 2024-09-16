from django.contrib import admin
from django.utils.safestring import mark_safe
from .models import Article

@admin.register(Article)
class ArticlelAdmin(admin.ModelAdmin):
    list_display = ["title","is_draft","created_at"]
    prepopulated_fields = {
        "slug": ("title",),
    }
