from django.urls import path

from hexlet_django_blog.article.views import (
    ArticleFormCreateView,
    ArticleFormDeleteView,
    ArticleFormEditView,
    ArticleView,
    IndexView,
)

app_name = "article"

urlpatterns = [
    path("", IndexView.as_view(), name="articles"),
    path("<int:id>/edit/", ArticleFormEditView.as_view(), name="articles_update"),
    path("<int:id>/delete/", ArticleFormDeleteView.as_view(), name="articles_delete"),
    path("<int:id>/", ArticleView.as_view(), name="articles_show"),
    path("create/", ArticleFormCreateView.as_view(), name="articles_create"),
]
