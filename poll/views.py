from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.http import Http404
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from .forms import PersonForm

# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'poll/index.html', context)
class IndexView(generic.ListView):
    template_name = 'poll/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


# def detail(request, question_id):
#     try:
#         question = Question.objects.get(pk=question_id)
#     except Question.DoesNotExist:
#         raise Http404("Question does not exist")
#     return render(request,'poll/detail.html',{'question':question})
class DetailView(generic.DetailView):
    model = Question
    template_name = 'poll/detail.html'

    # def get_queryset(self):
    #     """
    #     Excludes any questions that aren't published yet.
    #     """
    #
    #     return Question.objects.filter(pub_date__lte=timezone.now())


# def results(request,question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     #response= "You are looking at the results of question %s."
#     return render(request,'poll/results.html',{'question':question})
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'poll/results.html'


def vote(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError,Choice.DoesNotExist):
        return render(request, 'poll/detail.html',{'question':question,'error message':"You didn't select a choice."})
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll:results',args=(question.id,)))


def get_name(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NameForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('poll:thanks'))
    # if a GET (or any other method) we'll create a blank form
    else:
        form = NameForm()
    return render(request,'poll/name.html', {'form': form})


class thanks(generic.ListView):
    template_name = 'poll/thanks.html'

    def get_queryset(self):
        pass

