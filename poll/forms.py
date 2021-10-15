from django import forms
from django.forms import ModelForm

class PersonForm(ModelForm):
    your_name = forms.CharField(label='Your name', max_length=100)
    message = forms.CharField(widget=forms.Textarea,max_length=100)
