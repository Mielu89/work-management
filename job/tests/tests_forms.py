import datetime
from django import forms
from job.forms import JobForm
from django.test import TestCase
from django.utils import timezone

class JobFormsTest(TestCase):
    
    def test_JobForm_fields_labels(self):
        form = JobForm()
        self.assertEquals(form.fields['jobNr'].label, 'Job number')
        self.assertEquals(form.fields['city'].label, 'City')
        self.assertEquals(form.fields['street'].label, 'Street')
        self.assertEquals(form.fields['zip'].label, 'Zip')
        self.assertEquals(form.fields['start'].label, 'Start Not required')
        self.assertEquals(form.fields['finish'].label, 'Finish Not required')
        
    def test_JobForm_fields_widgets(self):
        form = JobForm()
        self.assertEquals(type(form.fields['start'].widget), 
                          forms.SelectDateWidget
                          )
        self.assertEquals(type(form.fields['finish'].widget), 
                          forms.SelectDateWidget
                          )
        
    def test_JobForm_finish_date_and_no_start_date(self):
        date = timezone.now()
        form_data = {'finish': date, 'city': 'city', 'street': 'street', 
                     'jobNr': 1, 'zip': '00-001'
                    }
        form = JobForm(data = form_data)
        self.assertFalse(form.is_valid())
         
    def test_JobForm_finish_date_before_start_date(self):
        start_date = timezone.now() + datetime.timedelta(days=1)
        finish_date = timezone.now() 
        form_data = {'start': start_date, 'finish': finish_date, 
                     'city': 'city', 'street': 'street', 'jobNr': 1,
                     'zip': '00-001'
                    }
        form = JobForm(data = form_data)
        self.assertFalse(form.is_valid())
        
    def test_JobForm_correct_start_and_finish_date(self):
        start_date = datetime.date.today()
        finish_date = datetime.date.today() + datetime.timedelta(days=1)
        form_data = {'start': start_date, 'finish': finish_date,
                     'city': 'city', 'street': 'street', 'jobNr': 1,
                     'zip': '00-001'
                     }
        form = JobForm(data = form_data)
        self.assertTrue(form.is_valid())