# -*- coding: utf-8 -*-

from django.urls import path
from . import views 

app_name = 'posts'
urlpatterns = [
	path('', views.IndexView, name='index'),
	#path('Post/<int:page>', views.PostView, name=post),
	#path('Detail/<int:pk>', views.Detail, name=detail),
]