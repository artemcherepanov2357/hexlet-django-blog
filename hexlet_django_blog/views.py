# hexlet_django_blog/views.py
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView
from django.urls import reverse
from django.views import View


class IndexView(TemplateView):
    template_name = 'index.html'


class AboutView(TemplateView):
    template_name = 'about.html'