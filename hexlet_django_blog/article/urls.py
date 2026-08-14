# hexlet_django_blog/article/views.py
from django.urls import path

from hexlet_django_blog.article import views

from . import views

app_name = 'article'  # пространство имен

urlpatterns = [
    # Маршрут для списка статей (уже есть)
    path('', views.ArticleIndexView.as_view(), name='index'),

    # Новый динамический маршрут для конкретной статьи
    # /articles/tags/article_id/
    path('<str:tags>/<int:article_id>/', views.article_detail, name='article_detail'),
]