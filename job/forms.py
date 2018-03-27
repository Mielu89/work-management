from django import forms
from .models import Job
from django.contrib.admin.widgets import AdminDateWidget

class JobForm(forms.ModelForm):  
    class Meta:
        model = Job
        fields = ['jobNr','city', 'street', 'zip', 'start', 'finish']
        widgets = {
            "start" : forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),
            "finish": forms.SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day")),            
            }
        labels = {
            "start" : "Start Not required",
            "finish" : "Finish Not required"
            }