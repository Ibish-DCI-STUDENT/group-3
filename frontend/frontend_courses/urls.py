from django.urls import path
from .views import HomeView, CourseList, DetailView, VideoTemplate

app_name = "frontend_courses"  # This is the namespace, needed in urls.py of it_courses

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("course_list/", CourseList.as_view(), name="course_list"),
    path("course_detail/<int:course_id>/", DetailView.as_view(), name="course_detail"),
    path('video_template/<int:video_id>/', VideoTemplate.as_view(), name='video_template'),



]
