from django.urls import path
from .views import EnterView

app_name = "account"

urlpatterns = [
    path("sign/", EnterView.as_view(), name="enter"),
]
