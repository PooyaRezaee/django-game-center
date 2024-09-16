from django.urls import path
from .views import EnterView, LoginView, RegisterView,LogoutView

app_name = "account"

urlpatterns = [
    path("sign/", EnterView.as_view(), name="enter"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
]
