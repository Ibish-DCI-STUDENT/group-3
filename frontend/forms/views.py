from typing import Any
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseServerError
from django.views.generic.edit import FormView
from django.views import View
from .forms import AddCourseForm

class AddCourseView(FormView):
    template_name = 'add_new_course.html'
    form_class = AddCourseForm
    success_url = reverse_lazy('frontrnd_courses: course_list')

    def form_valid(self, form):
        # Prepare data from the form
        api_data = {
            'name': form.cleaned_data['name'],
            'description': form.cleaned_data['description'],
            'instructor': form.cleaned_data['instructor'],
            'price': form.cleaned_data['price'],
            'duration': form.cleaned_data['duration'],
            'published_date': form.cleaned_data['published_date'],
        }

        # Send a POST request to the API to add the data
        response = requests.post('"http://127.0.0.1:8000/api/items"', data=api_data)

        if response.status_code == 201:  # Assuming the API returns 201 for successful creation
            return super().form_valid(form)
        else:
         
            return HttpResponseServerError('An error occurred while adding the course')
        
class EditCourseView(View):
    template_name = 'edit_course.html'
    api_url = 'http://127.0.0.1:8000/api/items/{}/'  # Replace with your API URL

    def get(self, request, pk):
        # Fetch data from the API
        response = requests.get(self.api_url.format(pk))
        if response.status_code == 200:
            data = response.json()
            form = AddCourseForm(initial=data)  # Populate the form with fetched data
            return render(request, self.template_name, {'form': form})
        else:
            return redirect('error_page')

    def post(self, request, pk):

        response = requests.get(self.api_url.format(pk))
        if response.status_code == 200:
            data = response.json()
            form = AddCourseForm(request.POST, initial=data)  
            if form.is_valid():
      
                form_data = form.cleaned_data  
                update_response = requests.put(self.api_url.format(pk), data=form_data)
                if update_response.status_code == 200:
                    return redirect('course_list')  
                else:
                    return HttpResponseServerError('An error occurred')
            else:
               
                return render(request, self.template_name, {'form': form})
        else:
            return HttpResponseServerError('An error occurred')
        
class DeleteCourseView(View):
    template_name = 'delete_course.html'
    api_url = 'http://127.0.0.1:8000/api/items/{}/' 

    def get(self, request, pk):
        return render(request, self.template_name)

    def post(self, request, pk):
        # Check if the user confirmed the deletion
        if 'confirm_delete' in request.POST:
            # Send a DELETE request to the API
            response = requests.delete(self.api_url.format(pk))
            if response.status_code == 204:
                return redirect('course_list')
        return redirect('course_list')