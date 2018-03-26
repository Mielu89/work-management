from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from django.shortcuts import render
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from .forms import SignUpForm
# Create your views here.



@login_required
def index(request):     
    return render(request, 'index.html', {})

    
class UserLoginView(LoginView):
    template_name='account/login.html'
    model = User
    
class SignUpView(CreateView):
    
    form_class = SignUpForm
    template_name="account/signup.html"
    success_url = reverse_lazy('account:login')