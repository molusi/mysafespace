from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView,DetailView,TemplateView
from books.models import *
from django.db.models import Q
from .forms import ContactForm
from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse
from django.views import View
from django.views.generic.detail import SingleObjectMixin
from django.core.mail import send_mail
from django.views.generic import FormView
from django.contrib import messages, auth



class BookHomeView(ListView):
    template_name = 'books/home.html'
    queryset = Book.objects.all()
    context_object_name = 'books'

class AuthorListView(ListView):
    queryset = Author.objects.all()
    template_name = 'books/authors.html'
    context_object_name = 'authors'

class SearchView(View):
    template_name = 'books/search.html'

    def get(self,*args, **kwargs):
        query = self.request.GET.get("q", "")
        if query:
            qset = (
                    Q(title__icontains=query) |
                    Q(authors__name__icontains=query) |
                    Q(publisher__name__icontains=query)
            )
            results = Book.objects.filter(qset).distinct()
            context = {"results": results, "query": query}
            return render(self.request, self.template_name, context)
        else:
            return redirect('books:home')


class BookDetailView(DetailView):
    model = Book
    template_name = "books/book_details.html"
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher_list'] = Publisher.objects.all()
        return context


class AuthorDetailView(DetailView):
    model = Author
    template_name = "books/author_detail.html"


class ContactView(FormView):
    template_name = 'books/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {"form":form}
        return render(request,self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return HttpResponseForbidden()
        form =ContactForm(request.POST)
        if form.is_valid():
            topic = form.cleaned_data['topic']
            message = form.cleaned_data['message']
            sender = form.cleaned_data.get('sender', 'noreply@example.com')
            form.save()
            # send_mail(
            #     'Feedback from your site, topic: %s' % topic,
            #     message, sender,
            #     ['molusi.abigail@gmail.com']
            # )
            return redirect('books:thanks')
        else:
            form.errors


class ThanksView(TemplateView):
    template_name = "books/thanks.html"








class PublisherBookListView(ListView):
    template_name = 'books/books_by_publisher.html'
    context_object_name = "books"

    def get_queryset(self):
        self.publisher = get_object_or_404(Publisher, name=self.kwargs['publisher'])
        return Book.objects.filter(publisher=self.publisher)

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in the publisher
        context['publisher'] = self.publisher
        return context


class PublisherListView(ListView):
    queryset = Publisher.objects.all()
    template_name = 'books/publishers.html'
    context_object_name = 'publishers'

class BookListView(ListView):
    queryset = Book.objects.all()
    template_name = 'books/our_books.html'
    context_object_name = 'books'






class PublisherDetailView(SingleObjectMixin, ListView):
    model=Publisher
    template_name = "books/publisher_detail.html"
    context_object_name = "publisher"
    paginate_by = 2

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Publisher.objects.all())

        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['publisher'] = self.object
        return context

    def get_queryset(self):
        return self.object.book_set.all()











