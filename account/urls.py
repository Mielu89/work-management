from django.urls import path
from . import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView

app_name = 'account'

urlpatterns = [
    path('registration/', views.SignUpView.as_view(), name='signup'),
    path('login/', 
         views.UserLoginView.as_view(), name='login'),
    path('logout/', 
         LogoutView.as_view(), name='logout'),
    ]