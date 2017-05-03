# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import Message, Comment 
from ..user_dashboard.models import User
from ..user_dashboard import my_utils as _
def index(request):
    return redirect('messages:show_user', user_id = request.session['current_user_id'])

def show_user(request, user_id):
    user = User.objects.get(id = user_id)
    messages = user.messages_received.all().order_by('-created_at')
    threads = [ (message, message.comments.all().order_by('created_at')) for message in messages ]
    context = {
        'user' : user,
        'threads': threads
    }
    return render(request, 'user_messages/show_user.html', context)

@_.if_not_POST('messages:index')
def post_message(request, user_id):
    validation = Message.objects.validate_post_message(request.POST, request.session, user_id)
    if validation['success']:
        return redirect('messages:show_user', user_id = user_id)

@_.if_not_POST('messages:index')
def delete_message(request, user_id, message_id):
    validation = Message.objects.validate_delete_message(request.session, message_id)
    if validation['success']:
        return redirect('messages:show_user', user_id = user_id)

@_.if_not_POST('messages:index')
def post_comment(request, message_id, user_id):
    validation = Comment.objects.validate_post_comment(request.POST, request.session, message_id, user_id)
    if validation['success']:
        return redirect('messages:show_user', user_id = user_id)

@_.if_not_POST('messages:index')
def delete_comment(request, user_id, comment_id):
    validation = Comment.objects.validate_delete_comment(request.session, comment_id)
    if validation['success']:
        return redirect('messages:show_user', user_id = user_id)
