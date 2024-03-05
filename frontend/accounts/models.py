from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)
    purchased_courses = models.JSONField(default=list)
    address = models.CharField(null=True, blank=True, max_length=255)
    phone_number = models.CharField(null=True, blank=True, max_length=15)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    
    
