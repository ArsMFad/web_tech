import copy
import random

from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from django.db.models import Count


LOGGED_IN_USER = {
    'name': 'Dr.Pepper',
    'avatar': '/img/cacodemon.jpg',
    'is_logged': 1
}

LOGGED_OUT_USER = {
    'name': 'null',
    'avatar': 'null',
    'is_logged': 0
}

ANSWERS = [{
    'text': f'Title({i}) First of all I would like to thank you for the invitation to participate in such a... Russia is the huge territory which in many respects needs to be render habitable.',
} for i in range(30)
]

ANSWERS_NULL = 'null'

def paginate(objects_list, request, per_page=5):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(objects_list, per_page)
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)

    return page

def get_popular_tags():
    return models.Tag.objects.annotate(
        num_questions=Count('question')
    ).order_by('-num_questions')[:10]


def get_best_members():
    return models.User.objects.all().order_by('-rating')[:5]


def index(request):
    page = paginate(models.Question.objects.all(), request, 5)

    return render(request, template_name='index.html', context={
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER,
        })


def hot(request):
    questions = models.Question.objects.all().order_by('-rating')[:20]
    page = paginate(questions, request, 5)

    return render(request, template_name='hot.html', context={
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER,
        })


def question(request, question_id):
    page = paginate(models.Answer.objects.all(), request, 5)

    return render(request, template_name='single_question.html', context={
        'question': models.Question.objects.get(pk=question_id),
        'answers': page.object_list,
        'page_obj': page,
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER,
        })


def settings(request):
    return render(request, template_name='settings.html', context={
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER
        })


def registration(request):
    return render(request, template_name='registration.html', context={
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_OUT_USER
        })


def login(request):
    return render(request, template_name='login.html', context={
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_OUT_USER
        })


def ask(request):
    return render(request, template_name='ask.html', context={
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER
        })


def tag(request, tag_title):
    questions = models.Question.objects.filter(tags__title=tag_title).distinct()

    paginator = Paginator(questions, 5)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, template_name='tag.html', context={
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': get_popular_tags(),
        'best_members': get_best_members(),
        'user': LOGGED_IN_USER,
        'tag': tag_title
        })
