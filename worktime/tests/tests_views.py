from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from worktime.views import *
from job.models import *
from worktime.models import *
import datetime

def createJobAndJobWorkersObjects(user):
    
    job = Job.objects.create(jobNr = 1, city = 'city', 
                                     street = 'street%',
                                     zip = '00-000',
                                     start = datetime.date.today())
    jobworker = JobWorker.objects.create(user = user, job = job)
    return job, jobworker
    
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
        self.assertEquals(resp.status_code, 200)
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
        
        self.client.logout()
          
        resp = self.client.get(reverse('worktime:addhours'))
        self.assertRedirects(resp, '/acc/login/?next=/hours/addhours/')
        
        resp = self.client.get(reverse('worktime:addhours', 
                                       kwargs = {'jobNr': 1}))
        self.assertRedirects(resp, '/acc/login/?next=/hours/addhours/1/')
    
    def test_correct_template(self):
        
        resp = self.client.get(reverse('worktime:addhours'))
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'worktime/addhours.html')
    
    def test_create_worktime_object_without_param_in_url(self):
        
        job, jobworkers = createJobAndJobWorkersObjects(self.user)
        
        resp =self.client.post(reverse('worktime:addhours'), 
                                       {'description': 'description',
                                       'date': datetime.date.today(),
                                       'hours': 20,
                                       'jobWorker': job.pk})
        query = WorkTime.objects.all()
        self.assertEquals(len(query), 1)
        self.assertEquals(query[0].hours, 20)
        
    def test_create_worktime_object_with_param_in_url(self):
        
        createJobAndJobWorkersObjects(self.user)
        
        resp =self.client.post(reverse('worktime:addhours', 
                                       kwargs ={'jobNr': 1}), 
                                       {'description': 'description',
                                       'date': datetime.date.today(),
                                       'hours': 10})
        query = WorkTime.objects.all()
        self.assertEquals(len(query), 1)
        self.assertEquals(query[0].hours, 10)
    
    def test_pass_kwargs_jobNr_to_class_form(self):
        
        createJobAndJobWorkersObjects(self.user)
        
        resp =self.client.post(reverse('worktime:addhours', 
                                       kwargs ={'jobNr': 1}),
                                       {'date': datetime.date.today()})

        self.assertEquals(resp.context['form'].jobNr, 1)
        
    def test_redirect_after_save_object(self):
        
        createJobAndJobWorkersObjects(self.user)
        
        resp =self.client.post(reverse('worktime:addhours', 
                                       kwargs ={'jobNr': 1}), 
                                       {'description': 'description',
                                       'date': datetime.date.today(),
                                       'hours': 10})
        self.assertRedirects(resp, reverse('worktime:myjobs'))
        
class MyHoursViewTest(WorkTimeViewsSetUp, TestCase):
    
    def test_redirect_when_user_not_login(self):
         
        self.client.logout()
          
        resp = self.client.get(reverse('worktime:myhours'))
        self.assertRedirects(resp, '/acc/login/?next=/hours/myhours/')
        
    def test_correct_template(self):
        
        resp = self.client.get(reverse('worktime:myhours'))
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'worktime/my_hours.html')
        
    def test_query_fo_search(self):
        
        for i in range(1,5):
            job = Job.objects.create(jobNr = i, city = 'city%s' % i, 
                                     street = 'street%s' % i,
                                     zip = '00-00%s' % i)
            JobWorker.objects.create(job = job, user = self.user)
            
        #Searching by jobNr
        resp = self.client.get(reverse('worktime:myhours'),{'search': '1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 1)
        
        #Searching by city
        resp = self.client.get(reverse('worktime:myhours'),{'search': 'city1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 1)
        
        #Searching by street
        resp = self.client.get(reverse('worktime:myhours'),{'search': 'street1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 1)
        
        #Searching by ZIP
        resp = self.client.get(reverse('worktime:myhours'),{'search': '00-001'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 1)
        
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
          
        resp = self.client.get(reverse('worktime:myhours'), {'sort': 'current'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 5)
    
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
          
        resp = self.client.get(reverse('worktime:myhours'), {'sort': 'complited'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 5)     
        
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
    
        resp = self.client.get(reverse('worktime:myhours'), {'sort': 'future'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 5) 
        
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
        resp = self.client.get(reverse('worktime:myhours'), {'sort': 'all'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobWorker']), 10) 