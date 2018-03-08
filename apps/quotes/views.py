# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.messages import get_messages
import re
import bcrypt
from .models import User,Quote


# Create your views here.
def current_user(request):
	return User.objects.get(id = request.session['user_id'])
    
def index(request):
    return render(request,"quotes/index.html")

def users(request,user_id):
    submit_by = User.objects.get(id=user_id)
    context = {
        'quotes' : Quote.objects.filter(submit_by = submit_by),
        'Submitted By': submit_by
    }
    return render(request,"quotes/user.html",context)
def quotes(request):
    users = User.objects.all()
    user = current_user(request)
    
    favorites = Quote.objects.filter(user_favorite = user)
    quotelist = Quote.objects.all().order_by('-id').exclude(id__in=[f.id for f in favorites])
    context = {
        "users": users,
        "user": user,
        "quotes":quotelist,
        "favorites": favorites
    }
    return render(request, "quotes/quotes.html",context)
def quote_add(request):
    # check if POST request
    if request.method == "GET":
        return redirect ('/')
    if request.method == "POST":
        quote = request.POST['quote']
        submit_by = request.session['user_id']
        quote_by = request.POST['quote_by']
        print quote_by
        #Validate entries
        result = Quote.objects.add_quote(quote,submit_by,quote_by)
        if result['status'] == True:
            messages.info(request, result['errors'])
            return redirect ('/quotes')
        messages.error(request,result['errors'],extra_tags="saved")
        return redirect('/quotes')

def add_favorite(request, quote_id):
    user = request.session['user_id']
    Quote.objects.add_favorite(user,quote_id)
    return redirect('/quotes')

def delete_favorite(request,quote_id):
    user = request.session['user_id']
    print user
    Quote.objects.delete_favorite(user,quote_id)
    return redirect('/quotes')

def register(request):
    #check if POST request
    if request.method == "GET":
        return redirect('/')
    #check validation
    user = User.objects.register(request.POST['name'],request.POST['alias'],request.POST['email'],request.POST['DOB'],request.POST['password'],request.POST['confirm_password'])
    if user['status'] == True:
        #Registration validation result = True
        request.session['id'] = user['user'].id
        return redirect ('/')
    else:
        messages.error(request, user['errors'],extra_tags = "register")
        return redirect ('/')

def login(request):
    #check if POST request
    if request.method == "GET":
        return redirect('/')
    else:
		if request.POST.get('alias') == '' or request.POST.get('password') == '':
			messages.error(request, "no")
			return redirect('/')

		user = User.objects.filter(alias=request.POST.get('alias')).first()
		if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
			request.session['user_id']= user.id
			request.session['name']= user.name
			

			return redirect('/quotes')
		else:
			messages.error(request, "no")
			return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    return redirect('quotes/user.html')

