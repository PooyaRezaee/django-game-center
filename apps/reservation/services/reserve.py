import jdatetime
from django.db import models,IntegrityError
from ..models import Reserve


def reserve_device(
    device: models, user: models, string_date: str, start_at: int, end_at: int
):
    jyear = int(string_date.split("/")[0])
    jmonth = int(string_date.split("/")[1])
    jday = int(string_date.split("/")[2])
    jdate = jdatetime.date(year=jyear, month=jmonth, day=jday)
    date_reserve = jdate.togregorian()
    
    base_reserve_filter = device.reserves.filter(date_reserve=date_reserve)
    for reserve in base_reserve_filter:
        if reserve.time_start <= start_at < reserve.time_end:
            raise IntegrityError("بازه انتخابی رزرو شده است لطفا به بازه های پر دقت کنید و ساعت دیگری را وارد کنید")
    # TODO need check exacly
    return Reserve.objects.create(
        user=user,
        date_reserve=date_reserve,
        time_start=start_at,
        time_end=end_at,
        content_object=device,
    )
