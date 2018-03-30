from django import forms
from .models import JobWorker, WorkTime
from job.views import JOB_PARAM
from job.models import Job

JOB_WORKER = 'jobWorker'

class AddHoursForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):   
        #Add jobworker field to from Worktime model if any jobNr pass in url
        #When in url will be parameter. Job foreignkey will be set by automat.
        self.jobNr = kwargs.pop(JOB_PARAM, None)
        super(AddHoursForm, self).__init__(*args, **kwargs)
        if not self.jobNr:
            self.fields[JOB_WORKER] = forms.ModelChoiceField(queryset=Job.objects.all())

    class Meta:
        model = WorkTime
        fields = ['date', 'hours', 'description']
        
        widgets = {
            'date': forms.SelectDateWidget(empty_label=("Choose Year", 
                                                          "Choose Month", 
                                                          "Choose Day"))
            }
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        
        if self.jobNr:
            jobDate = Job.objects.get(jobNr=self.jobNr)
            
        elif not cleaned_data.get(JOB_WORKER).start: 
            raise forms.ValidationError("Dat work don't start yet")
                
        else:
            jobDate = cleaned_data.get(JOB_WORKER).start
              
        if date<jobDate:
            raise forms.ValidationError("Wrong date")
        
        return cleaned_data