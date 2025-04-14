import copy
import random

from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import models
from django.http import Http404


possible_tags = ['perl', 'python', 'c']
best_members_list = ['Mr.Freeman', 'Dr.House', 'Bender', 'Queen Victoria', 'V.Pupkin']

COLOR_BY_IMPORTANCE = {
    0: 'black',
    1: 'red',
    2: 'green'
}

FONT_SIZE_BY_IMPORTANCE = {
    0: '0.83em',
    1: '1.2em',
    2: '1.53em'
}

def count_popular_tags():
    to_ret = []

    for i in range(10):
        rnd = random.randint(0, 2)
        to_ret.append({
            'title': possible_tags[rnd],
            'id': i,
            'href': '#',
            'importance': rnd,
            'color': COLOR_BY_IMPORTANCE[rnd],
            'font_size': FONT_SIZE_BY_IMPORTANCE[rnd]
        })
    
    return to_ret


def count_questions():
    to_ret = []

    for i in range(30):
        to_ret.append({
            'title': f'Title ({i})',
            'id': i,
            'text': f'This is text for question {i}',
            'img_path': '/img/spectre.jpg',
            'tags': [possible_tags[random.randint(0, 2)]]
        })
    
    return to_ret


def count_best_members():
    to_ret = []

    for i in range(5):
        to_ret.append({
        'title': best_members_list[i],
        'id': i,
        'href': '#'
    })
    
    return to_ret

QUESTIONS = count_questions()


POPULAR_TAGS = count_popular_tags()

BEST_MEMBERS = count_best_members()

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
    try:
        if not objects_list or not hasattr(objects_list, '__len__'):
            raise Http404("Pagination error")
        
        paginator = Paginator(objects_list, per_page)
        
        try:
            page_num = int(request.GET.get('page', 1))
        except (ValueError, TypeError):
            page_num = 1
        
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            
        return page
        
    except Exception as e:
        raise Http404("Pagination error")



def index(request):
    page = paginate(models.Question.objects.all(), request, 5)

    return render(request, template_name='index.html', context={
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER,
        'answers': ANSWERS_NULL})


def hot(request):
    q = reversed(copy.deepcopy(QUESTIONS))
    return render(request, template_name='hot.html', context={
        'questions': q,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER})


def question(request, question_id):
    page = paginate(ANSWERS, request, 5)

    return render(request, template_name='single_question.html', context={
        'question': QUESTIONS[question_id],
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER,
        'answers': page.object_list,
        'page_obj': page,})


def settings(request):
    return render(request, template_name='settings.html', context={
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER})


def registration(request):
    return render(request, template_name='registration.html', context={
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_OUT_USER})


def login(request):
    return render(request, template_name='login.html', context={
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_OUT_USER})


def ask(request):
    return render(request, template_name='ask.html', context={
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER})


def tag(request, tag_title):
    DATA_ARRAY = [i for i in QUESTIONS if tag_title in i['tags']]
    page = paginate([i for i in QUESTIONS if tag_title in i['tags']], request, 5)

    return render(request, template_name='tag.html', context={
        'questions': DATA_ARRAY,
        'popular_tags': POPULAR_TAGS,
        'best_members': BEST_MEMBERS,
        'user': LOGGED_IN_USER,
        'answers': page.object_list,
        'page_obj': page,
        'tag': tag_title})
