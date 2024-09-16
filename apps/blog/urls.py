from django.urls import path,re_path
from .views import ArticleDetailView, ArticleListView

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="list"),
    re_path(r"(?P<slug>[-\w]+)/", ArticleDetailView.as_view(), name="detail"),
]
