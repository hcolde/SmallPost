# -*- coding: utf-8 -*-

import datetime
import random
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse, JsonResponse
from django.views import generic
from django.urls import reverse
from django.core.paginator import Paginator
from .models import User, Post, Comment
from .forms import PostForm

def IndexView(request):
	'''
	首页视图.
	1. 展示帖子.
	2. 登录或注册时将表单POST到当前页面.
	'''

	nickName = request.COOKIES.get('nickName', None)
	msg = request.COOKIES.get('msg', None)
	if request.POST:
		if nickName and msg=='100':
			response = Posts(nickName, request.POST.get('PostTitle', None), request.POST.get('PostText', None))
			return response
		else:
			response = LoginOrRegirest(request.POST.get('belong', None), account=request.POST.get('account', None), password=request.POST.get('password1', None), nickName=request.POST.get('nickName', None), sex=request.POST.get('sex', None), headPortrait=request.FILES.get('headPortrait', None))
			if response:
				return response
			else:
				raise Http404('阿欧，迷路了！')
	info = Paging(1)
	return render(request, 'posts/index.html', info)

def PageView(request, page):
	'''
	分页视图.
	'''

	info = Paging(page)
	return render(request, 'posts/page.html', info)


class DetailView(generic.DetailView):
	'''
	帖子详情视图.
	'''

	model = Post
	template_name = 'posts/detail.html'

def Paging(page):
	'''
	Django分页方法.
	按编辑时间排序(倒序)，每页显示5条数据.
	'''

	show = 5
	posts = Post.objects.order_by('-editDate').all()
	paginator = Paginator(posts, show)
	contacts = paginator.get_page(page)
	info = {
		'contacts': contacts,
		'start': (page-1)*show+1,
	}
	return info

def LoginOrRegirest(which, **kw):
	'''
	区分登录或注册操作.
	'''

	data = None
	response = redirect('posts:index')
	if which == 'Login':
		data = Login(account=kw['account'], password=kw['password'])
		response.set_cookie('msg', data['msg'])
		response.set_cookie('nickName', data['nickName'])
		response.set_cookie('sex', data['sex'])
		response.set_cookie('headPortrait', data['headPortrait'])
		response.set_cookie('token', data['token'])
	elif which == 'Register':
		data = Register(account=kw['account'], password=kw['password'], nickName=kw['nickName'], sex=kw['sex'], headPortrait=kw['headPortrait'])
		response.set_cookie('msg', data['msg'])
	else:
		return None
	return response

def Login(**kw):
	'''
	执行登陆操作时调用
	1. msg:001 不存在该账号.
	2. msg:010 密码错误.
	3. msg:100 账号密码相匹配,登陆成功.
	登录成功后将赋予一个新的token值.
	'''

	json = {'nickName':None, 'sex':None, 'headPortrait':None, 'token':None}
	try:
		user = User.objects.get(account=kw['account'])
	except:
		json['msg'] = '001'
	else:
		if user.password == kw['password']:
			json['msg'] = '100'
			json['nickName'] = user.nickName
			json['sex'] = user.sex
			json['headPortrait'] = str(user.headPortrait)
			user.token = token()
			json['token'] = user.token
			user.save()
		else:
			json['msg'] = '010'
	finally:
		return json

def Register(**kw):
	'''
	执行注册操作时调用
	1. msg:011 账号已存在.
	2. msg:101 昵称已存在.
	3. msg:110 注册成功.
	'''

	json = {}
	accountExist = False
	nameExist = False
	try:
		accountExist = User.objects.get(account=kw['account'])
	except:
		pass
	if accountExist:
		json['msg'] = '011'
	else:
		try:
			nameExist = User.objects.get(nickName=kw['nickName'])
		except:
			pass
		if nameExist:
			json['msg'] = '101'
		else:
			json['msg'] = '110'
			user = User.objects.create()
			user.account = kw['account']
			user.password = kw['password']
			user.nickName = kw['nickName']
			user.sex = kw['sex']
			user.headPortrait = kw['headPortrait'] if kw['headPortrait'] else user.headPortrait
			user.save()
	return json

