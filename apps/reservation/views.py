from django.shortcuts import render
from django.views import View


class ReserveView(View):
    def get(self, request):
        context = {
            "state":"reserve",
        }

        return render(request,"reservation/index.html",context)

    def post(self, request):
        context = {
            "state":"reserve",
        }

        return render(request,"reservation/index.html",context)

