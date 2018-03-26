from django.urls import path
from . import views

app_name = 'job'

urlpatterns = [
    path('<int:jobNr>/', views.JobDetailView.as_view() ,name='jobdetail'),
    path('jobs/', views.JobListView.as_view(), name='joblist'),
    path('edit/<int:jobNr>/', views.JobEditView.as_view(), name='jobedit'),
    ]