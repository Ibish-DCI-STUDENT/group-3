from django.urls import path
from .views import (
    SignUpView,
    PurchaseCourseView,
    PurchaseCourseListView,
    LearnPageView,
    EditProfileView,
    ProfileView
)

app_name = 'accounts'

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path('purchased_list/', PurchaseCourseListView.as_view(), name ='purchased_list' ),
    path('purchase/<int:pk>/', PurchaseCourseView.as_view(), name="complete_order"),
    path('learn_page/<int:pk>/', LearnPageView.as_view(), name="learn_page"),
    path('edit_profile/', EditProfileView.as_view(), name='edit_profile'),
    path('my_profile/', ProfileView.as_view(), name='my_profile'),

]