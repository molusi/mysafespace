from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import render,redirect
from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import *
from .forms import *
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages, auth
from itertools import chain
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.views.generic import TemplateView,View,ListView
from django.core.exceptions import ValidationError, ObjectDoesNotExist,MultipleObjectsReturned
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseRedirect, request
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic import ListView,DetailView,CreateView,View
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
import random
import string
import datetime
from accounts.models import User
from . models import Article
from accounts.forms import UserForm,CreateuserForm
user = get_user_model()



def bloghome(request,*args, **kwargs):
    try:
        articles = Article.objects.all().order_by('-created')
        p = Paginator(articles, 3)
        page_number = request.GET.get('page')
        try:
            page_obj = p.get_page(page_number)
        except PageNotAnInteger:
            page_obj = p.page(1)
        except EmptyPage:
            page_obj = p.page(p.num_pages)
        context = {"articles": articles,"page_obj": page_obj}
        return render(request, "blog/index.html", context)
    except ObjectDoesNotExist:
        messages.info(request, "No articles to show..")
        return redirect('blog:myposts')


class MyPostsView(ListView):
    def get(self,*args,**kwargs):
        try:
            articles = Article.objects.filter(author__user=self.request.user)
            context = {"articles":articles}
            return render(self.request,"blog/myposts.html",context)
        except ObjectDoesNotExist:
            messages.info(self.request,"No articles to show..Add your first article")
            return redirect('blog:myposts')

def person_login(request):
    if request.user.is_authenticated:
        return redirect('blog:home')
    else:
        form = UserForm()
        if request.method == 'POST':
            email = request.POST.get('email')
            password = request.POST.get('password')
            user = authenticate(request, email=email,password=password)
            if user is not None:
                login(request,user)
                return redirect('todo_app:index')
            else:
                messages.error(request,'Invalid credentials')
        return render(request, 'accounts/person_login.html',{"form":form})


def createaccount(request):
    if request.user.is_authenticated:
        return redirect('blog:userprofile_create')
    else:
        form = CreateuserForm()
        if request.method == 'POST':
            form = CreateuserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect(reverse_lazy("accounts:person_login"))
            else:
                form.errors
        return render(request, 'accounts/register.html', {"form": form})


@login_required
def articlecreateview(request,*args,**kwargs):
    try:
        userprofile = Userprofile.objects.get(user__email=request.user)
    except ObjectDoesNotExist:
        messages.info(request, 'Please complete your profile first...')
        return redirect('blog:userprofile_create')
    initial_data = {'author':userprofile.preffered_name}
    form = ArticleForm(request.POST or None,initial=initial_data)
    context = {'form': form}
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            category = form.cleaned_data.get('category')
            if 'image' in request.FILES:
                picture = request.FILES.get('image')
                article = Article()
                article.title = title
                article.category = category
                article.content = content
                article.image = picture
                article.author = get_object_or_404(Userprofile,user__email=request.user)
                article.save()
                context["article"] = article
                return redirect('blog:home')
            else:
                article = Article()
                article.title = title
                article.category = category
                article.content = content
                article.author = get_object_or_404(Userprofile,user__email=request.user)
                article.save()
                context["article"] = article
                return redirect('blog:home')
        else:
            print(form.errors)
    return render(request, "blog/article_create.html", context)


def commentupdate(request,pk,*args,**kwargs):
    comment_ = get_object_or_404(Comment,id=pk)
    article_ = comment_.article
    initial_data = {"content":comment_.content}
    form = CommentForm(request.POST or None, initial=initial_data)
    context = {"comment": comment_,"article": article_,"form":form}
    if request.method == 'POST':
        form = CommentForm(request.POST,initial=initial_data)
        if form.is_valid():
            content = form.cleaned_data.get("content")
            comment = Comment()
            comment.content = content
            comment.article = article_
            comment.author=comment_.author
            comment.save()
            return HttpResponseRedirect(reverse("blog:detail",kwargs={"pk":article_.pk}))
        else:
            form.errors
    else:
        form=CommentForm()
    return render(request,"blog/articledetail.html",context)




class ArticleUpdateView(LoginRequiredMixin,UpdateView):
    form_class = ArticleModelForm
    template_name = 'blog/article_update.html'
    queryset = Article.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Article,pk=id_)











class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/articledetail.html'


class ArticleDeleteView(LoginRequiredMixin,DeleteView):
    model = Article
    template_name = 'blog/article_delete.html'

    def get_object(self):
        id_= self.kwargs.get("pk")
        return get_object_or_404(Article,pk=id_)

    def get_success_url(self):
        return reverse('blog:myposts')

class SearchView(View):
    template_name = 'blog/search.html'

    def get(self,*args, **kwargs):
        query = self.request.GET.get("q", "")
        if query:
            qset = (
                    Q(title__icontains=query) |
                    Q(author__preffered_name__icontains=query) |
                    Q(category__icontains=query) |
                    Q(content__icontains=query)
            )
            results = Article.objects.filter(qset).distinct()
            context = {"results": results, "query": query}
            return render(self.request, self.template_name, context)
        else:
            return redirect('blog:home')




@login_required
def userprofileview(request,*args,**kwargs):
    user = get_user_model()
    initial_data = {"user": request.user}
    form = UserProfileForm()
    context={'form':form}
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            preffered_name = form.cleaned_data.get('preffered_name')
            about = form.cleaned_data.get('about')
            if 'profilepic' in request.FILES:
                profilepicture = request.FILES.get('profilepic')
                userprofile = Userprofile(user=user, preffered_name=preffered_name,about=about,profilepic=profilepicture)
            else:
                userprofile = Userprofile(user=user, preffered_name=preffered_name, about=about)
            userprofile.save()
            context["userprofile"] = userprofile
            return HttpResponseRedirect(reverse('blog:existingprofile',kwargs={'pk':userprofile.user.id}))
        else:
            form.errors
    return render(request, "blog/profile.html",context)

class UserProfileUpdateView(LoginRequiredMixin,UpdateView):
    form_class = UserProfileUpdateForm
    template_name = 'blog/existing_profile_update.html'
    queryset = Userprofile.objects.all()

    def get_object(self):
        id_ = self.kwargs.get("pk")
        return get_object_or_404(Userprofile, pk=id_)





def existinguserprofile(request,pk):
    try:
        userprofile = Userprofile.objects.get(user__id=pk)
        result = list(chain(Article.objects.filter(author__id=userprofile.id)))
        context = {"userprofile":userprofile,"result":result}
        return render(request, 'blog/existing_profile.html', context)
    except ObjectDoesNotExist:
        if pk == request.user.id:
            return redirect("blog:userprofile_create")
        else:
            messages.info(request, 'Profile nolonger exists..')
            return HttpResponseRedirect(reverse('blog:article',kwargs={"pk":id}))























