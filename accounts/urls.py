import blog
from . import views
from .views import logmeout
from django.urls import path
from.models import *
from blog import views

app_name='accounts'

urlpatterns = [
    path('',blog.views.person_login,name="person_login"),
    path('register',views.createaccount,name="create_account"),
    path('logout/',logmeout,name='logout'),

    ]