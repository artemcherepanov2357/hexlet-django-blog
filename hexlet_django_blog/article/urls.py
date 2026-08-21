# hexlet_django_blog/article/views.py
from django.urls import path

from hexlet_django_blog.article.views import (
    IndexView, ArticleView, ArticleFormCreateView, ArticleFormEditView, ArticleFormDeleteView,
)

app_name = 'article'  # пространство имен

urlpatterns = [
    path("", IndexView.as_view(), name="articles"),
    path("<int:id>/edit/", ArticleFormEditView.as_view(), name="articles_update"),
    path("<int:id>/delete/", ArticleFormDeleteView.as_view(), name="articles_delete"),
    path("<int:id>/", ArticleView.as_view(), name="articles_show"),
    path("create/", ArticleFormCreateView.as_view(), name="articles_create"),
]
