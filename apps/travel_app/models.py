# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.db import models
 

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['name']) < 2 or not postData['name']:
            errors["name"] = "Name should be more than one alphabetical character."
        if len(postData['username']) < 2 or not postData['username']:
            errors["username"] = "Username should be more than one alphabetical character."
        if len(postData['password']) < 8 or not postData['password']:
            errors["password"] = "password should be more than 8 alphabetical character."
        if postData['password'] != postData['passconf']:
            errors["passwordmatch"] = "Passwords do not match!."
        return errors
    # def login_validator(self,postdata):

class PlanManager(models.Manager):
    def basic_validator(self, postData):
        present = datetime.now().strftime("%Y-%m-%d")
        errors = {}
        if len(postData['dest']) < 1 or not postData['dest']:
            errors["dest"] = "destination should not be blank"
        if len(postData['desc']) < 1 or not postData['desc']:
            errors["desc"] = "Description should not be blank."
        if len(postData['from']) < 1 or not postData['from']:
            errors["from"] = "Travel From date cannot be blank"
        if len(postData['to']) < 1 or not postData['to']:
            errors["to"] = "travel to date should not be empty"
        if present > postData['from']:
            errors['pastfrom'] = 'travel from date cannot be before today'
        if present > postData['to']:
            errors['pastfrom'] = 'travel to date cannot be before today'
        if postData['to'] < postData['from']:
            errors['tobeforefrom'] = 'Travel to date must be after  travel from date'
        return errors

class User(models.Model):
    name= models.CharField(max_length = 255)
    username = models.CharField(max_length = 255, unique=True)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return "<User: {} {}".format(self.name, self.id)
class Plan(models.Model):
    destination = models.CharField(max_length = 255)
    description = models.CharField(max_length = 255)
    travel_date_from = models.DateField()
    travel_date_to = models.DateField()
    planned_by = models.ForeignKey(User, related_name = "plans")
    joined_by = models.ManyToManyField(User, related_name = 'joins')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = PlanManager()
    def __repr__(self):
        return "<Plan: {} {}".format(self.destination, self.travel_date_from)