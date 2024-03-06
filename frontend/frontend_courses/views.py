from typing import Any
from django.views.generic import TemplateView
from django.urls import reverse
import requests
from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseRedirect,HttpResponseNotFound
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from accounts.models import CustomUser, Comment, Rate
from accounts.forms import CommentForm
from django.db.models import Avg


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

        comment_form = CommentForm()
        comments = Comment.objects.filter(course=course_id)

        average_rating = Rate.objects.filter(course=course_id).aggregate(avg_rating=Avg('rating'))['avg_rating']

        user_has_rated = Rate.objects.filter(course=course_id, user=self.request.user).exists()
        total_ratings = Rate.objects.filter(course=course_id).count()

        if average_rating is not None:
            average_rating = round(average_rating, 1)
        else:
            average_rating = 0.0

        context = {
            "url_home_page": url_home_page,
            "url_course_list": url_course_list,
            "course": course_info,
            "stars_range": stars_range,
            "comments": comments,
            "average_rating": average_rating,
            'user_has_rated': user_has_rated,
            "form": comment_form,
            "total_ratings": total_ratings,

        }
        return render(request, self.template_name, context)


    def post(self, request, *args, **kwargs):

        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.user = request.user
                comment.course = kwargs['course_id']
                comment.save()
                return HttpResponseRedirect(reverse("accounts:learn_page", kwargs={"pk": kwargs['course_id']}))
        else:

            return super().post(request, *args, **kwargs)