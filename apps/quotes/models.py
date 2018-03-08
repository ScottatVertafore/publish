# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re
import bcrypt


emailRegex = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')

# Create your models here.
class UserManager(models.Manager):
    def register(self,name,alias,email,DOB,password,confirm_password):
        #validate
        validation = self.validate(name,alias,email,DOB,password,confirm_password)
        #result: result = {'status': True,'errors':"validation works"}
        if validation['status']:
            hash_pass = bcrypt.hashpw(password.encode(),bcrypt.gensalt())
            user = self.create(name=name,alias=alias,email=email,DOB=DOB,password=hash_pass)
            validation = {'status': validation['status'],'user':user}
            return validation
        return validation

    def validate(self,name,alias,email,DOB,password,confirm_password):
        errors = []
        result = {}
            #validate name
        if name == '':
            msg = "You have to have a name"
            errors.append(msg)
            result = {'status': False, 'errors' : errors[0]}
            return result
        elif name.isalpha() == True:
            msg = "Letters only please"
            errors.append(msg)
            result = {'status': False, 'errors' : errors[0]}
            return result
        elif len(name) <5:
            msg = "We need your full name"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
            #validate alias
        if alias == '':
            msg = "You have to have an alias"
            errors.append(msg)
            result = {'status': False, 'errors' : errors[0]}
            return result
        elif len(alias) <2:
            msg = "User your initials or a nickname"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
            #validate DOB
        if DOB == '':
            msg = "Everyone has a birthday"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
            #validate email
        if email == '':
            msg = "Everyone has an email"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
        elif not emailRegex.match(email):
            msg = "Not a valid email"
            errors.append(msg)
            result = {'status' : True, 'errors' : errors[0]}
            return result
        elif len(self.filter(email=email)) > 0:
            msg = "Email already exists in system"
            errors.append(msg)
            result = {'status' : False, 'errors' : errors[0]}
            return result
            #validate password
        if password == '':
            msg = "Gots to have a password, Dude!"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
        elif len(password)<2:
            msg = "Password must be more than 2 characters"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
        elif confirm_password != password:
            msg = "Passwords don't match"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
        else:
            result =  {'status':True, 'errors':"You Valid"}
            return result

    def valid_login(self,alias,password):
        errors = []
        try:
            valid_user = self.get(alias = alias)
            
            if bcrypt.checkpw(password.encode(),valid_user.password.encode()):
                result = {'status':True, 'valid_user': valid_user}
                return result
            else:
                msg = "Guess again......"
                errors.append(msg)
                result = {'status':False, 'errors':errors[0]}
                return result
        except:
            msg = "Please register before trying to login"
            errors.append(msg)
            result = {'status':False, 'errors':errors[0]}
            return result
class Quote_Manager(models.Manager):
    def add_quote(self,quote,submit_by,quote_by):
        errors = []
        if len(quote)<15:
            msg = "It has to be a real quote!"
            result = {'status':False, 'errors':errors[0]}
            return result
        elif len(quote_by)<5:
            msg = "Quote has to be by a real person!"
            result = {'status':False, 'errors':errors[0]}
            return result
        submit_by = User.objects.get(id=submit_by)
        self.create(quote=quote,quote_by=quote_by,submit_by=submit_by)
        msg = "That's a good one!"
        errors.append(msg)
        result =  {'status':True, 'errors': errors[0]}
        return result
    def add_favorite(self,user_id,quote_id):
        user = User.objects.get(id=user_id)
        favorite = Quote.objects.get(id=quote_id)
        favorite.user_favorite.add(user)
        result = {'status':True}
        return result
    def delete_favorite(self,user_id,quote_id):
        user = User.objects.get(id=user_id)
        favorite = Quote.objects.get(id=quote_id)
        favorite.user_favorite.remove(user)

class User(models.Model):
    alias = models.CharField(max_length=255, null=True)
    name = models.CharField(max_length=255, null=True)
    DOB = models.CharField(max_length=25,null = True)
    email = models.CharField(max_length=255, null=True)
    password = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    def __str__(self):
        return self.name


class Quote(models.Model):
    quote_by = models.CharField(max_length=255, null=True)
    quote = models.TextField(max_length=1000, null=True)
    submit_by = models.ForeignKey(User,related_name="quotes")
    user_favorite = models.ManyToManyField(User,related_name = "favorite_quotes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = Quote_Manager()
