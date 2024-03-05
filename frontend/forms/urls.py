from django.urls import path
from .views import AddCourseView, EditCourseView, DeleteCourseView

app_name = "forms"  # This is the namespace, needed in urls.py of it_courses

urlpatterns = [

    path('add_new_course/', AddCourseView.as_view(), name= 'add_new_course' ),
    path('<int:pk>/edit/', EditCourseView.as_view(), name= 'edit_course' ),
    path("<int:pk>/delete/", DeleteCourseView.as_view(), name= 'delete_course')
    
]