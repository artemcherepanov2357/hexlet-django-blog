from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from hexlet_django_blog.article.forms import ArticleForm
from hexlet_django_blog.article.models import Article


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(
            request,
            "articles/index.html",
            context={"articles": Article.objects.all()[:15]},
        )


class ArticleView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])
        return render(
            request,
            "articles/show.html",
            context={"article": article},
        )


class ArticleFormCreateView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "articles/create.html", {"form": ArticleForm()})

    def post(self, request, *args, **kwargs):
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save()
            messages.success(request, f'Статья "{article.name}" успешно создана!')
            return redirect("article:articles")
        messages.error(request, "Пожалуйста, исправьте ошибки в форме.")
        return render(request, "articles/create.html", {"form": form})


class ArticleFormEditView(View):
    def get(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])
        return render(
            request,
            "articles/update.html",
            {"form": ArticleForm(instance=article), "article_id": article.id},
        )

    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            messages.success(request, f"Статья '{article.name}' успешно обновлена!")
            return redirect("article:articles")
        return render(
            request,
            "articles/update.html",
            {"form": form, "article_id": article.id},
        )


class ArticleFormDeleteView(View):
    def post(self, request, *args, **kwargs):
        article = get_object_or_404(Article, id=kwargs["id"])
        name = article.name
        article.delete()
        messages.success(request, f'Статья "{name}" успешно удалена!')
        return redirect("article:articles")
