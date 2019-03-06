from django.urls import path
from . import views
from django.views.generic import TemplateView


# See https://docs.djangoproject.com/en/2.1/topics/http/urls/
app_name = "demo"  # https://docs.djangoproject.com/en/2.1/intro/tutorial03/#namespacing-url-names
urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('get_notes', views.get_notes),
    path('add_notes', views.add_notes),
    path('', views.index),
]