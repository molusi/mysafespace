from . import views
from .views import *
from django.urls import path
from.models import *
app_name="todo_app"
urlpatterns = [
               path('todo_app/',views.index,name="index"),
               path('list/',views.todo_list,name="list"),
               path('list/delete_todo/',views.todo_list,name="list-delete"),
               path('add_todo/',views.add_todo,name="add_todo"),
               path('delete_todo/',views.index,name="delete_todo_plain"),
               path('delete_todo/<int:todo_id>/',views.delete_todo,name="delete_todo"),
               path('list/delete_todo/<int:todo_id>/',views.delete_todo,name="delete_todo_list"),
               path("todo/<int:pk>",views.DetailView.as_view(), name='detail')]