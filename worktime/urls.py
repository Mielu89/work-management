from django.urls import path
from . import views

app_name = 'worktime'

urlpatterns = [
    path('myjobs/', views.MyJobsView.as_view(), name='myjobs'),
    path('addhours/<int:jobNr>/', views.AddHoursView.as_view(), name='addhours'),
    path('addhours/', views.AddHoursView.as_view(), name='addhours'),
    path('myhours/', views.MyHoursView.as_view(), name='myhours'),
    path('my/<int:pk>/', views.MyHoursJobEditView.as_view(), name='myjobhours'),
    path('my/delete/<int:pk>/', views.MyHoursJobDeleteView.as_view(), name='deletehour')
    ]
