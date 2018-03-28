from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Job(models.Model):
    
    jobNr = models.IntegerField(unique = True,)
    
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=30)
    zip = models.CharField(max_length=30)
    
    start = models.DateField(blank = True, null = True)
    finish = models.DateField(blank = True, null = True)
    staff = models.ManyToManyField(User, related_name = 'staff',
                                   through = 'JobWorker')

    def __str__(self):
        return str(self.jobNr) + ' ' + self.street

    def totalHours(self):
        return sum([h.totalHours() for h in self.jobworkers.all()])
    
    class Meta:
        ordering = ['jobNr']
    
class JobWorker(models.Model):
    job = models.ForeignKey(Job, related_name='jobworkers', 
                            on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name = 'userjobs',
                             on_delete = models.CASCADE)
    
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
            
    def totalHours(self):
        return sum([h.hours for h in self.time.all()])
    
    
    class Meta:
        unique_together = ('job', 'user')
        