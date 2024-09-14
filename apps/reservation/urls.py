from django.urls import path
from .views import ReserveView

app_name = "reserve"

urlpatterns = [
    path("", ReserveView.as_view(), name="index"),
]
