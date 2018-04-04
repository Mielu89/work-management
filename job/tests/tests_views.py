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
from django.shortcuts import redirect

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
        
class JobEditViewTest(JobViewsSetUp, TestCase):
    
    def test_redirect_for_user_not_login(self):
        
        resp = self.client.get(reverse('job:jobedit', kwargs={'jobNr': 0}))
        self.assertRedirects(resp, '/acc/login/?next=/job/edit/0/')

    def test_correct_termplate(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.get(reverse('job:jobedit', kwargs = {'jobNr': 0}))
        self.assertTemplateUsed(resp, 'job/job_edit.html')
        
    def test_succes_url(self):
        
        self.client.login(username = 'user1', password = '12345')
         
        resp = self.client.post(reverse('job:jobedit', kwargs={'jobNr':0}),
                                {'jobNr': 0, 
                                 'city': '0', 
                                 'street': '0',
                                 'zip': '0'
                                 })
        self.assertRedirects(resp, reverse('job:jobdetail', 
                                           kwargs={'jobNr': 0}))
        
    def test_editing_fields_for_job_model(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        resp = self.client.post(reverse('job:jobedit', kwargs={'jobNr': 0}),
                                {'jobNr': 1, 
                                 'city': '1', 
                                 'street': '1',
                                 'zip': '1'
                                 })
        job = Job.objects.all()[0]
        self.assertEquals(job.jobNr, 1)
        self.assertEquals(job.city, '1')
        self.assertEquals(job.street, '1')
        self.assertEquals(job.zip, '1')
        
    def test_edit_job_add_start_date(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        resp = self.client.post(reverse('job:jobedit', kwargs={'jobNr': 0}),
                                {'jobNr': 1, 
                                 'city': '1', 
                                 'street': '1',
                                 'zip': '1',
                                 'start':  datetime.date(2005, 7, 14)
                                 })
        job = Job.objects.all()[0]
        self.assertEquals(job.start, datetime.date(2005, 7, 14))
        
    def test_edit_job_add_start_and_finish_date(self):
        
        self.client.login(username = 'user1', password = '12345')
        
        resp = self.client.post(reverse('job:jobedit', kwargs={'jobNr': 0}),
                                {'jobNr': 1, 
                                 'city': '1', 
                                 'street': '1',
                                 'zip': '1',
                                 'start':  datetime.date(2005, 7, 14),
                                 'finish': datetime.date(2005, 7, 15)
                                 })
        job = Job.objects.all()[0]
        self.assertEquals(job.finish, datetime.date(2005, 7, 15))

class JobCreateViewTest(JobViewsSetUp, TestCase):
    
    def test_redirect_if_user_not_login(self):
        
        resp = self.client.get(reverse('job:jobnew'))
        self.assertRedirects(resp, '/acc/login/?next=/job/new/')
    
    def test_corret_template(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.get(reverse('job:jobnew'))
        
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'job/job_new.html')
        
    def test_create_new_job_object(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.post(reverse('job:jobnew'),
                                {
                                'jobNr': 1,
                                'city': 'city',
                                'street': 'street',
                                'zip': '00-000'
                                })
        job = Job.objects.filter(jobNr = 1, city = 'city', street = 'street',
                                 zip = '00-000')
        self.assertEquals(len(job), 1)
        self.assertEquals(job[0].jobNr, 1)
        
    def test_success_url_after_create_new_job_object(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.post(reverse('job:jobnew'),
                                {
                                'jobNr': 1,
                                'city': 'city',
                                'street': 'street',
                                'zip': '00-000'
                                })
        self.assertRedirects(resp, reverse('job:jobdetail', kwargs={'jobNr': 1}))

class JobDeleteViewTest(JobViewsSetUp, TestCase):
    
    def test_redirect_if_user_is_not_login(self):
        
        resp = self.client.get(reverse('job:jobdelete', kwargs = {'jobNr': 0}))
        self.assertRedirects(resp, '/acc/login/?next=/job/delete/0/')
        
    def test_correct_template(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.get(reverse('job:jobdelete', kwargs = {'jobNr': 0}))
        self.assertEquals(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'job/job_delete.html')
        
    def test_delete_get_request(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.get(reverse('job:jobdelete', kwargs = {'jobNr': 0}))
        self.assertContains(resp, 'Do you confirm delete job nr: ')
    
    def test_redirect_success_delete_object_job(self):
        
        self.client.login(username = 'user1', password = '12345')
        resp = self.client.post(reverse('job:jobdelete', kwargs = {'jobNr': 0}))
        self.assertRedirects(resp, reverse('job:joblist'), status_code=302)
        self.assertEquals(len(Job.objects.all()), 0)