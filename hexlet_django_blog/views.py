# hexlet_django_blog/views.py
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.views import View


class IndexView(View):
    def get(self, request):
        # Перенаправление на /articles/python/42/
        # Используем reverse для получения URL
        url = reverse('article:article_detail', kwargs={
            'tags': 'python',
            'article_id': 42
        })
        return redirect(url)



class AboutView(TemplateView):
    template_name = 'about.html'