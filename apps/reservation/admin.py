from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.core.cache import cache
from .models import PS4, PS5, PC, PCGame, PS4Game, PS5Game, Reserve


class PCGameInline(admin.TabularInline):
    model = PCGame
    extra = 1


class PS4GameInline(admin.TabularInline):
    model = PS4Game
    extra = 1


class PS5GameInline(admin.TabularInline):
    model = PS5Game
    extra = 1


class DeviceAdmin(admin.ModelAdmin):
    list_display = ("name", "status", "game_count")
    search_fields = ("name",)

    def game_count(self, instance):
        return instance.games.count()

    def save_model(self, *args, **kwargs):
        super().save_model(*args, **kwargs)
        cache.delete(self.cache_key)

    game_count.short_description = "تعداد بازی ها"


class ReserveInline(GenericTabularInline):
    model = Reserve
    ct_field = "content_type"
    ct_fk_field = "object_pk"
    fk_name = "content_object"
    extra = 1
    fields = [
        "user",
        "date_reserve",
        "time_start",
        "time_end",
        "count_controller",
    ]


@admin.register(PS4)
class PS4Admin(DeviceAdmin):
    inlines = [ReserveInline, PS4GameInline]
    cache_key = "devices-ps4"


@admin.register(PS5)
class PS5Admin(DeviceAdmin):
    inlines = [ReserveInline, PS5GameInline]
    cache_key = "devices-ps5"


@admin.register(PC)
class PCAdmin(DeviceAdmin):
    inlines = [ReserveInline, PCGameInline]
    cache_key = "devices-pc"


import jdatetime
from django.utils import timezone
from datetime import timedelta, date


class ReserveFilter(admin.SimpleListFilter):
    title = "وضعیت رزرو"
    parameter_name = "reserve_status"

    def lookups(self, request, model_admin):
        return (
            ("active", "رزرو های فعال"),
            ("expired", "رزرو های تمام شده"),
            ("today", "رزرو های امروز"),
            ("this_week", "رزرو های این هفته"),
            ("this_month", "رزرو های این ماه"),
        )

    def queryset(self, request, queryset):
        now = timezone.now().date()
        if self.value() == "active":
            return queryset.filter(date_reserve__gte=now)
        elif self.value() == "expired":
            return queryset.filter(date_reserve__lt=now)
        elif self.value() == "today":
            if (
                timezone.now().hour == 20 and timezone.now().minute >= 30
            ) or timezone.now().hour >= 21:
                return queryset.filter(date_reserve=(now + timedelta(days=1)))

            return queryset.filter(date_reserve=now)
        elif self.value() == "this_week":
            match now.weekday():
                case 0:
                    days = 4
                case 1:
                    days = 3
                case 2:
                    days = 2
                case 3:
                    days = 1
                case 4:
                    days = 0
                case 5:
                    days = 6
                case 6:
                    days = 5
            end_of_week = now + timedelta(days=days)
            return queryset.filter(date_reserve__range=(now, end_of_week))
        elif self.value() == "this_month":
            end_of_month = now + timedelta(days=30)
            return queryset.filter(date_reserve__range=(now, end_of_month))
        return queryset


class DeviceFilter(admin.SimpleListFilter):
    title = "نوع دستگاه"
    parameter_name = "device_type"

    def lookups(self, request, model_admin):
        return (
            ("pc", "کامپیوتر"),
            ("ps4", "ps4"),
            ("ps5", "ps5"),
        )

    def queryset(self, request, queryset):
        if self.value() == "pc":
            return queryset.filter(content_type__model="pc")
        elif self.value() == "ps4":
            return queryset.filter(content_type__model="ps4")
        elif self.value() == "ps5":
            return queryset.filter(content_type__model="ps5")
        return queryset


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
    search_fields = ("user__phone_number", "customer_id")
    list_filter = (ReserveFilter, "created_at", DeviceFilter)
    ordering = ("-date_reserve", "time_start", "time_end")

    def jalali_date_reserve(self, instance):
        date = instance.date_reserve
        months_fa = [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
            "مهر",
            "آبان",
            "آذر",
            "دی",
            "بهمن",
            "اسفند",
        ]
        jdate = jdatetime.date.fromgregorian(date=date)
        return f"{jdate.day} {months_fa[jdate.month - 1]}"

    def jalali_date_created(self, instance):
        datetime = instance.created_at
        if not datetime:
            return "نامشخص"

        months_fa = [
            "فروردین",
            "اردیبهشت",
            "خرداد",
            "تیر",
            "مرداد",
            "شهریور",
            "مهر",
            "آبان",
            "آذر",
            "دی",
            "بهمن",
            "اسفند",
        ]
        jdatetime_created = jdatetime.datetime.fromgregorian(datetime=datetime)
        hour = jdatetime_created.hour + 3
        minutes = jdatetime_created.minute + 30
        day = jdatetime_created.day
        month = jdatetime_created.month
        month_fa = months_fa[month - 1]
        if minutes > 60:
            minutes -= 60
            hour += 1
        if hour >= 24:
            hour -= 24
            day += 1
        return f"{day} {month_fa} - {hour}:{minutes}"

    def device(self, instance):
        return f"{instance.content_object}"

    device.short_description = "دستگاه"
    jalali_date_reserve.short_description = "تاریخ رزرو شده"
    jalali_date_created.short_description = "تاریخ ایجاد رزرو"
