from django.contrib import admin
from .models import PS4, PS5, PC, PCGame, PS4Game, PS5Game


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

    game_count.short_description = "تعداد بازی ها"


@admin.register(PS4)
class PS4Admin(DeviceAdmin):
    inlines = [PS4GameInline]


@admin.register(PS5)
class PS5Admin(DeviceAdmin):
    inlines = [PS5GameInline]


@admin.register(PC)
class PCAdmin(DeviceAdmin):
    inlines = [PCGameInline]


# class GameAdmin(admin.ModelAdmin):
#     list_display = ("name", "device")
#     search_fields = ("name",)

#     def device(self, instance):
#         return f"{instance.content_type.name} | {instance.content_object.name}"

#     device.short_description = "دستگاه"
