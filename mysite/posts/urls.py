# -*- coding: utf-8 -*-

from django.urls import path
from . import views 

app_name = 'posts'
urlpatterns = [
	path('', views.IndexView, name='index'),
	path('p/<int:page>/', views.PageView, name='page'),
	path('d/<int:pk>/', views.Detail.as_view(), name='detail'),
]