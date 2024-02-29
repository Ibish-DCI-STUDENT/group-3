from django.urls import path
from .views import CourseList, CourseDetail,CourseFilteredList

urlpatterns = [
    path('api/items/', CourseList.as_view(), name='course-list'),
    path('api/items/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('api/items/filtered/', CourseFilteredList.as_view(), name='course-list'),
    

]
