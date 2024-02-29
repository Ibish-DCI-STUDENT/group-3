from django.db import models

# Create your models here.

class Course(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    instructor = models.CharField(max_length=255, null=True)
    duration = models.CharField(max_length=50, null=True)
    published_date = models.DateField(null=True)
    course_image = models.ImageField(upload_to='course_images/', blank=True, null=True)
    course_video = models.FileField(upload_to='course_videos/',blank=True, null=True)
    is_free = models.BooleanField(default=False)
    is_on_sale = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    course_rating = models.CharField(max_length=5, blank=True, null=True)
    
    def __str__(self):
        return self.name