# filters/views.py
from django.shortcuts import render
import requests
from .forms import FilterForm

def filter_view(request):
    form = FilterForm(request.GET)
    items = []

    if form.is_valid():
        params = {}
        for field_name, value in form.cleaned_data.items():
            if value:
                params[field_name] = value

        if params:  # Only make the API request if there are parameters
            response = requests.get('http://127.0.0.1:8000/api/items/filtered/', params=params)

            if response.status_code == 200:
                items = response.json()

    return render(request, 'filter.html', {'form': form, 'items': items})
