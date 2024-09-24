from django.urls import path
from .views import ListReserveView, PCReserveView, PS4ReserveView, PS5ReserveView

app_name = "reserve"

urlpatterns = [
    path("", ListReserveView.as_view(), name="index"),
    path("pc/<int:device_pk>/", PCReserveView.as_view(), name="pc"),
    path("ps4/<int:device_pk>/", PS4ReserveView.as_view(), name="ps4"),
    path("ps5/<int:device_pk>/", PS5ReserveView.as_view(), name="ps5"),
]
