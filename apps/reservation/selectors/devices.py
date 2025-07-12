from django.db.models import QuerySet
from ..models import Device
from django.core.cache import cache

def get_devices() -> dict[str, QuerySet]:
    devices = {}
    for dtype in ["ps4", "ps5", "pc"]:
        cache_key = f"devices-{dtype}"
        cached = cache.get(cache_key)
        if not cached:
            cached = Device.objects.filter(type=dtype, status=True).prefetch_related("games")
            cache.set(cache_key, cached, 60 * 60)
        devices[dtype] = cached

    return devices
