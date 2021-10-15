from django import forms
from django.forms import ModelForm
from . models import *
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import UserCreationForm


class ContactForm(ModelForm):
    topic = forms.ChoiceField(choices=TOPIC_CHOICES)
    message = forms.CharField(widget=forms.Textarea(attrs={"placeholder": "message", "rows": 4, "cols": 35}))
    sender = forms.EmailField(required=False)
    class Meta:
        model = Contact
        fields = "__all__"



