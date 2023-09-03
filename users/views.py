from django.shortcuts import render, redirect

from home import models,forms

from .forms import  CustomUserCreationForm

from django.views.generic import CreateView, View
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from django.http import HttpResponse
from django.views.generic import ListView, CreateView,DetailView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from pymusic import settings
import smtplib
import ssl



class RegisterView(CreateView):
    template_name = "users/register.html"
    form_class = CustomUserCreationForm
    
    def form_valid(self, form: CustomUserCreationForm):
        user = form.save()
        login(self.request, user)
        return redirect("/")


class CustomLoginView(LoginView):
    template_name = "users/login.html"
    form_class = AuthenticationForm

class ProfileView(DetailView):
    template_name = 'users/profile.html'
    model = get_user_model()

    def get_context_data(self,*args,**kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Profile'
        if self.request.user.is_authenticated:
            context['user_playlists'] = models.Playlist.objects.filter(user=self.request.user)
        return context








# class SendEmail(View):
#     def get(self, request):
#         message = "Hello, world!"
#         # post_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
#         # post_server.ehlo()
#         # post_server.starttls(context=ssl.create_default_context())
#         # post_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         # post_server.sendmail(settings.EMAIL_HOST_USER, "example@gmail.com", message)
#         # post_server.quit()
#         send_mail("Mail to example@gmail.com",message,settings.EMAIL_HOST_USER,
#         ['example@gmail.com'])

#         return HttpResponse('Mesage sent')


    
    
# class SendMessageView(View):
#     def get(self, request):
#         message = "Hello, world!"
#         post_server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
#         post_server.ehlo()
#         post_server.starttls(context=ssl.create_default_context())
#         post_server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
#         post_server.sendmail(settings.EMAIL_HOST_USER, "yaku19760@gmail.com", message)
#         post_server.quit()
        
#         return HttpResponse("Повідомлення відправлено")
