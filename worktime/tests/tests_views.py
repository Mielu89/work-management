from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from worktime.views import *
from job.models import *
from worktime.models import *
import datetime

class WorkTimeViewsSetUp:
        
    def setUp(self):
    
        self.user = User.objects.create_user(username = 'user1', 
                                          password = '12345')
        self.client.login(username = 'user1', password = '12345')

class MyJobsViewTest(WorkTimeViewsSetUp, TestCase):
        
    def test_redirect_when_user_not_login(self):
         
        self.client.logout()
          
        resp = self.client.get(reverse('worktime:myjobs'))
        self.assertRedirects(resp, '/acc/login/?next=/hours/myjobs/')
        
    def test_correct_template(self):
        
        resp = self.client.get(reverse('worktime:myjobs'))
        self.assertTemplateUsed(resp, 'worktime/myjobs.html')
        
    def test_query_fo_search(self):
        
        for i in range(1,5):
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                     street = 'street%s' % i,
                                     zip = '00-00%s' % i)
            JobWorker.objects.create(job = job, user = self.user)
            
        #Searching by jobNr
        resp = self.client.get(reverse('worktime:myjobs'),{'search': '1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #Searching by city
        resp = self.client.get(reverse('worktime:myjobs'),{'search': 'city1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #Searching by street
        resp = self.client.get(reverse('worktime:myjobs'),{'search': 'street1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #Searching by ZIP
        resp = self.client.get(reverse('worktime:myjobs'),{'search': '00-001'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
    def test_query_sorting_curent(self):
        
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                   street = 'street%s' % i,
                                   zip = '00-00%s' % i,
                                   start = date)
            JobWorker.objects.create(job = job, user = self.user)
          
        resp = self.client.get(reverse('worktime:myjobs'), {'sort': 'current'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 5)
    
    def test_query_sorting_complited(self):
        
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                   street = 'street%s' % i,
                                   zip = '00-00%s' % i,
                                   start = date,
                                   finish = date)
            JobWorker.objects.create(job = job, user = self.user)
          
        resp = self.client.get(reverse('worktime:myjobs'), {'sort': 'complited'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 5)     
        
    def test_query_sorting_future(self):
        
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                   street = 'street%s' % i,
                                   zip = '00-00%s' % i,
                                   start = date)
            JobWorker.objects.create(job = job, user = self.user)
    
        resp = self.client.get(reverse('worktime:myjobs'), {'sort': 'future'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 5) 
        
    def test_query_sorting_all(self):
        
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                   street = 'street%s' % i,
                                   zip = '00-00%s' % i,
                                   start = date)
            JobWorker.objects.create(job = job, user = self.user)
        
        #Sort by current jobs    
        resp = self.client.get(reverse('worktime:myjobs'), {'sort': 'all'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 10) 
            
class AddHoursViewTest(WorkTimeViewsSetUp, TestCase):
            
    def test_redirect_user_not_login(self):
        pass
            
            
            
            