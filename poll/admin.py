from django.contrib import admin
from . models import *
# Register your models here.

admin.site.site_header = "Welcome to the polling app Admin"
admin.site.site_title = "Polling app Admin Area"
admin.site.index_title = "Welcome to the polling app admin area"


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date','was_published_recently')
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes':['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date']
    search_fields = ['question_text']


# class QuestionAdmin(admin.ModelAdmin):
#     list_display = ("question_text", 'pub_date',')
#
#
# class ChoiceAdmin(admin.ModelAdmin):
#     list_display = ('question', 'choice_text','votes')


admin.site.register(Question,QuestionAdmin)
# admin.site.register(Choice)
