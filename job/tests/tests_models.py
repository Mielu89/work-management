from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.utils import IntegrityError

# Create your tests here.

from job.models import Job, JobWorker
from worktime.models import WorkTime

def createWorkTimeObjects(job, user):
    jobworker = JobWorker.objects.create(job = job, user=user)
    wt1 = WorkTime.objects.create(jobWorker = jobworker, date = timezone.now(),
                            description = 'test', hours = 30)
    wt2 = WorkTime.objects.create(jobWorker = jobworker, date = timezone.now(),
                            description = 'test', hours = 10)
    return wt1, wt2

class JobModelTest(TestCase):

    @classmethod
    def setUpTestData(self):
        Job.objects.create(jobNr = 1, city = 'city1', street = 'street1',
                           zip = '00-001')
        Job.objects.create(jobNr = 22, city = 'city2', street = 'street2',
                           zip = '00-002')
        Job.objects.create(jobNr = 33, city = 'city3', street = 'street3',
                           zip = '00-003')
        User.objects.create_user(username='testuser1', password='12345')
        User.objects.create_user(username='testuser2', password='12345')
    
    def test_fields_name_label(self):
        job = Job.objects.get(pk = 1)
        jobNr_label = job._meta.get_field('jobNr').verbose_name
        city_label = job._meta.get_field('city').verbose_name
        street_label = job._meta.get_field('street').verbose_name
        zip_label = job._meta.get_field('zip').verbose_name
        start_label = job._meta.get_field('start').verbose_name
        finish_label = job._meta.get_field('finish').verbose_name
        staff_label = job._meta.get_field('staff').verbose_name
        
        self.assertEquals(jobNr_label, 'jobNr')
        self.assertEquals(city_label, 'city')
        self.assertEquals(street_label, 'street')
        self.assertEquals(zip_label, 'zip')
        self.assertEquals(start_label, 'start')
        self.assertEquals(finish_label, 'finish')
        self.assertEquals(staff_label, 'staff')
    
    def test_fields_max_length(self):
        job = Job.objects.get(id = 1)
        city_max_length = job._meta.get_field('city').max_length
        street_max_length = job._meta.get_field('street').max_length
        zip_max_length = job._meta.get_field('zip').max_length
        self.assertEquals(city_max_length, 30)
        self.assertEquals(street_max_length, 30)
        self.assertEquals(zip_max_length, 30)
        
    def test_start_finish_fields_is_null(self):
        job = Job.objects.get(pk = 1)
        self.assertEquals(job.start, None)
        self.assertEquals(job.finish, None)
        
    def test_start_finish_fields_not_blank(self):
        job = Job.objects.create(jobNr = 10, city = 'city', street = 'street',
                                 start = timezone.now(),
                                 finish = timezone.now())
        self.assertEquals(type(job.start), type(timezone.now()))
        self.assertEquals(type(job.finish), type(timezone.now()))
        
    def test_object_name_is_jobNr_space_street(self):
        job = Job.objects.get(pk = 1)
        expected_object_name = '%s %s' % (job.jobNr, job.street)
        self.assertEquals(expected_object_name, str(job))
        
    def test_no_totalHours_when_no_JobWorker(self):
        job = Job.objects.get(pk = 1)
        self.assertEquals(job.totalHours(), 0)
    
    def test_totalHours_when_no_hours(self):
        job = Job.objects.get(pk = 1)
        user = User.objects.get(pk = 1)
        jobworker = JobWorker.objects.create(job = job, user=user)
        self.assertEquals(job.totalHours(), 0)
        
    def test_totalHours_when_WorkTime_more_then_0_when_one_user(self):
        job = Job.objects.get(pk = 1)
        user = User.objects.get(pk = 1)
        worktime1, worktime2 = createWorkTimeObjects(job, user)
        expected_totalHours = worktime1.hours + worktime2.hours
        self.assertEquals(job.totalHours(), expected_totalHours)
        
    def test_totalHours_when_Worktime_more_then_0_and_more_users(self):
        job = Job.objects.get(pk = 1)
        user1 = User.objects.get(pk = 1)
        user2 = User.objects.get(pk = 2)
        worktime1u1, worktime2u1 = createWorkTimeObjects(job, user1)
        worktime1u2, worktime2u2 = createWorkTimeObjects(job, user2)
        expected_totalHours = sum([worktime1u1.hours,worktime2u1.hours,
                                   worktime1u2.hours,worktime2u2.hours])
        self.assertEquals(job.totalHours(), expected_totalHours)
    
    def test_ordering_by_jobNr(self):      
        job1 = Job.objects.get(pk = 1)
        job2 = Job.objects.get(pk = 2)
        job3 = Job.objects.get(pk = 3)
        query = Job.objects.all()
        self.assertEquals(query[0], job1)
        self.assertEquals(query[1], job2)
        self.assertEquals(query[2], job3)
    
    def test_unique_jobNr(self):
        with self.assertRaises(IntegrityError):
            Job.objects.create(jobNr = 1)
    
