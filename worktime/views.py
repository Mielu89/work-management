from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import AddHoursForm, MyHoursJobEditForm

# Create your views here.

from worktime.forms import JOB_WORKER 
from job import models
from job.views import JOB_PARAM
from .models import WorkTime

class MyJobsView(LoginRequiredMixin, generic.ListView):
    template_name = "worktime/myjobs.html"
    model = models.Job
    context_object_name = 'jobList'
        
    def get_context_data(self, **kwargs):
        context = super(MyJobsView, self).get_context_data(**kwargs)
      
        context['activ'] = self.request.GET.get('sort', None)
        if context['activ'] == None:
            context['activ'] = 'current'
        return context
        
    def get_queryset(self):
        user = self.request.user

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
            query = models.Job.objects.filter(filterArg, 
                                              jobworkers__user = user)
            return query
        
        if sort:
            if sort == "all":
                return models.Job.objects.filter(jobworkers__user = user)
            elif sort == "future":
                return models.Job.objects.filter(start__isnull=True, 
                                                 jobworkers__user = user)
            elif sort == 'complited':
                return models.Job.objects.filter(finish__isnull = False, 
                                                 jobworkers__user = user)
            elif sort == 'current':
                return models.Job.objects.filter(start__isnull = False, 
                                                 finish__isnull = True,
                                                 jobworkers__user = user)
        else : 
            return models.Job.objects.filter(finish__isnull = True, 
                                            start__isnull = False,
                                            jobworkers__user = user)
            
class AddHoursView(LoginRequiredMixin, generic.CreateView):
    
    template_name = "worktime/addhours.html"
   
    form_class = AddHoursForm
    success_url = reverse_lazy('worktime:myjobs')  
     
    def get_context_data(self, **kwargs):
        kwargs = super(AddHoursView, self).get_context_data(**kwargs)
        kwargs[JOB_PARAM] = self.kwargs.get(JOB_PARAM)
        return kwargs
          
    def get_form_kwargs(self):
        # pass "jobNr" keyword argument from current url to your form
        kwargs = super(AddHoursView, self).get_form_kwargs()
        kwargs[JOB_PARAM] = self.kwargs.get(JOB_PARAM)
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit = False)
        
        # If url/jobNR take jobNr from URL, if not take from form
        try:
            jobNr = self.kwargs[JOB_PARAM]
        except KeyError:
            jobNr = form.cleaned_data[JOB_WORKER].jobNr

        job = models.Job.objects.get(jobNr = jobNr)

        jobWorker = models.JobWorker.objects.get_or_create(job = job,
                                                    user = self.request.user)
        self.object.jobWorker = jobWorker[0]
        self.object.save()
        return HttpResponseRedirect(reverse('worktime:myjobs'))

class MyHoursView(LoginRequiredMixin, generic.ListView):
    
    template_name = "worktime/my_hours.html"
    object = models.JobWorker
    context_object_name = "jobWorkers"
    
    def get_context_data(self):
        context = super().get_context_data()
        context['activ'] = self.request.GET.get('sort', None)
        
        if not context['activ']:
            context['activ'] = 'all'
        
        return context
    
    def get_queryset(self):
        user = self.request.user
        
        sort = self.request.GET.get('sort', None)
        search = self.request.GET.get('search', None)
        
        if search:
            filterArg = (Q(job__zip__iexact = search)| 
                        Q(job__street__istartswith = search)|
                        Q(job__city__istartswith = search))
            try:
                filterArg |= Q(job__jobNr__iexact = search)
            except:
                pass
            query = self.object.objects.filter(filterArg, 
                                              user = user)
            return query

        if sort:
            if sort == 'all':
                query = self.object.objects.filter(user=user)
            elif sort == 'current':
                query = self.object.objects.filter(user=user,
                                                   job__start__isnull = False,
                                                   job__finish__isnull = True)
            elif sort == 'future':
                query = self.object.objects.filter(user = user,
                                                   job__start__isnull = True)
            elif sort == 'complited':
                query = self.object.objects.filter(user = user,
                                                   job__finish__isnull = False)
            
        else:
            query = self.object.objects.filter(Q(user=user))
            
        return query

class MyHoursJobEditView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'worktime/job_hours_view.html'
    context_name_object = "jobHours"
    form_class = MyHoursJobEditForm
      
    def get_object(self, **kwargs):
        object = get_object_or_404(WorkTime,
                                   id = self.kwargs["pk"])        
        return object
    
    def get_success_url(self):
        return reverse('worktime:myhours')