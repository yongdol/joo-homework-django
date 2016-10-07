from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.views import generic


# class IndexView(generic.ListView):
#     template_name = 'index.html'
#     context_object_name = 'latest_question_list'
#
#     def get_queryset(self):
#         return Question.objects.order_by('-pub_date')[:5]
#
# class DetailView(generic.DetailView):
#     model = Question
#     template_name = 'detail.html'
#
# class ResultsView(generic.DetailView):
#     model = Question
#     template_name = 'results.html'

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'latest_question_list' : latest_question_list,
    }
    return render(request, 'index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'detail.html', {'question' : question})

def results(request,question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'results.html', {'question' : question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.POST)
    try:
        add_choice_name = request.POST['add_choice_data']
        if add_choice_name == '':
            return HttpResponse('choice_ name is required')
        elif len(add_choice_name) < 3:
            return HttpResponse('choice_ name is too short')
    except (KeyError):
        raise HttpResponse('choice_name kye does not exist')
    question.choice_set.create(choice_text=add_choice_name)
    redirect_url = reverse('polls:detail', args=(question_id,))
    return HttpResponseRedirect(redirect_url)