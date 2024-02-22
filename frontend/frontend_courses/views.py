from typing import Any
from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponse
from django.shortcuts import render
import json
import requests


class HomeView(TemplateView):
    template_name = "home.html"
    # def get_context_data(self);
    #     context = {}

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
        # course_data = models.Course.objects.get(name=course_name)
        context = {"url_home_page": url_home_page, "url_course_list": url_course_list, "course": course_info}
        return context


# class UserInfo(TemplateView):
#     template_name="user_info.html"
    
#     def get_context_data(self,user_fname):
#         url_user_list= reverse("users:users_list")
#         url_home_page= reverse("users:home_page")
#         user_data=models.Users.objects.get(first_name=user_fname)
#         context={"url_home_page":url_home_page, "url_user_list":url_user_list, "user_data":user_data, "data":"classbased" }
#         return context