from django.conf.urls import patterns, include, url

from django.contrib import admin
from lab.views import *


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'complexLab.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r"",include('lab.urls')),
    url(r"^dc/",include('blog.urls'))
)
