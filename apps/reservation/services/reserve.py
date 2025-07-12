import jdatetime
from django.db import IntegrityError
from ..models import Reserve, Device
from apps.main.models import SiteSettings

def reserve_device(device: Device, user, string_date: str, start: int, end: int, controllers: int) -> str:
    y, m, d = map(int, string_date.split("/"))
    date_reserve = jdatetime.date(year=y, month=m, day=d).togregorian()

    for r in device.reserves.filter(date_reserve=date_reserve):
        if r.time_start <= start < r.time_end:
            raise IntegrityError("این بازه قبلاً رزرو شده است")

    reserve = Reserve.objects.create(
        user=user,
        device=device,
        date_reserve=date_reserve,
        time_start=start,
        time_end=end,
        count_controller=controllers,
    )
    return reserve.customer_id


def calculate_price(start: int, end: int, device: Device, controllers=1) -> int:
    cfg = SiteSettings.get_solo()
    hours = end - start
    if hours <= 0:
        return 0
    if device.type == "ps4":
        base = cfg.price_ps4
        extra = cfg.price_per_controoler_ps4
    elif device.type == "ps5":
        base = cfg.price_ps5
        extra = cfg.price_per_controoler_ps5
    else:
        base = cfg.price_pc
        extra = 0
    return base * hours + max(0, controllers - 1) * extra * hours
