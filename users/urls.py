from django.urls import path
from . import views 
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('logout/',LogoutView.as_view(), name='logout'),
    path('my_profile/',views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>',views.UserView.as_view(),name='user_detail')
]