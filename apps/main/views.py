from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self, request):
        context = {
            "state":"home",
        }

        return render(request, "main/home.html",context)


class GalleryView(View):
    def get(self, request):
        context = {
            "state":"gallery",
        }

        return render(request, "main/gallery.html",context)


class ContactView(View):
    def get(self, request):
        context = {
            "state":"contact",
        }

        return render(request, "main/contact.html",context)

    def post(self, request):  # TODO need captcha
        context = {
            "state":"contact",
        }

        return render(request, "main/contact.html",context)
