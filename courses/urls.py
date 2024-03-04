from django.urls import path
from .views import CourseList, CourseDetail,CourseFilteredList, CommentListCreateView, LikeListCreateView, RatingListCreateView

urlpatterns = [
    path('api/items/', CourseList.as_view(), name='course-list'),
    path('api/items/<int:pk>/', CourseDetail.as_view(), name='course-detail'),
    path('api/items/filtered/', CourseFilteredList.as_view(), name='course-list'),
    path('api/items/<int:course_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('api/items/<int:course_pk>/likes/', LikeListCreateView.as_view(), name='like-list-create'),
    path('api/items/<int:course_pk>/ratings/', RatingListCreateView.as_view(), name='rating-list-create'),
    

]
