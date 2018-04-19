from django.contrib import admin
from .models import User, Post, Comment, Reply

def Register(*args):
	for item in args:
		admin.site.register(item)

Register(User, Post, Comment, Reply)