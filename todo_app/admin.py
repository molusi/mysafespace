from django.contrib import admin
from . models import *
from django.contrib.auth import get_user_model

User=get_user_model()



class TodoAdmin(admin.ModelAdmin):
    list_display = ('title', 'text','created','complete')
    list_filter = ['user']
    search_fields = ['user']

admin.site.register(Todo,TodoAdmin)
