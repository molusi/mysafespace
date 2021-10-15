from django.urls import path
from . import views


app_name = 'poll'

urlpatterns = [
    path('',views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/',views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/',views.vote,name='vote'),
    path('get_name/',views.get_name,name='get_name'),
    path('get_name/thanks/',views.thanks.as_view(),name='thanks')
]