from django.shortcuts import render
from django.views import View


class EnterView(View):
    def get(self, request):
        return render(request,"account/enter.html")

class RegisterView(View):
    def post(self, request):
        pass


class LoginView(View):
    def post(self, request):
        pass
