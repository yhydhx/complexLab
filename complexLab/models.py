import datetime
from django_mongodb_engine.contrib import MongoDBManager
from django.db import models
from django.utils import timezone
from djangotoolbox.fields import  ListField
from django import forms


class School(models.Model):
    label = models.CharField(max_length = 100)
    weight = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class SchlLink(models.Model):
    originUid = models.CharField(max_length=100)
    endUid = models.CharField(max_length=100)
    originLabel = models.CharField(max_length=100)
    endLabel = models.CharField(max_length=100)
    weight = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class Department(models.Model):
    image_url = models.CharField(max_length=100)
    collaboration = models.IntegerField()
    label = models.CharField()
    Total = models.IntegerField()
    schlId = models.CharField(max_length=100)
    school = models.CharField(max_length= 100)
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
    	self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class DeptLink(models.Model):
    originUid = models.CharField(max_length=100)
    endUid = models.CharField(max_length=100)
    originLabel = models.CharField(max_length=100)
    endLabel = models.CharField(max_length=100)
    weight = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")


class Library(models.Model):
    name = models.CharField(max_length=100)
    label = models.CharField(max_length = 100)
    uniqueID = models.CharField(max_length = 100)
    fullname = models.CharField(max_length = 100)
    deptId = models.CharField(max_length=100)
    department = models.CharField(max_length= 100)
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class LibLink(models.Model):
    originUid = models.CharField(max_length=100)
    endUid = models.CharField(max_length=100)
    originLabel = models.CharField(max_length=100)
    endLabel = models.CharField(max_length=100)
    weight = models.IntegerField()
    uploadTime = models.DateTimeField()
    uploadUser = models.CharField(max_length = 100)
    def date_format(self):
        self.uploadTime = self.uploadTime.strftime("%Y-%m-%d")

class User(models.Model):
    name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 100)
    user_flag = models.SmallIntegerField()

class Admin(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)