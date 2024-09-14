from django.shortcuts import render
from django.views import View


class ArticleListView(View):
    def get(self, request):
        context = {
            "state":"weblog",
        }

        return render(request,"blog/list.html",context)


class ArticleDetailView(View):
    def get(self, request):
        context = {
            "state":"weblog",
        }

        return render(request,"blog/detail.html",context)