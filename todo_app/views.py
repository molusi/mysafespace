from django.core.exceptions import ValidationError
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, request
from .models import *
from .forms import *
from django.views.generic.edit import CreateView
from django.views.generic import ListView,DetailView,CreateView
from django.urls import reverse, reverse_lazy
# Create your views here.
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages, auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,DetailView
User=get_user_model()



@login_required(login_url='accounts:person_login')
def index(request):
    form = TodoForm()
    todos=Todo.objects.filter(user=request.user).order_by('-created')[:5]
    return render(request,"todo_app/index.html",context={"todos":todos,"form":form})

@login_required(login_url='accounts:person_login')
def todo_list(request):
    todos = Todo.objects.filter(user=request.user).all()
    return render(request, "todo_app/todolist.html", context={"todos": todos})



def add_todo(request):
    if request.method=='POST':
        form= TodoForm(request.POST)
        if form.is_valid():
            user=request.user
            title = form.cleaned_data['title']
            text=form.cleaned_data['text']
            complete=form.cleaned_data['complete']
            todo=Todo(user=user,title=title,text=text,complete=complete)
            todo.save()
            return redirect("todo_app:index")



def delete_todo(request,todo_id):
    todo=get_object_or_404(Todo,pk=todo_id)
    todo.delete()
    messages.success(request,f'{todo} deleted successfully.')
    return redirect('todo_app:index')

def confirm_delete(request,todo_id):
    if request.method == 'POST':
        todo=get_object_or_404(Todo,pk=todo_id)
        deleted_todo=todo.delete()
    return HttpResponseRedirect(reverse('todo_app:index'))


class DetailView(DetailView):
    model = Todo
    template_name = 'todo_app/Detail.html'


