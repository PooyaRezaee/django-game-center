import jdatetime
from django.db import models


def time_reserved(device: models, string_date: str) -> list[tuple[int, int]]:
    jyear = int(string_date.split("/")[0])
    jmonth = int(string_date.split("/")[1])
    jday = int(string_date.split("/")[2])
    jdate = jdatetime.date(year=jyear, month=jmonth, day=jday)
    date_reserve = jdate.togregorian()

    reserves = device.reserves.filter(date_reserve=date_reserve)

    times = []
    for reserve in reserves.order_by("time_start"):
        times.append((reserve.time_start, reserve.time_end))

    return times
