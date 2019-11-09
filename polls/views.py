from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.utils import timezone
from polls.models import Question, Choice
from django.shortcuts import resolve_url as r
"""
https://docs.djangoproject.com/en/2.2/intro/tutorial04/
"""


class IndexView(ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions (not including
            those set to be published in the future).
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]


index = IndexView.as_view()


class DetailView(DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
            Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


detail = DetailView.as_view()


class ResultsView(DetailView):
    model = Question
    template_name = 'polls/results.html'


results = ResultsView.as_view()


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        # F() -> To avoid race condition
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # This is if there are two selected_choice.save(), the selected_choice would be sum twice.
        selected_choice.refresh_from_db()

    return HttpResponseRedirect(r('polls:results', question.id))

"""
def index(resquest):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(resquest, 'polls/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

"""