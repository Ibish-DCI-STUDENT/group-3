# yourscript.py

import os
import django
import requests
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Comment, Course
from django.core.management import setup

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "it_courses.settings")
setup()

# Assuming there is a Course with ID=1
course = get_object_or_404(Course, pk=1)

# Create a new user or use an existing one
user = User.objects.first()  

# If there are no users in the database, create a new one
if user is None:
    user = User.objects.create_user(username='testuser', password='testpassword')
    
# Hardcoded comment data
comment_data = {
    'user': user.pk,
    'course': course.pk,
    'text': 'This is a hardcoded comment for the API.'
}

# API endpoint URL
api_url = "http://127.0.0.1:8000/api/items/1/comments/"  # Replace with your actual API endpoint

# Send a POST request to create the comment
response = requests.post(api_url, data=comment_data)

# Check the response
if response.status_code == 201:  # HTTP status code 201 indicates successful creation
    print("Comment successfully created through the API.")
else:
    print(f"Failed to create comment. Status code: {response.status_code}, Response content: {response.text}")
