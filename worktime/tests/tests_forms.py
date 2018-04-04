from django.test import TestCase
from django import forms
from django.urls import reverse
from django.contrib.auth.models import User

import datetime

from worktime.forms import AddHoursForm, MyHoursJobEditForm
from worktime.models import WorkTime
from job.models import JobWorker, Job


class AddHoursFormTest(TestCase):
    
    def test_forms_labels(self):
        
        form = AddHoursForm()
        self.assertEquals(form.fields['date'].label, 'Date')
        self.assertEquals(form.fields['hours'].label, 'Hours')
        self.assertEquals(form.fields['description'].label, 'Description')
        
    def test_date_field_widget_is_SelectDateWidget(self):
        
        form = AddHoursForm()
        self.assertEquals(type(form.fields['date'].widget), 
                          forms.SelectDateWidget)
        
    def test_form_model_is_WorkTime(self):
        
        form = AddHoursForm()
        self.assertEquals(form._meta.model, WorkTime)
        
    def test_get_jobNr_from_url(self):
        
        User.objects.create_user(username = 'user', password = '12345')
        self.client.login(username = 'user', password = '12345')
        
        # Pass jobNr from view to form and check if form.jobNr is view object
        resp = self.client.get(reverse('worktime:addhours', 
                                        kwargs = {'jobNr': 1}))
        form = resp.context['form']
        self.assertEquals(form.jobNr, 1)
    
    def test_create_field_jobworker_if_not_jobNr_in_url(self):
        
        User.objects.create_user(username = 'user', password = '12345')
        self.client.login(username = 'user', password = '12345')
        
        # Pass jobNr from view to form and check if form.jobNr is view object
        resp = self.client.get(reverse('worktime:addhours'))
        form = resp.context['form']
        self.assertEquals(type(form.fields['jobWorker']), 
                          forms.ModelChoiceField)
        
#     def test_no_jobNr_in_url_and_no_date(self):
#         
#         job = Job.objects.create(jobNr = 1, street = 'a', city = 'a',
#                                 zip = 'a')
#         user = User.objects.create(username = 'user', password = '12345')
#         jw = JobWorker.objects.create(user = user, job = job)
# 
#         form_data = {'description': 'description', 'hours': 20}
#         form = AddHoursForm(form_data)
#         # Override field jobWorker after __init__ form
#         form.fields['jobWorker'] = job
#         
# 
#         self.assertFalse(form.is_valid())
        
        