# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ..user_dashboard.models import User

class MessageManager(models.Manager):
    def validate_post_message(self, data, session, user_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'message'
        }
        if len(data['text']) < 1:
            errors.append('Message text is required')
        if not errors:
            try:
                message_to = User.objects.get(id = user_id)
                if message_to.id == session['current_user_id']:
                    raise Exception
                message_from = User.objects.get(id = session['current_user_id'])
                message = self.create(
                    text = data['text'],
                    message_to = message_to,
                    message_from = message_from
                )
                validation['success'] = True
                validation['result'] = message
            except:
                errors =['shit went wrong']
                validation['result'] = errors
        else:
            validation['result'] = errors
        return validation
    def validate_delete_message(self, session, message_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None
        }
        message = self.get(id = message_id)
        # make sure the form action url wasn't tampered with to delete someone elses post
        if message.message_from.id != session['current_user_id']:
            errors.append('hacker')
        if not errors:
            message.delete()
            validation['success'] = True
        return validation


class CommentManager(models.Manager):
    def validate_post_comment(self, data, session, message_id, user_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'comment'
        }
        if len(data['text']) < 1:
            errors.append('Comment text is required')
        if not errors:
            try:
                message = Message.objects.get(id = message_id)
                user = User.objects.get(id = session['current_user_id'])
                comment = self.create(
                    text = data['text'],
                    comment_on = message,
                    comment_by = user
                )
                validation['success'] = True
                validation['result'] = comment
            except:
                pass
        else:
            validation['result'] = errors
        return validation
    
    def validate_delete_comment(self, session, comment_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None
        }
        comment = self.get(id = comment_id)
        if comment.comment_by.id != session['current_user_id']:
            errors.append('Hacker')
        if not errors:
            comment.delete()
            validation['success'] = True
        return validation

class Message(models.Model):
    text = models.TextField()

    message_from = models.ForeignKey(User, related_name = 'messages_sent')
    message_to = models.ForeignKey(User, related_name = 'messages_received')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = MessageManager()

class Comment(models.Model):
    text = models.TextField()

    comment_on = models.ForeignKey(Message, related_name = 'comments')
    comment_by = models.ForeignKey(User, related_name = 'comments')

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    
    objects = CommentManager()
