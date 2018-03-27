from django.db import models

# Create your models here.

class Menu(models.Model):
    
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    text = models.CharField(max_length=20)
    views = models.CharField(max_length=20)
    
    
    def __str__(self):
        return self.text
    