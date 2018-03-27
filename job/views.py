from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin


from mysite.secret import mapKey
from . import models
from menu.models import Menu
from . import forms

# Create your views here.

EDIT_FIELDS = ['jobNr','city', 'street', 'zip', 'start', 'finish']
JOB_PARAM = 'jobNr'
ADMIN_JOB_CONTEXT = 'adminJobMenu'
JOB_CONTEXT = "JobMenu"

class MenuMixin(Menu):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context[ADMIN_JOB_CONTEXT] = Menu.objects.get(name = ADMIN_JOB_CONTEXT)
        return context
    
 
class JobDetailView(LoginRequiredMixin, MenuMixin, generic.DetailView):
    
    template_name = 'job/job_detail.html'
    model = models.Job
    context_object_name = 'jobDetail'
    
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        
        #Pass Google Map Key to JS in template        
        context.update({'key': mapKey})
        
        context[ADMIN_JOB_CONTEXT] = context[ADMIN_JOB_CONTEXT].item_set.filter(text__in = ["Edit","New", "Delete"])
        
        return context
    
    def get_object(self):
        object = get_object_or_404(models.Job, jobNr = self.kwargs[JOB_PARAM])
        return object

class JobListView(LoginRequiredMixin, MenuMixin, generic.ListView):
    template_name = 'job/jobs_list.html'
    model = models.Job
    context_object_name = 'jobList'
    
    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        context[ADMIN_JOB_CONTEXT] = context[ADMIN_JOB_CONTEXT].item_set.filter(text__in = ["New"])
        
        return context
    
    def get_queryset(self, **kwargs):
        sort = self.request.GET.get('sort', None)
        print(sort)
        if sort:
            if sort == "all":
                return models.Job.objects.all()
            elif sort == "future":
                return models.Job.objects.filter(start__isnull = True)
            elif sort == 'complited':
                return models.Job.objects.filter(finish__isnull = False)
            elif sort == 'current':
                return models.Job.objects.filter(start__isnull = False, finish__isnull = True)
        else: 
            return models.Job.objects.filter(finish__isnull = True, start__isnull=False)

class JobEditView(generic.UpdateView):
    template_name = 'job/job_edit.html'
    form_class = forms.JobForm
    context_object_name = "jobEdit"
    
    def get_success_url(self):
        return reverse_lazy('job:jobdetail', kwargs={JOB_PARAM: self.kwargs[JOB_PARAM]})
    
    def get_object(self):
        object = get_object_or_404(models.Job, jobNr = self.kwargs[JOB_PARAM])     
        return object
    
    
class JobCreateView(generic.CreateView):
    template_name = "job/job_new.html"
    form_class = forms.JobForm
    context_object_name = "jobNew"
    
    def get_success_url(self):
        return reverse('job:jobdetail', kwargs={JOB_PARAM: self.request.POST["jobNr"]})


class JobDeleteView():
    pass

class JobWorkersView():
    pass