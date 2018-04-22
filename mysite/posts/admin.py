# -*- coding: utf-8 -*-

from django.contrib import admin
from .models import User, Post, Comment


class UserAdmin(admin.ModelAdmin):
	fieldsets = [
		('账号信息', {'fields': ['account', 'password', 'token'], 'classes':['collapse']}),
		('用户资料', {'fields': ['nickName', 'sex', 'headPortrait']}),
	]
	list_display = ('account', 'nickName', 'sex', 'createDate')
	list_filter = ['sex']
	search_fields = ['account', 'nickName']
	readonly_fields = ['account', 'nickName', 'token']


class PostAdmin(admin.ModelAdmin):
	fieldsets = [
		('帖子详情', {'fields': ['title', 'user', 'text']}),
		('帖子相关', {'fields': ['readNum', 'likeNum', 'show'], 'classes': ['collapse']}),
	]
	list_display = ('title', 'user', 'createDate', 'editDate', 'readNum', 'likeNum')
	list_filter = ['createDate', 'editDate', 'user']
	search_fields = ['user', 'title', 'text']
	readonly_fields = ['readNum', 'likeNum']


class CommentAdmin(admin.ModelAdmin):
	fieldsets = [
		('评论详情', {'fields': ['user', 'text']}),
		('评论相关', {'fields': ['contentType', 'likeNum'], 'classes': ['collapse']}),
	]
	list_display = ('text', 'user')
	list_filter = ['user']
	search_fields = ['user', 'text']
	readonly_fields = ['user' ,'contentType', 'likeNum']

admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)