from django.contrib import admin
from .models import Course, Comment,Rating,Like

admin.site.register(Course)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Like)
