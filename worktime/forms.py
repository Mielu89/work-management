from django import forms
from .models import JobWorker, WorkTime
from django.shortcuts import get_object_or_404


class AddHoursForm(forms.ModelForm):

    model = WorkTime
    
   
                                                