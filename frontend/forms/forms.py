from django import forms

class AddCourseForm(forms.Form):
    name = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    price = forms.DecimalField(max_digits=10, decimal_places=2)
    instructor = forms.CharField(max_length=255, required=False)
    duration = forms.CharField(max_length=50, required=False)
    published_date = forms.DateField(required=False)
    course_image = forms.ImageField(required=False)  
    course_video = forms.FileField(required=False)
    is_free = forms.BooleanField(required=False)
    is_on_sale = forms.BooleanField(required=False)
    course_rating = forms.CharField(max_length=5, required=False)

