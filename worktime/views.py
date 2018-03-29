from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .forms import AddHoursForm

# Create your views here.


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
            
class AddHoursView(generic.CreateView):
    
    template_name = "worktime/addhours.html"
   
    form_class = AddHoursForm
    success_url = reverse_lazy('worktime:myjobs')  
     
    def get_context_data(self, **kwargs):
        kwargs = super(AddHoursView, self).get_context_data(**kwargs)
        kwargs['jobNr'] = self.kwargs.get(JOB_PARAM)
        return kwargs
          
    def get_form_kwargs(self):
        # pass "jobNr" keyword argument from current url to your form
        kwargs = super(AddHoursView, self).get_form_kwargs()
        kwargs['jobNr'] = self.kwargs.get(JOB_PARAM)
        return kwargs
