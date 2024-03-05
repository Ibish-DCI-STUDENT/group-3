# filters/forms.py

from django import forms

class FilterForm(forms.Form):
    min_price = forms.DecimalField(required=False)
    max_price = forms.DecimalField(required=False)
    instructor = forms.CharField(required=False)
    duration = forms.CharField(required=False)