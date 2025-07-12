import jdatetime
from ..models import Device

def time_reserved(device: Device, jalali_date: str):
    y, m, d = map(int, jalali_date.split("/"))
    g_date = jdatetime.date(year=y, month=m, day=d).togregorian()
    qs = device.reserves.filter(date_reserve=g_date)
    return [(r.time_start, r.time_end) for r in qs]
