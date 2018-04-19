# -*- coding: utf-8 -*-

from django.urls import path
from . import views 

app_name = 'posts'
urlpatterns = [
	path('', views.IndexView, name=index),
	path('Register/', views.RegisterView, name=register),
	path('Login/', views.LoginView, name=login),
	path('Post/<int:page>', views.PostView, name=post),
	path('Detail/<int:pk>', views.Detail, name=detail),
]