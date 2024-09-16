from django.shortcuts import render
from django.views import View
from .selectors.devices import get_devices

class ReserveView(View):
    def get(self, request):
        context = {
            "state":"reserve",
            **get_devices(),
        }

        return render(request,"reservation/index.html",context)

    def post(self, request):
        context = {
            "state":"reserve",
        }

        return render(request,"reservation/index.html",context)