def RandomPosition():
	'''
	按权重随机获取下划线、数字、大小写字母.
	1. _(95)
	2. 0-9(48-57)
	3. A-Z(65-90)
	4. a-z(97-122)
	将权重累加(temp)，然后获取一个从0至temp的随机数，从头至尾减去权重的值，
	当值小于等于0时返回下标.
	'''

	weights = [159, 1587, 4127, 4127]
	temp = 0
	x = random.randint(0, sum(weights))
	for i in range(len(weights)):
		x -= weights[i]
		if x <= 0:
			break
	return i

def token():
	'''
	生成一个包含数字、字母以及下划线的32位字符.
	'''

	ret = ''
	'''
	for i in range(32):
		x = RandomPosition()
		if x == 0:
			ret += chr(95)
		elif x ==1:
			ret += chr(random.randint(48, 57))
		elif x == 2:
			ret += chr(random.randint(65, 90))
		else:
			ret += chr(random.randint(97, 122))
	'''
	for i in range(32):
		x = RandomPosition()
		y = int((x+95) + (x*(-48)) + (x*(x-1)*32) + (x*(x-1)*(x-2)*(-8.1)))
		z = int((x+95) + (x*(-39)) + (x*(x-1)*35.5) + (x*(x-1)*(x-2)*(-12)))
		ret += chr(random.randint(y, z))
	return ret

def Posts(nickName, title, text):
	'''
	发帖.
	1. msg: 000 发帖失败.
	2. 发帖成功则跳转至帖子详情页面.
	'''

	response = None
	try:
		user = User.objects.get(nickName=nickName)
	except:
		response = redirect('posts:index')
		response.set_cookie('msg', '000')
	else:
		token = request.COOKIES.get('token', None)
		if token == user.token:
			post = Post.objects.create()
			post.title = title
			post.text = text if text else None
			post.user = user
			post.save()
			response = redirect(reverse('posts:detail', args=(post.id,)))
		else:
			response = redirect('posts:index')
			response.set_cookie('msg', '000')
	finally:
		return response

def MineView(request):
	'''
	个人详情.
	按时间(倒序)排列出个人动态(发帖&评论).
	用户可在该页面编辑自己的帖子、删除帖子/评论.
	'''

	nickName = request.COOKIES.get('nickName', '(null)')
	headPortrait = request.COOKIES.get('headPortrait', None)
	sex = request.COOKIES.get('sex', '(null)')
	info = {
		'nickName': nickName,
		'headPortrait': headPortrait,
		'sex': sex,
	}
	return render(request, 'posts/mine.html', info)

def MyDataView(request, types):
	'''
	个人详情(帖子、评论)分页.
	1. types:1 帖子
	   types:2 评论.
	2. POST得到页码，如果没有则页码为1.
	3. 如果有上一页，则返回上一页的页码，若没有则返回0；下一页同上.
	4. 返回JSON示例 {"types":x, "previous": 0, "next": 2, "title": ["xxx"], "id": [1]}.
	'''

	cla = None
	user = None
	show = 5
	page = request.POST.get('page', 1)
	nickName = request.COOKIES.get('nickName', None)
	try:
		user = User.objects.get(nickName=nickName)
	except:
		raise Http404('阿欧，迷路了！')
	if types == 1:
		cla = Post.objects.filter(user=user).order_by('-editDate')
	elif types == 2:
		cla = Comment.objects.filter(user=user).order_by('-publishDate')
	else:
		raise Http404('阿欧，迷路了！')
	paginator = Paginator(cla, show)
	contacts = paginator.get_page(page)
	ret = {}
	ret['types'] = str(types)
	ret['previous'] = contacts.previous_page_number() if contacts.has_previous() else 0
	ret['next'] = contacts.next_page_number() if contacts.has_next() else 0
	title = []
	pk = []
	date = []
	for item in contacts.object_list:
		try:
			title.append(item.title)
		except:
			title.append(item.text)
		pk.append(item.id)
		try:
			time = item.editDate
		except:
			time = item.publishDate
		date.append(time.strftime('%Y/%m/%d %H:%M:%S'))
	ret['title'] = title
	ret['id'] = pk
	ret['date'] = date
	return JsonResponse(ret)

