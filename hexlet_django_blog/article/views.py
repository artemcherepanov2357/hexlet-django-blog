# hexlet_django_blog/article/views.py

from django.http import HttpResponse
from django.views import View
from django.shortcuts import render

from hexlet_django_blog.article.models import Article


class IndexView(View):
    def get(self, request, *args, **kwargs):
        articles = Article.objects.all()[:15]
        return render(
            request,
            "articles/index.html",
            context={
                "articles": articles,
            },
        )

# class ArticleIndexView(View):
#     def get(self, request, *args, **kwargs):
#         return render(request, 'articles/index.html')


def article_detail(request, tags, article_id):
    return HttpResponse(f'Статья номер {article_id}. Тег {tags}')