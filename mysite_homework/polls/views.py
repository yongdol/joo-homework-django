from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from .models import Question, Choice
from django.urls import reverse
from django.utils import timezone



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
    latest_question_list = Question.objects.order_by('-pub_date')[:10]
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


def add_question(request):

    add_question_name = request.POST['add_question_data']
    if add_question_name == '':
        return HttpResponse('question name is required')
    elif len(add_question_name) < 5:
        return HttpResponse('question is too short')
    else:
        q = Question(question_text=add_question_name, pub_date=timezone.now())
        q.save()
        redirect_url = reverse('polls:index')
        return HttpResponseRedirect(redirect_url)


def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        add_choice_name = request.POST['add_choice_data']
        if add_choice_name == '':
            return HttpResponse('choice_ name is required')
        elif len(add_choice_name) < 1:
            return HttpResponse('choice_ name is too short')
    except(KeyError):
        raise HttpResponse('choice_name key does not exist')
    question.choice_set.create(choice_text=add_choice_name)
    redirect_url = reverse('polls:detail', args=(question_id,))
    return HttpResponseRedirect(redirect_url)


def choice_delete_question(request):
    question_lists = Question.objects.all()
    context = {
        'question_lists': question_lists,
    }
    return_value = request.POST.get('return')
    choice_question = request.POST.get('question_id')

    if choice_question is not None:
        print("choice question id: %s" % choice_question)
        delete_question = Question.objects.get(id=choice_question)
        delete_question.delete()
        print("delete complete")
        if return_value is not None:
            return render(request, 'choice_delete_question.html', context)
        else:
            return render(request, 'choice_delete_question.html', context)
    else:
        print("ELSE구문탔음")
        if return_value is not None:
            index_url = reverse('polls:index')
            return HttpResponseRedirect(index_url)
        else:
            return render(request, 'choice_delete_question.html', context)

