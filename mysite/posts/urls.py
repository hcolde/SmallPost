# -*- coding: utf-8 -*-

from django.urls import path
from . import views 

app_name = 'posts'
urlpatterns = [
	path('', views.IndexView, name='index'),
	path('p/<int:page>/', views.PageView, name='page'), #分页. 
	path('d/<int:pk>/', views.Detail.as_view(), name='detail'), #帖子详情. 
	path('mine/', views.MineView, name='mine'), #个人主页. 
	path('mine/<int:types>/', views.MyData, name='myData'), #个人发帖/评论 分页.
]