# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
# contains decorators logged_in_redirect, not_logged_in_redirect, if_not_POST
import my_utils as _


# used as decorator so logged in users can't go to start page, register page, or login page
logged_in_redirect = _.user_redirect('current_user_id', 'dashboard:dashboard')
# used as decorator so typing in urls without being logged in redirects out
# 
not_logged_in_redirect = _.no_user_redirect('current_user_id', 'dashboard:index')

@logged_in_redirect
def index(request):
    return render(request, 'user_dashboard/index.html')

@logged_in_redirect
def signin(request):
    return render(request, 'user_dashboard/signin.html')

@_.if_not_POST('dashboard:signin')
def signin_process(request):
    validation = User.objects.validate_signin_form(request.POST)
    if validation['success']:
        request.session['current_user_id'] = validation['result'].id
        request.session['current_user_is_admin'] = True if validation['result'].privileges else False
        return redirect('dashboard:dashboard')
    else:
        for error in validation['result']:
            messages.add_message(
            request,
            messages.ERROR,
            error,
            extra_tags = validation['from'])
        return redirect('dashboard:signin')

@logged_in_redirect
def register(request):
    return render(request, 'user_dashboard/register.html')

@_.if_not_POST('dashboard:register')
def register_process(request):
    validation = User.objects.validate_register_form(request.POST)
    if validation['success']:
        request.session['current_user_id'] = validation['result'].id
        request.session['current_user_is_admin'] = True if validation['result'].privileges else False
        return redirect('dashboard:dashboard')
    else:
        for error in validation['result']:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                extra_tags = validation['from'])
        return redirect('dashboard:register')

@not_logged_in_redirect
def signout(request):
    if 'current_user_id' in request.session.keys():
        del request.session['current_user_id']
    if 'current_user_is_admin' in request.session.keys():
        del request.session['current_user_is_admin']
    return render(request, 'user_dashboard/signout.html')

@not_logged_in_redirect
def dashboard(request):
    users = User.objects.all()
    if not request.session['current_user_is_admin']:
        users = users.filter(is_visible=True)
    context = {
        'users' : users
    }
    return render(request, 'user_dashboard/dashboard.html', context)

@not_logged_in_redirect
def users(request):
    return redirect('dashboard:dashboard')

@not_logged_in_redirect
def new_user(request):
    return render(request, 'user_dashboard/new_user.html') 

@_.if_not_POST('dashboard:new_user')
def user_new_process(request):
    validation = User.objects.admin_validate_add_form(request.POST)
    if validation['success']:
        messages.add_message(request, messages.INFO, 'User added successfully')
        return redirect('dashboard:new_user')
    else:
        for error in validation['result']:
            messages.add_message(request, messages.ERROR, error)
        return redirect('dashboard:new_user')

@not_logged_in_redirect
def edit_user(request): 
    context = {
        'user' : User.objects.get(id = request.session['current_user_id'])
        }
    return render(request, 'user_dashboard/edit_user.html', context)

@_.if_not_POST('dashboard:edit_user')
def edit_info_process(request, user_id):
    validation = User.objects.validate_info_edit_form(request.POST, user_id)
    if validation['success']:
        messages.add_message(
            request, 
            messages.INFO,
            'User info updated successfully',
            extra_tags = 'general')
    else:
        for error in validation['result']:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                extra_tags = validation['from'])
    return redirect('dashboard:edit_user')

@_.if_not_POST('dashboard:edit_user')
def edit_password_process(request, user_id):
    validation = User.objects.validate_password_edit_form(request.POST, user_id)
    if validation['success']:
        messages.add_message(
            request,
            messages.INFO,
            'Password updated successfully',
            extra_tags = 'general')
    else:
        for error in validation['result']:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                extra_tags = validation['from'])
    return redirect('dashboard:edit_user')

@_.if_not_POST('dashboard:edit_user')
def edit_description_process(request, user_id):
    validation = User.objects.validate_description_edit_form(request.POST, user_id)
    if validation['success']:
        messages.add_message(
            request,
            messages.INFO,
            'Description updated successfully',
            extra_tags = 'general')
    else:
        for error in validation['result']:
            messages.add_message(
                request,
                messages.ERROR,
                error,
                extra_tags = validation['from'])
    return redirect('dashboard:edit_user')

@_.if_not_POST('dashboard:dashboard')
def admin_remove_user(request, user_id):
    User.objects.remove_user(user_id)
    return redirect('dashboard:dashboard')
@_.if_not_POST('dashboard:dashboard')
def admin_edit_user(request, user_id):
    user = User.objects.get(id = user_id)
    if user.privileges != 0:
        return redirect('dashboard:dashboard')
    context = {
        'user' : user
    }
    return render(request, 'user_dashboard/admin_edit_user.html', context)
