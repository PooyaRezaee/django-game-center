from django.shortcuts import render
from django.views import View
from .selectors.articles import get_articles, get_article


class ArticleListView(View):
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
