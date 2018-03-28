from django.db import models

from job.models import JobWorker

# Create your models here.


class WorkTime(models.Model):
    
    jobWorker = models.ForeignKey(JobWorker, on_delete=models.CASCADE,
                                  related_name='time')
    date = models.DateField()
    description = models.CharField(max_length=100)
    hours = models.IntegerField(default = 0)
            
    def __str__(self):
        return str(self.hours)
    
    class Meta:
        ordering = ['date']