from django import forms
from .models import Job

class JobForm(forms.ModelForm):  
    class Meta:
        model = Job
        fields = ['jobNr','city', 'street', 'zip', 'start', 'finish']
        widgets = {
            "start" : forms.SelectDateWidget(empty_label=("Choose Year", 
                                                          "Choose Month", 
                                                          "Choose Day")),
            
            "finish": forms.SelectDateWidget(empty_label=("Choose Year", 
                                                          "Choose Month", 
                                                          "Choose Day")),            
            }
        labels = {
            "jobNr" : "Job number",
            "start" : "Start Not required",
            "finish" : "Finish Not required"
            }
        
    def clean_finish(self):

        finish = self.cleaned_data.get('finish')
        start = self.cleaned_data.get('start')
        if finish and not start:
            raise forms.ValidationError("Type start date before finish")  
        if finish:
            if finish < start:
                raise forms.ValidationError(
                        "Finish date can't be earlier then the start date.")
        return finish