# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse ## need to import reverse when using named routes!
from django.contrib import messages
from .models import *
import bcrypt
from datetime import datetime
from django.db.models import Q

from django.shortcuts import render
print "****************************views"
def index(request):
    request.session.flush()
    return render(request, 'travel_app/index.html')

def home(request):
    userid = request.session['user']
    user =  User.objects.get(id = userid)
    plans = {
            "plans":Plan.objects.all().filter(Q(planned_by = user)| Q(joined_by = user)),
            "allplans":Plan.objects.exclude(Q(planned_by = user)| Q(joined_by = user))
        }
    return render(request,'travel_app/travels.html', plans)

def create(request):
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if (errors): 
            for tag, error in errors.iteritems():
                messages.error(request, error, extra_tags = tag)
            return redirect(reverse('index')) ## reverse for named routes (namespace:urlname)
        else:
            hashpass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hashpass)
            user_id = User.objects.get(username=request.POST['username']).id
            request.session['user'] = user_id
            request.session['username'] = User.objects.get(username=request.POST['username']).name
            return redirect(reverse('home')) 
    else:
        return redirect(reverse('index'))

def login(request):
    username = request.POST["username"]
    if not User.objects.filter(username = username):
        return redirect(reverse('index'))
    username = request.POST["username"]
    user =  User.objects.get(username = username) 
    if user.username == request.POST['username']:
        request.session["username"] = user.name
        request.session["user"] = user.id
        encpass = request.POST['password']
        dbpass= user.password
    if bcrypt.checkpw( encpass.encode(), dbpass.encode()):
        return redirect('home')
    else:
        return redirect(reverse('index'))


def plan_create(request):
    return render(request,'travel_app/plan_create.html')


def new_plan(request):
    if request.method == 'POST':
        errors = Plan.objects.basic_validator(request.POST)
    if (errors): 
        for tag, error in errors.iteritems():
            messages.error(request, error, e 
        return redirect(reverse('plan_create')) ## reverse for named routes (namespace:urlname)
    else:
        Plan.objects.create(destination=request.POST['dest'], description=request.POST['desc'], 
        travel_date_from=request.POST['from'], travel_date_to=request.POST['to'],planned_by = User.objects.get(id = request.session['user']))
        print request.POST['from']
        print datetime.now().strftime("%Y-%m-%d")
        return redirect('home') 
    
def join_plan(request, plan_id):
    user_id = request.session['user']
    user = User.objects.get(id=user_id)
    plan = Plan.objects.get(id=plan_id)
    plan.joined_by.add(user)
    return redirect('home')
def plan( request, plan_id):
    this_plan = Plan.objects.get(id=plan_id)
    user_id = request.session['user']
    context = {
        "plans" : Plan.objects.get(id=plan_id),
        "user" : this_plan.joined_by.all().exclude(id=user_id),
    }
    print context
    return render(request,'travel_app/plan_display.html', context)
