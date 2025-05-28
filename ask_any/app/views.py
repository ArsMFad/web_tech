from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse
from . import models
from .forms import LoginForm, SignUpForm, AskForm, AnswerForm, SettingsForm


def paginate(objects_list, request, per_page=5):
    try:
        if objects_list is None or not hasattr(objects_list, '__len__'):
            raise ValueError("Invalid objects list for pagination")
        
        if len(objects_list) == 0:
            paginator = Paginator([], per_page)
            return paginator.page(1)
        
        paginator = Paginator(objects_list, per_page)
        page_num = request.GET.get('page', 1)
        
        try:
            page = paginator.page(page_num)
        except PageNotAnInteger:
            page = paginator.page(1)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)
            
        return page
    except Exception as e:
        raise Http404(f"Pagination error: {str(e)}")


def index(request):
    questions = models.Question.get_index_questions()
    page = paginate(questions, request, 5)
    return render(request, 'index.html', {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


def hot(request):
    questions = models.Question.get_hot_questions()
    page = paginate(questions, request, 5)
    return render(request, 'hot.html', {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


def question(request, question_id):
    question_obj = models.Question.objects.get(pk=question_id)
    
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user
            answer.question = question_obj
            answer.save()
            return HttpResponseRedirect(f"{reverse('question', args=[question_id])}?answer={answer.id}")
    else:
        form = AnswerForm()
    
    answers = models.Answer.objects.filter(question=question_obj)
    print(answers)
    page = paginate(answers, request, 5)
    print(page)
    
    return render(request, 'single_question.html', {
        'question': question_obj,
        'answers': page.object_list,
        'page_obj': page,
        'form': form,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


@login_required
def settings(request):
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('settings')
    else:
        form = SettingsForm(instance=request.user)
    
    return render(request, 'settings.html', {'form': form})


def registration(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    
    return render(request, 'registration.html', {
        'form': form,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            next_url = request.GET.get('next', 'index')
            return redirect(next_url)
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {
        'form': form,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


@login_required
def logout(request):
    auth_logout(request)
    return redirect(request.META.get('HTTP_REFERER', 'index'))


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            
            tags = form.cleaned_data['tags'].split(',')
            for tag_name in tags:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = models.Tag.objects.get_or_create(title=tag_name)
                    question.tags.add(tag)
            
            return redirect('question', question_id=question.id)
    else:
        form = AskForm()
    
    return render(request, 'ask.html', {
        'form': form,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })


def tag(request, tag_title):
    questions = models.Question.objects.filter(tags__title=tag_title).distinct()
    page = paginate(questions, request, 5)
    
    return render(request, 'tag.html', {
        'questions': page.object_list,
        'page_obj': page,
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
        'tag': tag_title,
    })


def page_not_found_view(request, exception):
    return render(request, '404.html', status=404, context={
        'popular_tags': models.Tag.get_popular_tags(),
        'best_members': models.Profile.get_best_members(),
    })
