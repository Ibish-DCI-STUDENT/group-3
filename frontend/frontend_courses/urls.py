from django.urls import path
from .views import HomeView, CourseList, DetailView

app_name = "frontend_courses"  # This is the namespace, needed in urls.py of it_courses

urlpatterns = [
    path("home/", HomeView.as_view(), name="home"),
    path("course_list/", CourseList.as_view(), name="course_list"),
    path("course_detail/<int:course_id>/", DetailView.as_view(), name="course_detail"),
    
]
