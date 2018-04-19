# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

GENDER_CHOICE = [
	('M', '男'),
	('F', '女'),
]


class User(models.Model):
	account = models.CharField(verbose_name='账号', max_length=11)
	password = models.CharField(verbose_name='密码', max_length=18)
	nickName = models.CharField(verbose_name='昵称', max_length=8)
	token = models.CharField(max_length=32)
	headPortrait = models.ImageField(verbose_name='头像', upload_to='uploads/')
	sex = models.CharField(verbose_name='性别', max_length=2, choices=GENDER_CHOICE)

	def __str__(self):
		return self.nickName


class Post(models.Model):
	title = models.CharField(verbose_name='标题', max_length=30)
	text = models.TextField(verbose_name='正文内容', null=True, blank=True)
	createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	editDate = models.DateTimeField(verbose_name='编辑时间', auto_now=True)
	userId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	show = models.BooleanField(verbose_name='是否显示', default=True)

	def __str__(self):
		return self.title


class Comment(models.Model):
	content = models.TextField(verbose_name='回帖内容')
	publishDate = models.DateTimeField(verbose_name='回帖日期', auto_now_add=True)
	userId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	postId = models.ForeignKey(Post, null=True, on_delete=models.SET_NULL)

	def __str__(self):
		return self.content[:10]


class Reply(models.Model):
	content = models.TextField(verbose_name='评论内容')
	publishDate = models.DateTimeField(verbose_name='评论日期', auto_now_add=True)
	userId = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	objectId = models.PositiveIntegerField()
	contentObject = GenericForeignKey('contentType', 'objectId')

	def __str__(self):
		return self.content[:10]


'''
class PostLike(models.Model):
	postId = models.ForeignKey(Post, on_delete=models.CASCADE)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	lickNum = models.IntegerField(default=0)


class CommentLike(models.Model):
	commentId = models.ForeignKey(Comment, on_delete=models.CASCADE)
	userId = models.ForeignKey(User, on_delete=models.CASCADE)
	time = models.DateTimeField(auto_now_add=True)
	lickNum = models.IntegerField(default=0)
'''