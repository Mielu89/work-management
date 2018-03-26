from django.contrib import admin
from . import models

# Register your models here.

class JobWorkerInline(admin.TabularInline):
    model = models.JobWorker

admin.site.register(models.Job)