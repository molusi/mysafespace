from django.contrib import admin
from .models import *

class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'address','city','state_province','country','website')
    list_filter = ['name']
    search_fields = ['name','city','country']


class BookAdmin(admin.ModelAdmin):
    list_display = ('title','publisher','publication_date')
    list_filter = ['title','authors']
    search_fields = ['name','city','country','publisher']


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('salutation', 'name','email')
    list_filter = ['name']
    search_fields = ['name']


class ContactAdmin(admin.ModelAdmin):
    list_display = ('topic', 'message','sender')
    list_filter = ['topic']
    search_fields = ['topic','sender']

admin.site.register(Publisher,PublisherAdmin)
admin.site.register(Book,BookAdmin)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Contact,ContactAdmin)


