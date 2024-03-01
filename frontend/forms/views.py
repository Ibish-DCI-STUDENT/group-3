from django.urls import reverse_lazy
from django.shortcuts import render, redirect
import requests
from django.http import HttpResponseServerError
from django.views.generic.edit import FormView
from django.views import View
from .forms import AddCourseForm
from decimal import Decimal

class AddCourseView(FormView):
    template_name = 'add_new_course.html'
    form_class = AddCourseForm
    success_url = reverse_lazy('frontend_courses:course_list')

    def form_valid(self, form):
        api_data = {key: str(value) if isinstance(value, Decimal) else value for key, value in form.cleaned_data.items()}
        api_files = {field: (file.name, file, file.content_type) for field in ['course_image', 'course_video'] if (file := self.request.FILES.get(field))}
        api_data.update(api_files)

        response = requests.post("http://127.0.0.1:8000/api/items/", data=api_data, files=api_files)

        if response.status_code == 201:
            return super().form_valid(form)
        else:
            print(response.status_code, response.content)
            return HttpResponseServerError('An error occurred while adding the course')
        
class EditCourseView(View):
    template_name = 'edit_course.html'
    api_url = 'http://127.0.0.1:8000/api/items/{}/'

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
            form = AddCourseForm(request.POST, request.FILES, initial=data)  
            if form.is_valid():
                
                form_data = {key: str(value) if isinstance(value, Decimal) else value for key, value in form.cleaned_data.items()}
                form_files = {field: (file.name, file, file.content_type) for field in ['course_image', 'course_video'] if (file := request.FILES.get(field))}
                form_data.update(form_files)
                
                update_response = requests.put(self.api_url.format(pk), data=form_data, files=form_files)
                if update_response.status_code == 200:
                    return redirect('frontend_courses:course_list')  
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
            print("PK value:", pk)
            response = requests.delete(self.api_url.format(pk))
            print(response.text)
            if response.status_code == 204:
                return redirect('frontend_courses:course_list')
        return HttpResponseServerError('An error occurred')
