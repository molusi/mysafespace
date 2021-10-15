from django.template.defaultfilters import stringfilter
from django import template
from django.db.models import Q
from books.models import *

register = template.Library()


@register.inclusion_tag('books/home.html')
def get_book_list():

    return {'books': Book.objects.all()}


# @register.inclusion_tag('books/search.html')
#
#
# def search(request):
#     query = request.GET.get("q","")
#     if query:
#         qset = (
#                 Q(title__icontains=query) |
#                 Q(authors__name__icontains=query)|
#                 Q(publisher__name__icontains=query)
#                 )
#         results = Book.objects.filter(qset).distinct()
#         print(results)
#     else:
#         results = []
#         return {"results": results,"query": query}
