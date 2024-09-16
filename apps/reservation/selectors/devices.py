from django.db.models import QuerySet
from ..models import PS4,PS5,PC

def get_devices() -> dict[str,QuerySet]:
    return {
        "ps4": PS4.objects.filter(status=True),
        "ps5": PS5.objects.filter(status=True),
        "pc": PC.objects.filter(status=True),
    }
