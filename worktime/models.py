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
    
    def delete(self, using=None):

        if self.jobWorker.time.all().count() == 1:
            self.jobWorker.delete()
        super(WorkTime, self).delete(using)
        
    class Meta:
        ordering = ['date']