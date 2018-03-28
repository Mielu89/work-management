from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('detail/<int:jobNr>/', views.JobDetailView.as_view() ,name='jobdetail'),
    path('jobs/', views.JobListView.as_view(), name='joblist'),
    path('edit/<int:jobNr>/', views.JobEditView.as_view(), name='jobedit'),
    path('new/', views.JobCreateView.as_view(), name="jobnew"),
    path('delete/<int:jobNr>/', views.JobDeleteView.as_view(), name="jobdelete")
    ]