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


	class Meta:
		verbose_name = '用户'
		verbose_name_plural = '一群用户'

	def __str__(self):
		return self.nickName


class Post(models.Model):
	title = models.CharField(verbose_name='标题', max_length=30)
	text = models.TextField(verbose_name='正文内容', null=True, blank=True)
	createDate = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
	editDate = models.DateTimeField(verbose_name='编辑时间', auto_now=True)
	user = models.ForeignKey(User, verbose_name='发帖人', null=True, on_delete=models.SET_NULL)
	show = models.BooleanField(verbose_name='是否显示', default=True)
	likeNum = models.IntegerField(verbose_name='点赞数', default=0)
	readNum = models.IntegerField(verbose_name='阅读人数', default=0)


	class Meta:
		verbose_name = '帖子'
		verbose_name_plural = '贴吧'

	def __str__(self):
		return self.title


class Comment(models.Model):
	text = models.TextField(verbose_name='评论内容')
	publishDate = models.DateTimeField(verbose_name='评论日期', auto_now_add=True)
	likeNum = models.IntegerField(verbose_name='点赞数', default=0)
	user = models.ForeignKey(User, verbose_name='评论者', null=True, on_delete=models.SET_NULL)
	contentType = models.ForeignKey(ContentType, verbose_name='评论类型', on_delete=models.CASCADE)
	objectId = models.PositiveIntegerField()
	contentObject = GenericForeignKey('contentType', 'objectId')


	class Meta:
		verbose_name = '评论'
		verbose_name_plural = '集体吐槽'

	def __str__(self):
		return self.text[:10]


class Like(models.Model):
	time = models.DateTimeField(verbose_name='点赞时间', auto_now_add=True)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	contentType = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	objectId = models.PositiveIntegerField()
	contentObject = GenericForeignKey('contentType', 'objectId')

	def __str__(self):
		try:
			ret = self.user.nickName
		except:
			return None
		else:
			return ret


class Read(models.Model):
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	readDate = models.DateTimeField(auto_now_add=True)