from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin


from mysite.secret import mapKey
from . import models
from menu.models import Menu
from . import forms

# Create your views here.

JOB_PARAM = 'jobNr'
ADMIN_JOB_CONTEXT = 'adminJobMenu'
JOB_CONTEXT = 'JobMenu'
SORT_CONTEXT = 'active'

class MenuMixin(Menu):
    def get_context_data(self, **kwargs):
        context = super(MenuMixin, self).get_context_data(**kwargs)
        context[ADMIN_JOB_CONTEXT] = Menu.objects.get(name = ADMIN_JOB_CONTEXT)
        return context
    
class JobParamMixin(object):
    
    def get_object(self):
        object = get_object_or_404(models.Job, jobNr = self.kwargs[JOB_PARAM])
        return object
    
class JobDetailView(LoginRequiredMixin, MenuMixin, JobParamMixin, generic.DetailView):
    
    template_name = 'job/job_detail.html'
    model = models.Job
    context_object_name = 'jobDetail'
    
    def get_context_data(self, **kwargs):
        context = super(JobDetailView, self).get_context_data(**kwargs)
        
        #Pass Google Map Key to JS in template        
        context.update({'key': mapKey})
        
        menu = context[ADMIN_JOB_CONTEXT].item_set.filter(
                                            text__in=["Edit","New", "Delete"])
        context[ADMIN_JOB_CONTEXT] = menu
        
        user = self.request.user
        context['myHours'] = user.userjobs.filter(job = self.object)
        return context

class JobListView(LoginRequiredMixin, MenuMixin, generic.ListView):
    template_name = 'job/jobs_list.html'
    model = models.Job
    context_object_name = 'jobList'
    
    def get_context_data(self, **kwargs):
        context = super(JobListView, self).get_context_data(**kwargs)
        
        menu = context[ADMIN_JOB_CONTEXT].item_set.filter(text__in = ["New"])
        context[ADMIN_JOB_CONTEXT] = menu
      
        context[SORT_CONTEXT] = self.request.GET.get('sort', None)
        if context[SORT_CONTEXT] == None:
            context[SORT_CONTEXT] = 'current'
        return context
    
    def get_queryset(self, **kwargs):
        sort = self.request.GET.get('sort', None)
        search = self.request.GET.get('search', None)
       
        if search:
            
            filterArg = (Q(zip__iexact = search)| 
                        Q(street__istartswith = search)| 
                        Q(city__istartswith = search))
            try:
                filterArg |= Q(jobNr__iexact = search)
            except:
                pass
            query = models.Job.objects.filter(filterArg)
            return query
        
        if sort:
            if sort == "all":
                return models.Job.objects.all()
            elif sort == "future":
                return models.Job.objects.filter(start__isnull = True)
            elif sort == 'complited':
                return models.Job.objects.filter(finish__isnull = False)
            elif sort == 'current':
                return models.Job.objects.filter(start__isnull = False, 
                                                 finish__isnull = True)
        else : 
            return models.Job.objects.filter(finish__isnull = True, 
                                             start__isnull=False)
        
class JobEditView(LoginRequiredMixin, JobParamMixin, generic.UpdateView):
    template_name = 'job/job_edit.html'
    form_class = forms.JobForm
    context_object_name = "jobEdit"     
    
    def get_success_url(self):
        jobNr = self.request.POST.get(JOB_PARAM)
        return reverse_lazy('job:jobdetail', 
                            kwargs={JOB_PARAM: jobNr})
       
class JobCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = "job/job_new.html"
    form_class = forms.JobForm
    context_object_name = "jobNew"
    
    def get_success_url(self):
        return reverse('job:jobdetail', 
                       kwargs={JOB_PARAM: self.request.POST[JOB_PARAM]})

class JobDeleteView(LoginRequiredMixin, JobParamMixin, generic.DeleteView):
    model = models.Job
    success_url = reverse_lazy('job:joblist')
    template_name = "job/job_delete.html"
    context_object_name = "job"