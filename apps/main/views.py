from django.shortcuts import render,redirect
from django.views import View
from .forms import ContactForm
from django.contrib import messages


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
    form_class = ContactForm

    def get(self, request):
        context = {
            "state":"contact",
            "form": self.form_class,
        }

        return render(request, "main/contact.html",context)

    def post(self, request):  # TODO need captcha
        form = self.form_class(request.POST)
        
        if form.is_valid():
            form.save()
            messages.success("پیام شما با موفقیت ارسال شد")
            return redirect("main:home")
        else:
            messages.warning(form.errors)
            context = {
                "state":"contact",
                "form": form,
            }
            return render(request, "main/contact.html",context)

