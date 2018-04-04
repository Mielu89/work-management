from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
import datetime

from menu.models import Menu, Item
from job.views import *
from job.models import Job, JobWorker
from worktime.models import WorkTime
from job.views import ADMIN_JOB_CONTEXT, JOB_PARAM
from mysite.secret import mapKey

class JobViewsSetUp():
    
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='12345') 
        self.user1.save()
        self.user2 = User.objects.create_user(username='user2', password='12345') 
        self.user2.save()
        
        self.menu = Menu.objects.create(name = ADMIN_JOB_CONTEXT)
        self.item1 = Item.objects.create(menu = self.menu,
                                         text = 'item1',
                                         views = 'item1view')
        self.item2 = Item.objects.create(menu = self.menu,
                                         text = 'item2',
                                         views = 'item2view')
        self.item3 = Item.objects.create(menu = self.menu,
                                         text = 'item3',
                                         views = 'item3view')
        
        Job.objects.create(jobNr = 0, city = '0', 
                               street = '0',
                               zip = 'a')        
        
class JobListViewTest(JobViewsSetUp, TestCase):
      
    def test_redirect_if_not_logged_in(self):
       
        resp = self.client.get(reverse('job:joblist'))
        self.assertRedirects(resp, '/acc/login/?next=/job/jobs/')
                
    def test_correct_template(self):
        
        login = self.client.login(username = 'user1', password = '12345')       
        resp = self.client.get(reverse('job:joblist'))
        
        self.assertEquals(resp.context['user'], self.user1)
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'job/jobs_list.html')
    
    def test_list_jobs_sort_all(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        #Create 9 jobs for test
        for i in range(1,10):
            Job.objects.create(jobNr = i, city = 'city%s' % i, 
                               street = 'street%s' % i,
                               zip = '00-00%s' % i)
        resp = self.client.get(reverse('job:joblist'), {'sort': 'all'})
        
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 10)
        
    def test_list_jobs_sort_current(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        #Create 10 jobs for test
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today() + datetime.timedelta(days = 1)
            else:
                date = None
            Job.objects.create(jobNr = i, city = 'city%s' % i, 
                               street = 'street%s' % i,
                               zip = '00-00%s' % i,
                               start = datetime.date.today(),
                               finish = date)
        
        resp = self.client.get(reverse('job:joblist'), {'sort': 'current'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 5)
        
    def test_list_jobs_sort_complited(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        #Create 10 jobs for test
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today() + datetime.timedelta(days = 1)
            else:
                date = None
            Job.objects.create(jobNr = i, city = 'city%s' % i, 
                               street = 'street%s' % i,
                               zip = '00-00%s' % i,
                               start = datetime.date.today(),
                               finish = date)
          
        resp = self.client.get(reverse('job:joblist'), {'sort': 'complited'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 5)
    
    def test_list_jobs_sort_future(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        #Create 10 jobs for test
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            Job.objects.create(jobNr = i, city = 'city%s' % i, 
                               street = 'street%s' % i,
                               zip = '00-00%s' % i,
                               start = date)
          
        resp = self.client.get(reverse('job:joblist'), {'sort': 'future'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 6)
        
    def test_job_list_search(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        #Create 10 jobs for test
        for i in range(1,11):
            if (i%2) == 0:
                date = datetime.date.today()
            else:
                date = None
            Job.objects.create(jobNr = i, city = 'city%s' % i, 
                               street = 'street%s' % i,
                               zip = '00-00%s' % i,
                               start = date)
            
        #searching by jobNr
        resp = self.client.get(reverse('job:joblist'), {'search': '1'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #searching by city 
        resp = self.client.get(reverse('job:joblist'), {'search': 'city2'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #searching by zip
        resp = self.client.get(reverse('job:joblist'), {'search': '00-001'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)
        
        #searching by street
        resp = self.client.get(reverse('job:joblist'), {'search': 'street2'})
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(len(resp.context['jobList']), 1)

class JobDetailViewTest(JobViewsSetUp, TestCase):
    
    def test_redirect_if_not_logged_in(self):

        resp = self.client.get(reverse('job:jobdetail', kwargs={'jobNr': 0}))
        self.assertRedirects(resp, '/acc/login/?next=/job/detail/0/')
        
    def test_correct_template(self):

        self.client.login(username = 'user1', password = '12345')
        resp = self.client.get(reverse('job:jobdetail', kwargs={'jobNr': 0}))
        self.assertEquals(resp.context['user'], self.user1)
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'job/job_detail.html')
        
    def test_passing_map_key_to_template(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        resp = self.client.get(reverse('job:jobdetail', kwargs={'jobNr': 0}))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.context['key'], mapKey)
        
    def test_user_hours_in_detail_job_view(self):
        
        self.client.login(username = 'user1', password = '12345')
        job = Job.objects.get(jobNr = 0)
        jobworker = JobWorker(job = job, user = self.user1)
        jobworker.save()
                
        resp = self.client.get(reverse('job:jobdetail', kwargs={'jobNr': 0}))
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(resp.context['myHours'][0], 
                          self.user1.userjobs.filter(job = job)[0])
        self.assertEquals(len(resp.context['myHours']), 1)
        