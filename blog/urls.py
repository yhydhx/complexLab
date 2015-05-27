from django.conf.urls import patterns, url

from blog import views
from django.conf import settings
urlpatterns = patterns('',
    url(r'^login\.html$', views.login, name='login'),
    url(r'index',views.dept, name="dept"),
   # url(r'^contact$', views.contact,name ='contact'),
    url(r'^addUser$', views.addUser,name ='addUser'),
    url(r'^loginCertifacate$', views.loginCertifacate,name ='loginCertifacate'),
    url(r'^addUserView$', views.addUserView,name ='addUserView'),
    url(r'^changePasswd$', views.changePasswd,name ='changePasswd'),
    url(r'^logout$', views.logout,name ='logout'),

	url(r'^dept/(?P<method>\w+)/(?P<Oid>\w*)$', views.dept,name ='dept'),
	url(r'^schl/(?P<method>\w+)/(?P<Oid>\w*)$', views.schl,name ='schl'),
    url(r'^lib/(?P<method>\w+)/(?P<Oid>\w*)$', views.lib,name ='lib'),
    url(r'^map/(?P<method>\w+)/(?P<Oid>\w*)$', views.mapGraph,name ='mapGraph'),

    
    url(r'^carMap$', views.carMap,name ='carMap'),
    url(r'^carMapDynamic(?P<map_id>\w+)$', views.carMapDynamic,name ='carMapDynamic'),

    
    url(r'^gethint$', views.gethint,name ='gethint'),
    url(r'^getCarInfo$', views.getCarInfo,name ='getCarInfo'),
    url(r'^getCarTest$', views.getCarTest,name ='getCarTest'),

    #file operation 
    url(r'^addImage$', views.addImage,name ='addImage'),
    url(r'^addImageInfo$', views.addImageInfo,name ='addImageInfo'),
    url(r'^showImgList$', views.showImgList,name ='showImgList'),
    url(r'^deleteImg/(?P<Oid>\w+)$', views.deleteImg,name ='deleteImg'),
    url(r'^test$', views.test,name ='test'),
    url(r'^generate$', views.generate,name ='generate'),
    url(r'^gnetDept$', views.generateDept,name ='generateDept'),
    url(r'^gnetLib$', views.generateLib,name ='generateLib'),
    url(r'^gnetJs$', views.generateJs,name ='generateJs'),
    url(r'^demo$', views.demo,name ='demo'),
    url(r'^parseData$', views.parseData,name ='parseData'),
    (r'^img/(?P<path>.*)','django.views.static.serve',{'document_root':settings.UPLOAD_PATH}), 
    url(r'^saveDataInMongo/(?P<day>\w+)/$', views.saveDataInMongo,name ='saveDataInMongo'),
)
