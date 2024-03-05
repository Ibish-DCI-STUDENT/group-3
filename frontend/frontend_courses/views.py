from typing import Any
from django.views.generic import TemplateView
from django.urls import reverse
import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseBadRequest,HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from accounts.models import CustomUser


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


class DetailView(View):
    template_name = "course_details.html"

    def get(self, request, course_id):
        url_home_page = reverse("frontend_courses:home")
        url_course_list = reverse("frontend_courses:course_list")
        response = requests.get("http://127.0.0.1:8000/api/items")
        data = response.json()

        course_info = None
        for course in data:
            if course["id"] == course_id:
                course_info = course
                break  # Exit the loop once the course is found

        if course_info is None:
            return HttpResponseNotFound("Course not found")  # Handle the case when the course is not found

        stars_range = range(1, 6)

        context = {
            "url_home_page": url_home_page,
            "url_course_list": url_course_list,
            "course": course_info,
            "stars_range": stars_range,
            "comments": "Comments will be displayed here",
            "ratings": "Ratings will be displayed here",
        }
        return render(request, self.template_name, context)


    def post(self, request, course_id):
        if request.user.is_authenticated:
            # Access form data
            comment_text = request.POST.get('comments')
            rating_value = request.POST.get('ratings')

            # Use the currently logged-in user
            comment_user = request.user
            rating_user = request.user

            # Save comments and ratings to the API
            api_url_comment = f"http://127.0.0.1:8000/api/items/{course_id}/comments/"
            api_data_comment = {'user': comment_user.pk, 'course': course_id, 'text': comment_text}
            requests.post(api_url_comment, data=api_data_comment)

            # Save ratings to the API
            api_url_rating = f"http://127.0.0.1:8000/api/items/{course_id}/ratings/"
            api_data_rating = {'user': rating_user.pk, 'course': course_id, 'value': rating_value}
            requests.post(api_url_rating, data=api_data_rating)

            api_url_rating = f"http://127.0.0.1:8000/api/items/{course_id}/ratings/"
            api_data_rating = {'user': rating_user.pk, 'course': course_id, 'value': rating_value}
            requests.post(api_url_rating, data=api_data_rating)

            # Redirect to avoid resubmission
            return redirect('frontend_courses:course_detail', course_id=course_id)
        else:
            # Handle the case when the user is not authenticated
            return HttpResponseForbidden("You must be logged in to perform this action.")
