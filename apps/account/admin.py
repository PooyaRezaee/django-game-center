from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    fieldsets = (
        ("اصلی", {"fields": ("full_name", "phone_number", "email")}),
        (
            "دسترسی ها",
            {"fields": ("is_active", "is_admin", "is_superuser")},
        ),
        (
            "رخداد ها",
            {"classes": ("tabular",), "fields": ("last_login", "joined_at")},
        ),
    )

    add_fieldsets = (
        (
            "Personal",
            {
                "classes": ("wide",),
                "fields": ("phone_number", "full_name", "email"),
            },
        ),
        (
            "Security",
            {
                "classes": ("wide",),
                "fields": ("password1", "password2"),
            },
        ),
        ("Special Access", {"classes": ("wide",), "fields": ("is_admin",)}),
    )

    readonly_fields = ("joined_at", "last_login", "password", "is_superuser")

    ordering = ("joined_at",)
    filter_horizontal = ("groups", "user_permissions")
    list_display = (
        "phone_number",
        "full_name",
        "is_active",
        "last_login",
        "joined_at",
    )
    search_fields = ("id", "email", "full_name", "phone_number")
    list_filter = ("last_login", "is_active", "joined_at")
    actions = ["disable_account", "enable_account"]

    @admin.action(description="Disable users")
    def disable_account(self, request, queryset):
        queryset.update(is_active=False)

    @admin.action(description="Enable users")
    def enable_account(self, request, queryset):
        queryset.update(is_active=True)


admin.site.unregister(Group)
