from django.urls import path
from .views import ArticleDetailView,ArticleListView

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    path("detail/", ArticleDetailView.as_view(), name="detail"),
]
