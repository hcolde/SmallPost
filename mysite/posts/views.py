# -*- coding: utf-8 -*-

import random
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
#from django.contrib import messages
from django.conf import settings
from .models import User

def IndexView(request):
	'''
	messages.debug(request, '%s SQL statements were executed.' % count)
	messages.info(request, 'Three credits remain in your account.')
	messages.success(request, 'Profile details updated.')
	messages.warning(request, 'Your account expires in three days.')
	messages.error(request, 'Document deleted.')
	'''
	if request.POST:
		belong = request.POST['belong']
		if belong == 'Login':
			data = Login(account=request.POST['account'], password=request.POST['password1'])
			response = redirect('posts:index')
			response = SetCookies(response, data)
			return response
		elif belong == 'Register':
			data = Register(account=request.POST['account'], 
						password=request.POST['password1'],
						nickName=request.POST['nickName'],
						sex=request.POST['sex'],
						headPortrait=request.FILES.get('headPortrait'))
			response = redirect('posts:index')
			response = SetCookies(response, data)
			return response
		else:
			raise Http404('阿欧，迷路了！')
	return render(request, 'posts/index.html', {'msg': '000'})

def Login(**kw):
	'''
	执行登陆操作时调用
	1. msg:001 不存在该账号.
	2. msg:010 密码错误.
	3. msg:100 账号密码相匹配,登陆成功.
	登录成功后将赋予一个新的token值.
	'''

	json = {'nickName': '', 'sex': '', 'headPortrait': '', 'token':''}
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

	json = {'nickName': '', 'sex': '', 'headPortrait': '', 'token':''}
	isExist = False
	try:
		isExist = User.objects.get(account=kw['account'])
	except:
		pass
	if isExist:
		json['msg'] = '011'
	else:
		try:
			isExist = User.objects.get(nickName=kw['nickName'])
		except:
			pass
		if isExist:
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

def SetCookies(response, data):
	'''
	设置cookie.
	包含msg、昵称、性别、头像、token.
	当注册失败或登录失败时，昵称、性别、头像、token的cookie值为空.
	'''

	response.set_cookie('msg', data['msg'])
	response.set_cookie('nickName', data['nickName'])
	response.set_cookie('sex', data['sex'])
	response.set_cookie('headPortrait', data['headPortrait'])
	response.set_cookie('token', data['token'])
	return response

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