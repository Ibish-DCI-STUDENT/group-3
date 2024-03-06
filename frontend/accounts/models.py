from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.urls import reverse


class CustomUser(AbstractUser):
    name = models.CharField(null=True, blank=True, max_length=100)
    purchased_courses = models.JSONField(default=list)
    address = models.CharField(null=True, blank=True, max_length=255)
    phone_number = models.CharField(null=True, blank=True, max_length=15)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return self.comment

class Rate(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    course = models.IntegerField()
    rating = models.IntegerField()

    def __str__(self) :
        return self.rating
