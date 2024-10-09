from django.db.models import QuerySet
from ..models import PS4,PS5,PC
from django.core.cache import cache

def get_devices() -> dict[str,QuerySet]:
    ps4 = cache.get("devices-ps4")
    if not ps4:
        ps4 = PS4.objects.filter(status=True).prefetch_related('games')
        cache.set("devices-ps4",ps4, 60*60)

    ps5 = cache.get("devices-ps5")
    if not ps5:
        ps5 = PS5.objects.filter(status=True).prefetch_related('games')
        cache.set("devices-ps5",ps5, 60*60)

    pc = cache.get("devices-pc")
    if not pc:
        pc = PC.objects.filter(status=True).prefetch_related('games')
        cache.set("devices-pc",pc, 60*60)

    return {
        "ps4": ps4,
        "ps5": ps5,
        "pc": pc,
    }
