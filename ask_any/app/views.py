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
