# hexlet_django_blog/article/views.py
from django.contrib import messages
from django.http import HttpResponse
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect

from hexlet_django_blog.article.forms import ArticleForm
from hexlet_django_blog.article.models import Article
from django.shortcuts import render


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

class ArticleView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])

        return render(
            request,
            "articles/show.html",
            context={
                "article": article,
            },
        )


class ArticleFormCreateView(View):
    def get(self, request, *args, **kwargs):
        form = ArticleForm()
        return render(request, "articles/create.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            # Flash-сообщение об успехе
            messages.success(request, f'Статья "{article.name}" успешно создана!')
            return redirect('article:articles')  # Редирект на список статей
        # Если данные некорректные
        messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
        return render(request, 'articles/create.html', {'form': form})

