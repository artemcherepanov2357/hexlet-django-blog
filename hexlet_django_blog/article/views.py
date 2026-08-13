from django.shortcuts import render

# hexlet_django_blog/article/views.py
from django.http import HttpResponse


def index(request):
    context = {
        'app_name': 'Блог о Django',  # Название приложения
        'articles': []  # Пока пустой список, позже добавите статьи из базы данных
    }
    return render(request, 'articles/index.html', context)
