# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate_names(self, data):
        errors = []
        if len(data['first_name']) < 1:
            errors.append('First name is a required field')
        if len(data['last_name']) < 1:
            errors.append('Last name is a required field')
        return errors
    
    def validate_email(self, data):
        errors = []
        if len(data['email']) < 1:
            errors.append('E-Mail Address is a required field')
        elif not EMAIL_REGEX.match(data['email']):
            errors.append('E-Mail Address format invalid')
        return errors

    def validate_passwords(self, data):
        errors = []
        if len(data['password']) < 1:
            errors.append('Password field is required')
        elif len(data['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif not data['password'] == data['password_confirm']:
            errors.append('Password must match confirmation')
        return errors

    def validate_add(self, data):
        errors = []
        errors += self.validate_names(data)
        errors += self.validate_email(data)
        errors += self.validate_passwords(data)
        return errors 
   
    def validate_register_form(self, data):
        errors = self.validate_add(data)
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'register'
        }
        if not errors:
            try:
                self.get(email = data['email'])
                errors = ['Email already exists, please sign in']
                validation['success'] = False
                validation['result'] = errors
            except:
                user = self.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    email = data['email'],
                    password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt().encode())
                )
                if user.id == 1:
                    user.privileges = 9
                    user.save()
                validation['success'] = True
                validation['result'] = user
        else:
            validation['result'] = errors
        return validation
    
    def validate_signin_form(self, data):
        errors = []
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'signin'
        }
        errors += self.validate_email(data)
        if len(data['password']) < 1:
            errors.append('Password is required')

        if not errors:
            try:
                user = self.get(email = data['email'])
                if not user.is_active:
                    # "deleted" users will be set to inactive and their signins will be rejected
                    # however all their posts will be preserved in the database
                    raise Exception
                if bcrypt.checkpw(data['password'].encode(), user.password.encode()):
                    validation['success'] = True
                    validation['result'] = user
                else:
                    raise Exception
            except:
                errors = ['Bad Credentials']
                validation['result'] = errors
        else:
            validation['result'] = errors
        return validation
    
    
    
    def validate_info_edit_form(self, data, user_id):
        errors = []
        validation ={
            'success' : False,
            'result'  : None,
            'from'    : 'info'
        }
        errors += self.validate_names(data)
        errors += self.validate_email(data)
        if not errors:
            try:
                user = self.get(id = user_id)
                user.first_name = data['first_name']
                user.last_name = data['last_name']
                user.email = data['email']
                #   Need this statement for admin edit any user
                if 'privileges' in data.keys():
                    user.privileges = data['privileges']
                user.save()
                validation['success'] = True
                validation['result'] = user
            except:
                errors = ['Shit went wrong']
                validation['result'] = errors
        else:
            validation['result'] = errors
        return validation

    def validate_password_edit_form(self, data, user_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'password'
        }
        errors += self.validate_passwords(data)
        if not errors:
            try:
                user = self.get(id = user_id)
                new_password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt().encode())
                user.password = new_password
                user.save()
                validation['success'] = True
                validation['result'] = user
                print 'success'
            except:
                errors = ['Shit went wrong']
                validation['result'] = errors
        else:
            validation['result'] = errors
        return validation

    def validate_description_edit_form(self, data, user_id):
        errors = []
        validation = {
            'success' : False,
            'result'  : None,
            'from'    : 'description'
        }
        if len(data['description']) < 1:
            errors.append('Description is a required field')
        if not errors:
            try:
                user = self.get(id = user_id)
                user.description = data['description']
                user.save()
                validation['success'] = True
                validation['result'] = user
            except:
                errors = ['shit went wrong']
                validation['result'] = errors
        else:
            validation['result'] = errors
        return validation
    
    def admin_validate_add_form(self, data):
        errors = self.validate_add(data)
        validation = {
            'success' : False,
            'result'  : None
        }
        privileges = {
            'admin'  : 9,
            'normal' : 0
        }
        if not data['privileges'] in privileges.keys():
            errors.append('Invalid user privilege choice')
        if not errors:
            try:
                self.get(email = data['email'])
                errors = ['Email already exists, please sign in']
                validation['success'] = False
                validation['result'] = errors
            except:
                user = self.create(
                    first_name = data['first_name'],
                    last_name = data['last_name'],
                    email = data['email'],
                    privileges = privileges[data['privileges']],
                    password = bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt().encode())
                )
                # First user ever entered in the database is an admin
                if user.id == 1:
                    user.privileges = 9
                    user.save()
                validation['success'] = True
                validation['result'] = user
        else:
            validation['result'] = errors
        return validation
        
    # remove does not delete user, it makes them invisible to normal users
    # and unable to login
    # TODO add restore user functionality 
    def remove_user(self, user_id):
        try:
            user = self.get(id = user_id)
            # TODO create super-admin that can perform full deletes on users and admins
            # TODO maybe make it so super-admins can only do full deletes on inactive users
            # TODO thus full deletes will require an admin to remove first, then super-admin to full delete
            # TODO then how would admins be fully deleted?
            if user.privileges == 0:
                user.is_active = False
                user.is_visible = False
                user.save()
            # return values don't do anything here
            return True
        except:
            # Something went very wrong if this statement is reached
            print "Something is broken"
            return False

            

class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
   
    description = models.TextField(default = "Write something about yourself!")

    privileges = models.PositiveSmallIntegerField(default = 0)
    
    is_visible = models.BooleanField(default = True)
    is_active = models.BooleanField(default = True)

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()