def RemoveView(request):
	'''
	删帖、删除评论.
	types: 1.删帖 2.删除评论.
	'''

	types = request.POST.get('types', None)
	pk = int(request.POST.get('pk', None))
	token = request.COOKIES.get('token', None)
	nickName = request.COOKIES.get('nickName', None)
	cla = None
	info = {}
	try:
		user = User.objects.get(nickName=nickName)
	except:
		info['info'] = 0
		return JsonResponse(info)
	else:
		if token != user.token:
			info['info'] = 0
			return JsonResponse(info)
		elif types and pk:
			if types == '1':
				cla = Post.objects.filter(pk=pk)
			elif types == '2':
				cla = Comment.objects.filter(pk=pk)
			else:
				raise Http404('阿欧，迷路了！')
			try:
				cla.delete()
			except:
				info['info'] = 0
			else:
				info['info'] = 1
			finally:
				return JsonResponse(info)
		else:
			raise Http404('阿欧，迷路了！')

def EditView(request, pk):
	'''
	编辑帖子.
	'''

	token = request.COOKIES.get('token', None)
	nickName = request.COOKIES.get('nickName', None)
	post = None
	try:
		user = User.objects.get(nickName=nickName)
	except:
		raise Http404('阿欧，迷路了！')
	else:
		if token != user.token:
			raise Http404('登录信息已过期，请重新登录')
		else:
			try:
				post = Post.objects.get(pk=pk)
			except:
				raise Http404('阿欧，迷路了！')
			if request.method == 'POST':
				form = PostForm(request.POST)
				if form.is_valid():
					postForm = form.save(commit=False)
					post.title = postForm.title
					post.text = postForm.text
					post.save()
					return redirect('posts:detail', pk = pk)
			else:
				form = PostForm({'title':post.title, 'text':post.text})
			return render(request, 'posts/edit.html', {'form':form})

def ReplyView(request):
	'''
	回帖.
	'''

	pk = request.POST.get('pk', None)
	text = request.POST.get('text', None)
	token = request.COOKIES.get('token', None)
	nickName = request.COOKIES.get('nickName', None)
	info = {}
	if pk and text and nickName:
		try:
			user = User.objects.get(nickName=nickName)
			post = Post.objects.get(pk=pk)
		except:
			info['info'] = 0
		else:
			if user.token == token:
				Comment.objects.create(text=text, user=user, contentObject=post)
				info['info'] = 1
			else:
				info['info'] = 0
		finally:
			return JsonResponse(info)
	else:
		raise Http404('阿欧，迷路了！')

def CommentView(request):
	'''
	查看所有回帖/评论.
	'''

	pk = request.POST.get('pk', None)
	page = request.POST.get('page', 1)
	show = 5
	text = []
	date = []
	likeNum = []
	user = []
	headPortrait = []
	info = {}
	if pk:
		try:
			post = Post.objects.get(pk=pk)
		except:
			raise Http404('阿欧，迷路了！')
		else:
			comment = post.comment.order_by('-publishDate')
			paginator = Paginator(comment, show)
			pageNum = paginator.page(page)
			for item in pageNum.object_list:
				text.append(item.text)
				date.append(item.publishDate.strftime('%Y/%m/%d %H:%M:%S'))
				likeNum.append(item.likeNum)
				user.append(item.user.nickName)
				headPortrait.append(item.user.headPortrait.url)
			info['text'] = text
			info['date'] = date
			info['likeNum'] = likeNum
			info['user'] = user
			info['headPortrait'] = headPortrait
			info['next'] = pageNum.has_next()
			return JsonResponse(info)
	else:
		raise Http404('阿欧，迷路了！')