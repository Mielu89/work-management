from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import generic

from django.contrib.auth.mixins import LoginRequiredMixin


from mysite.secret import mapKey
from . import models

# Create your views here.

EDIT_FIELDS = ['jobNr','city', 'street', 'zip', 'start', 'finish']
JOB_PARAM = 'jobNr'

class JobDetailView(LoginRequiredMixin, generic.DetailView):
    
    template_name = 'job/job_detail.html'
    model = models.Job
    context_object_name = 'jobDetail'
    
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        context.update({'key': mapKey})
        return context
    
    def get_object(self):
        object = get_object_or_404(models.Job, jobNr = self.kwargs[JOB_PARAM])
        return object

class JobListView(LoginRequiredMixin, generic.ListView):
    template_name = 'job/jobs_list.html'
    model = models.Job
    context_object_name = 'jobList'
    
    def get_queryset(self):
        return models.Job.objects.filter(finish__isnull = True, start__isnull=False)
        

class JobEditView(generic.UpdateView):
    model = models.Job
    template_name = 'job/job_edit.html'
    fields = EDIT_FIELDS
    
    def get_success_url(self):
        return reverse_lazy('job:jobdetail', kwargs={JOB_PARAM: self.kwargs[JOB_PARAM]})
    
    def get_object(self):
        try:
            object = models.Job.objects.get(jobNr = self.kwargs[JOB_PARAM])
        except:
            return redirect('/job/joblist/')
        return object
    
    def save(self):
        object = get_object_or_404(models.Job, jobNr = self.kwargs[JOB_PARAM])
        object.save(save_fields=EDIT_FIELDS)
        return object
    
class JobCreateView():
    pass

class JobDeleteView():
    pass

class JobWorkersView():
    pass