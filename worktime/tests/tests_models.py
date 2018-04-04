from django.test import TestCase
from django.contrib.auth.models import User

from worktime.models import WorkTime
from job.models import Job, JobWorker

import datetime
from django.core.exceptions import ObjectDoesNotExist

class WorkTimeTest(TestCase):
    
    def setUp(self):
        
        user = User.objects.create_user(username = 'user', 
                                         password = '12345')
        
        job = Job.objects.create(jobNr = 1, city = 'city1', 
                                  street = 'street1', zip = '00-001')
        
        self.jobworker = JobWorker.objects.create(user = user, job = job)
        
        self.worktime = WorkTime.objects.create(jobWorker = self.jobworker,
                                                hours = 30,
                                                date = datetime.date.today(),
                                                description = 'description')
        
    def test_fields_name_labels(self):
        
        wt = self.worktime
        
        jobworker_label = wt._meta.get_field('jobWorker').verbose_name
        date_label = wt._meta.get_field('date').verbose_name
        description_label = wt._meta.get_field('description').verbose_name
        hours_label = wt._meta.get_field('hours').verbose_name
        
        self.assertEquals(jobworker_label, 'jobWorker')
        self.assertEquals(date_label, 'date')
        self.assertEquals(description_label, 'description')
        self.assertEquals(hours_label, 'hours')
        
    def test_object_name(self):
        
        expected = str(self.worktime)
        self.assertEquals(str(self.worktime), expected)
        
    def test_max_length_fields(self):
        
        description_max = \
            self.worktime._meta.get_field('description').max_length
        self.assertEquals(description_max, 100)
        
    def test_foreign_key(self):
        
        fk = self.worktime.jobWorker
        self.assertEquals(type(fk), JobWorker)
        
    def test_is_default_hours_zero(self):
        
        wt = WorkTime.objects.create(jobWorker = self.jobworker,
                                     date = datetime.date.today(),
                                     description = 'description')
        self.assertEquals(wt.hours, 0)
        
    def test_ordering_objects(self):
        
        for i in range(1,4):
            WorkTime.objects.create(jobWorker = self.jobworker,
                 date = datetime.date.today() + datetime.timedelta(days = i),
                 description = 'description')
        query = WorkTime.objects.all()
        self.assertTrue(query[0].date < query[1].date)
        self.assertTrue(query[1].date < query[2].date)
        self.assertTrue(query[2].date < query[3].date)
    
    def test_delete_foreignkey_if_not_related_Worktime_objects(self):
        
        jw = JobWorker.objects.get(pk = 1)

        for work in jw.time.all():
            work.delete()
        
        query = JobWorker.objects.all()
        self.assertTrue(list(query) == [])            