class JobModelM2MTest(TestCase):
    
    def setUp(self):
        self.job1 = Job.objects.create(jobNr = 1, city = 'city1', 
                                  street = 'street1', zip = "00-001")
        self.job2 = Job.objects.create(jobNr = 2, city = 'city2', 
                                  street = 'street2', zip = "00-002")
        self.job3 = Job.objects.create(jobNr = 3, city = 'city3', 
                                  street = 'street3', zip = "00-003")
        
        self.user1 = User.objects.create_user(username = 'user1',
                                              password='12345',
                                              first_name = 'f_user1',
                                              last_name = 'l_user1')    
        self.user2 = User.objects.create_user(username = 'user2', 
                                              password='12345',
                                              first_name = 'f_user2',
                                              last_name = 'l_user2')
        self.user3 = User.objects.create_user(username = 'user3', 
                                              password='12345',
                                              first_name = 'f_user3',
                                              last_name = 'l_user3')
        
        JobWorker.objects.create(job = self.job1, user = self.user1)
        JobWorker.objects.create(job = self.job1, user = self.user2)
        JobWorker.objects.create(job = self.job1, user = self.user3)
        
        JobWorker.objects.create(job = self.job2, user = self.user1)
        JobWorker.objects.create(job = self.job2, user = self.user2)
        JobWorker.objects.create(job = self.job2, user = self.user3)
        
        JobWorker.objects.create(job = self.job3, user = self.user1)
        JobWorker.objects.create(job = self.job3, user = self.user2)
        JobWorker.objects.create(job = self.job3, user = self.user3)
        
    def test_user_staff_unfiltered(self):
        job1_staff = User.objects.filter(staff = self.job1)
        self.assertEquals(list(job1_staff), [self.user1, 
                                             self.user2, self.user3])
    
    def test_unique_togheter_job_user(self):
        with self.assertRaises(IntegrityError):
            JobWorker.objects.create(job = self.job1, user = self.user1)
    
    def test_object_name_is_userFirstName_space_userLastName(self):
        jobWorker = JobWorker.objects.get(pk = 1)
        expecting_name = '%s %s job numer: %s' % (jobWorker.user.first_name,
                                                  jobWorker.user.last_name,
                                                  jobWorker.job.jobNr)
        self.assertEquals(expecting_name, str(jobWorker))
    
    def test_jobworkers_orderind(self):
        query = JobWorker.objects.all()
        self.assertTrue(query[0].job.jobNr <= query[1].job.jobNr, str(query))
        self.assertTrue(query[2].job.jobNr <= query[3].job.jobNr, str(query))
        self.assertTrue(query[3].job.jobNr <= query[4].job.jobNr, str(query))
        self.assertTrue(query[4].job.jobNr <= query[5].job.jobNr, str(query))
        self.assertTrue(query[5].job.jobNr <= query[6].job.jobNr, str(query))       