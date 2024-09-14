from django.urls import path
from .views import HomeView,GalleryView,ContactView

app_name = "main"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("gallery/", GalleryView.as_view(), name="gallery"),
    path("contact/", ContactView.as_view(), name="contact"),
]
