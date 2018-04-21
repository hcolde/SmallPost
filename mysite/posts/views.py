# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, Http404
#from django.contrib import messages
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
			account = request.POST['account']
			password = request.POST['password1']
			data = Login(account=account, password=password)
			response = render(request, 'posts/index.html', data)
			response.set_cookie('nickName', data['nickName'])
			response.set_cookie('sex', data['sex'])
			response.set_cookie('headPortrait', data['headPortrait'])
			response.set_cookie('token', data['token'])
			return response
		elif belong == 'Register':
			return HttpResponse(Login(request))
		else:
			raise Http404('阿欧，迷路了！')
	return render(request, 'posts/index.html', {'msg': '000'})

def Login(**kw):
	'''
	执行登陆操作时调用
	1. msg:001 不存在该账号.
	2. msg:010 密码错误.
	3. msg:100 账号密码相匹配,登陆成功.
	'''

	json = {}
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
			json['token'] = user.token
		else:
			json['msg'] = '010'
	finally:
		return json