import copy

from django.shortcuts import render


QUESTIONS = [
    {
        'title': f'Title ({i})',
        'id': i,
        'text': f'This is text for question {i}',
        'img_path': '/img/spectre.jpg',
    } for i in range(30)
]


def index(request):
    return render(request, template_name='index.html', context={'questions': QUESTIONS})


def hot(request):
    q = reversed(copy.deepcopy(QUESTIONS))
    return render(request, template_name='hot.html', context={'questions': q})


def question(request, question_id):
    return render(request, template_name='single_question.html', context={'question': QUESTIONS[question_id]})