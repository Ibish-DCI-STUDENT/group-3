
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, View, TemplateView, UpdateView
from .forms import CustomUserCreationForm
from django.shortcuts import render, redirect
from django.http import HttpResponseServerError
import json
import requests
from .models import CustomUser
from .forms import CustomUserChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

class PurchaseCourseView(View):
    template_name = 'purchased_course.html'
    api_url = 'http://127.0.0.1:8000/api/items/{}/' 

    def get(self, request, pk):
        return render(request, self.template_name)

    def post(self, request, pk):
        response = requests.get(self.api_url.format(pk))
        if response.status_code == 200:
            try:
                course_data = response.json()
                if course_data:
                    if request.user.is_authenticated:
                        user = request.user
                        purchased_courses = user.purchased_courses or []
                        print(purchased_courses)
                        purchased_courses.append(course_data['id'])
                        user.purchased_courses = purchased_courses
                        user.save()
                    return redirect('accounts:purchased_list') 
                else:
                    return HttpResponseServerError('The API response is empty')
            except json.JSONDecodeError as e:
                return HttpResponseServerError(f'Error decoding API response: {e}')
        else:
            return HttpResponseServerError(f'Failed to fetch course data. Status code: {response.status_code}')
        
class PurchaseCourseListView(ListView):
    model = CustomUser
    template_name = 'purchased_list.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        purchased_courses_ids = user.purchased_courses
        
        course_list = []

        if purchased_courses_ids:
            try:
                # Make a single API call to fetch details of all courses
                response = requests.get("http://127.0.0.1:8000/api/items/")
                if response.status_code == 200:
                    all_courses = response.json()
                    for course in all_courses:
                        if course['id'] in purchased_courses_ids:
                            course_info = {'id': course['id'], 'name': course['name']}
                            course_list.append(course_info)
                else:
                    print(f"Failed to fetch course details. Status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error fetching course details: {e}")

        context['course_list'] = course_list
        return context
    
class LearnPageView(TemplateView):
    template_name = "learn_page.html"
    
    def get_context_data(self, **kwargs):
        course_id = kwargs['pk']
        
        
        url_home_page = reverse("frontend_courses:home")
        url_course_list = reverse("frontend_courses:course_list")
        response = requests.get("http://127.0.0.1:8000/api/items")
        data = response.json()
        
        for course in data:
            if course["id"] == course_id:
                course_info = course
                break  
        
        context = {
            "url_home_page": url_home_page, 
            "url_course_list": url_course_list, 
            "course": course_info,
        }
        return context
    

class EditProfileView(View):
    template_name = 'edit_course.html'
    
    def get(self, request):
        user = request.user
        form = CustomUserChangeForm(instance=user)
        context = {'form': form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = request.user
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('frontend_courses:home')  
        else:
            context = {'form': form}
            return render(request, self.template_name, context)


class ProfileView(ListView):
    model = CustomUser
    template_name = "my_profile.html"
    context_object_name = "profile"

    def get_queryset(self):
        return CustomUser.objects.filter(pk=self.request.user.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = context['object_list'].first()  
        context['profile'] = profile
        return context
