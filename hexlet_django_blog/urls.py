"""
URL configuration for hexlet_django_blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
"""

from django.contrib import admin
from django.urls import include, path

from .views import AboutView, IndexView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("articles/", include("hexlet_django_blog.article.urls")),
    path("about/", AboutView.as_view(), name="about"),
    path("admin/", admin.site.urls),
]
