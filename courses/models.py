from django.db import models

# Create your models here.

class Course(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.CharField(max_length=255, null=True)
    duration = models.CharField(max_length=50, null=True)
    published_date = models.DateField(null=True)
    
    

    def __str__(self):
        return self.name