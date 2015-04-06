from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
from django import forms
from complexLab.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib, time, random


def index(request):
	return HttpResponse("Helloworld")

