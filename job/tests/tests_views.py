from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from job.views import *

# class JobListViewTest(TestCase):
#      
#     def setUp(self):
#         test_user1 = User.objects.create_user(username='testuser1', password='12345') 
#         test_user1.save()
#         self.factory = RequestFactory()
#      
#     def test_redirect_if_not_logged_in(self):
#         resp = self.client.get(reverse('job:joblist'))
#         self.assertRedirects(resp, '/acc/login/?next=/job/jobs/')
#      
#     def test_no_jobs(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         login = self.client.login(username='testuser1', password='12345')
#         reponse = self.factory.get(reverse('job:joblist'))
#         self.assertEqual(reponse.status_code, 200)
#         self.assertContains(reponse, "No jobs available.")
#         self.assertQuerysetEqual(reponse.context['jobList'], [])

