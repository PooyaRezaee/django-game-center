from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views import View
from .selectors.articles import get_articles, get_article
from apps.main.models import SiteSettings


class ArticleListView(View):
    def dispatch(self, request, *args, **kwargs):
        config = SiteSettings.get_solo()
        if config.weblog_status:
            return super().dispatch(request, *args, **kwargs)
        else:
            return HttpResponseNotFound()
    
    def get(self, request):
        context = {
            "state": "weblog",
            "articles": get_articles(),
        }

        return render(request, "blog/list.html", context)


class ArticleDetailView(View):
    def get(self, request, slug):
        context = {
            "state": "weblog",
            "article": get_article(slug, request.user.is_superuser),
        }

        return render(request, "blog/detail.html", context)
