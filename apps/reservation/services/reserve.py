import jdatetime
from django.db import models, IntegrityError
from ..models import Reserve, PC, PS4, PS5
from apps.main.models import SiteSettings


def reserve_device(
    device: models,
    user: models,
    string_date: str,
    start_at: int,
    end_at: int,
    count_controller: int,
) -> int:
    jyear = int(string_date.split("/")[0])
    jmonth = int(string_date.split("/")[1])
    jday = int(string_date.split("/")[2])
    jdate = jdatetime.date(year=jyear, month=jmonth, day=jday)
    date_reserve = jdate.togregorian()

    base_reserve_filter = device.reserves.filter(date_reserve=date_reserve)
    for reserve in base_reserve_filter:
        if reserve.time_start <= start_at < reserve.time_end:
            raise IntegrityError(
                "بازه انتخابی رزرو شده است لطفا به بازه های پر دقت کنید و ساعت دیگری را وارد کنید"
            )

    reserve = Reserve.objects.create(
        user=user,
        date_reserve=date_reserve,
        time_start=start_at,
        time_end=end_at,
        content_object=device,
        count_controller=count_controller,
    )
    return reserve.customer_id


def calculate_price(
    start_at: int, end_at: int, device: PS4 | PS5 | PC, count_controller=1
):
    config = SiteSettings.get_solo()
    total = 0
    hour = end_at - start_at

    if hour < 0:
        return 0

    if isinstance(device, PS4):
        total += config.price_ps4 * hour
        print(count_controller)
        total += (count_controller - 1) * config.price_per_controoler_ps4 * hour
    elif isinstance(device, PS5):
        total += config.price_ps5 * hour
        print(count_controller)
        total += (count_controller - 1) * config.price_per_controoler_ps5 * hour
    elif isinstance(device, PC):
        total += config.price_pc * hour
    else:
        return None

    return total
