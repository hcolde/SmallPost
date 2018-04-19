# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

GENDER_CHOICE = [
	('M', '男'),
	('F', '女'),
]


class User(models.Model):
	'''
	用户信息表.
	token: 记录用户登录时的token，防止多人使用同一账号.
	'''

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
	'''
	帖子详情表.
	1. 创建帖子的时间不可更改,帖子被编辑后自动记录编辑的时间.
	2. 当发帖人的账号被删除后,user字段为空.帖子不会因为发帖人账号被删除而被删除.
	3. 当发帖人删除已发表的帖子后,帖子不会从数据库中删除,而是将show字段设为False,并不会在客户端显示.
	'''

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
	'''
	评论表.
	1. 发表评论的时间不可更改.
	2. 用户在发表评论后被删除账号,该评论不会被删除,且user字段设为空.
	3. 评论的操作可分为1)给帖子评论;2)给评论回复.当执行1)操作时,评论表应该与帖子详情表建立外键关系;
	当执行2)操作时,评论表应该与评论表建立外键关系.
	'''

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
	'''
	点赞表.
	可以给帖子或者评论点赞.当给帖子点赞时，应与帖子详情表建立外键关系;
	给评论点赞时应与评论表建立外键关系.
	'''

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
	'''
	阅读表.
	记录一个帖子被多少位用户阅读过.
	'''

	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	readDate = models.DateTimeField(auto_now_add=True)