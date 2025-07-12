from django.contrib import admin
from django.core.cache import cache
import jdatetime
from .models import Device, Game, Reserve


class GameInline(admin.TabularInline):
    model = Game
    extra = 1


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "type", "status", "game_count")
    search_fields = ("name",)
    inlines = [GameInline]

    def game_count(self, obj):
        return obj.games.count()

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        cache.delete(f"devices-{obj.type}")


class ReserveFilter(admin.SimpleListFilter):
    title = "وضعیت رزرو"
    parameter_name = "reserve_status"

    def lookups(self, request, model_admin):
        return (
            ("active", "فعال"),
            ("expired", "تمام شده"),
            ("today", "امروز"),
        )

    def queryset(self, request, qs):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now().date()
        if self.value() == "active":
            return qs.filter(date_reserve__gte=now)
        if self.value() == "expired":
            return qs.filter(date_reserve__lt=now)
        if self.value() == "today":
            return qs.filter(date_reserve=now)
        return qs


@admin.register(Reserve)
class ReserveAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "device",
        "jalali_date_reserve",
        "time_start",
        "time_end",
        "count_controller",
        "customer_id",
        "jalali_date_created",
    )
    list_filter = (ReserveFilter, "device__type", "created_at")
    search_fields = ("user__phone_number", "customer_id")
    ordering = ("-date_reserve", "time_start")

    def jalali_date_reserve(self, obj):
        return jdatetime.date.fromgregorian(date=obj.date_reserve).strftime("%d %B")

    def jalali_date_created(self, obj):
        return jdatetime.datetime.fromgregorian(datetime=obj.created_at).strftime("%d %B - %H:%M")
