from django.urls import path
from books.views import *
from . import views

app_name = "books"
urlpatterns = [
    path('',BookHomeView.as_view(),name="home"),
    path('publishers/',PublisherListView.as_view(),name="publishers"),
    path('our_books/', BookListView.as_view(), name="our_books"),
    path('<int:pk>/',BookDetailView.as_view(),name="book_detail"),
    path('publishers/<int:pk>/',PublisherDetailView.as_view(),name="publisher_detail"),
    path('publishers/<publisher>/', PublisherBookListView.as_view(),name="publisher_booklist"),
    path('authors/',AuthorListView.as_view(),name="authors"),
    path('search/',SearchView.as_view(),name="search"),
    path('authors/<int:pk>/',AuthorDetailView.as_view(),name="author_detail"),
    path('contact/',views.ContactView.as_view(),name="contact"),
    path('thanks',ThanksView.as_view(),name="thanks")
]
