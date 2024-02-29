from typing import Any
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests
from django.shortcuts import get_object_or_404


class HomeView(TemplateView):
    template_name = "home.html"
    
class VideoTemplate(TemplateView):
    template_name = "video_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["url_home_page"] = reverse("frontend_courses:home")
        context["url_course_list"] = reverse("frontend_courses:course_list")

        course_id = kwargs.get('video_id')  # Assuming the parameter is named video_id
        
        try:
            # Update the API URL to include the course_id
            response = requests.get(f"http://127.0.0.1:8000/api/items/{course_id}/")
            response.raise_for_status()
            data = response.json()
            
            # Assuming the API response is a single course
            context["course"] = data if data else None
        except requests.RequestException as e:
            # Log the error or handle it appropriately
            print(f"Error fetching course information: {e}")
            
            context["course"] = None
            
        context["stars_range"] = range(1, 6)
        
        return context
    
class CourseList(TemplateView):
    template_name = "course_list.html"
    

    def get_context_data(self, **kwargs):
        url_home_page = reverse("frontend_courses:home")
        response = requests.get("http://127.0.0.1:8000/api/items")
        data = response.json()
        course_list = []
        for course in data:
            course_info = {'id': course['id'], 'name': course['name']} 
            course_list.append(course_info)
        context = {"url_home_page": url_home_page, "course_list": course_list}
        return context


class DetailView(TemplateView):
    template_name = "course_details.html"

    def get_context_data(self, course_id):
        url_home_page = reverse("frontend_courses:home")
        url_course_list = reverse("frontend_courses:course_list")
        response = requests.get("http://127.0.0.1:8000/api/items")
        data = response.json()
        for course in data:
            if course["id"]==course_id:
                course_info=course
            else:
                pass
            
        stars_range = range(1, 6)  # Add this line
                    
        # course_data = models.Course.objects.get(name=course_name)
        context = {"url_home_page": url_home_page, "url_course_list": url_course_list, "course": course_info,"stars_range": stars_range,}
        return context


# class UserInfo(TemplateView):
#     template_name="user_info.html"
    
#     def get_context_data(self,user_fname):
#         url_user_list= reverse("users:users_list")
#         url_home_page= reverse("users:home_page")
#         user_data=models.Users.objects.get(first_name=user_fname)
#         context={"url_home_page":url_home_page, "url_user_list":url_user_list, "user_data":user_data, "data":"classbased" }
#         return context