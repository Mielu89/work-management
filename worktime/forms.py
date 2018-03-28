from django import forms
from .models import JobWorker, WorkTime
from job.views import JOB_PARAM
from job.models import Job
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404

class AddHoursForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        #Add jobworker field from Worktime model if any jobNr pass in url
        self.jobNr = kwargs.pop('jobNr', None)
        super(AddHoursForm, self).__init__(*args, **kwargs)
        if not self.jobNr:
            self.fields['jobWorker'] = forms.ModelChoiceField(queryset=Job.objects.all())

    class Meta:
        model = WorkTime
        fields = ['date', 'hours', 'description']