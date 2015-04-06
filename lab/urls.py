from django.conf.urls import patterns, url

from lab import views

urlpatterns = patterns('',
    url(r'^index$', views.index, name='index'),
    
    #url(r'^test$', views.getClientIp, name='getClientIp')
)