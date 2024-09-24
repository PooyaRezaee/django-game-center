from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Contact, SiteSettings


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


admin.site.register(SiteSettings, SingletonModelAdmin)
