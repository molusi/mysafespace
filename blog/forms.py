from django import forms
from .models import *
from django.forms import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django.contrib.auth.models import Permission, User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from accounts.models import User
from django.utils import timezone
user = get_user_model()

CATEGORY_CHOICES = (
    ('f','food'),
    ('ft','fitness'),
    ('s','sports'),
    ('c','cars'),
    ('t','travel'),
    ('h','health')
)


class ArticleForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'title','class':'px-2'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":12,"cols":60,'class':'px-2','placeholder':'content'}))



    class Meta:
        model = Article
        fields = ['title','content','category','image','author']


class ArticleModelForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'px-2'}))
    category = forms.ChoiceField(choices=CATEGORY_CHOICES)

    class Meta:
        model = Article
        exclude = ['author']





class UserProfileForm(forms.Form):
    preffered_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'preffered name','class':'px-2'}),max_length=255)
    about = forms.CharField(widget=forms.Textarea(attrs={"rows":3,"cols":25,"placeholder":"About you..","class":"px-2"}),max_length=400)
    class Meta:
        model = Userprofile
        fields = ['preffered_name','profilepic','about','user','twitter','instagram']

class UserProfileUpdateForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={"rows":3,"cols":25,"placeholder":"About you..","class":"px-2"}),max_length=400)
    class Meta:
        model = Userprofile
        fields = ['preffered_name','profilepic', 'about','twitter','instagram']
        
