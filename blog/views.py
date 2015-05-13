# coding: utf-8  
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import render,get_object_or_404,RequestContext
from django.core.urlresolvers import reverse
from django.views import generic
#from dc.models import Poll,Choice,Blog
from django import forms
from complexLab.models import *
import datetime
from django.utils import timezone
from django.conf import settings
import hashlib,time,re,json


'''def index(request):
    latest_poll_list = Poll.objects.all().order_by('-pub_date')[:5]
    context = {'latest_poll_list': 1}
    return render(request, 'dc/index.html', context)
'''

def __checkin__(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

def login(request):
    return render(request, 'blog/login.html' )

def logout(request):
    del request.session['username']
    return HttpResponseRedirect("login.html")

def loginCertifacate(request):
    if request.method == 'POST': 
    # If the form has been submitted...
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        admin = get_object_or_404(Admin, username=username)
        if admin.password == password:
            request.session['username'] = username
            return HttpResponseRedirect('/dc/dept/show')
        else:
            return HttpResponse("密码错误") 
        

def addUserView(request):
    return render(request,"blog/addUserView.html")

def addUser(request):
    md5Encode = hashlib.new("ripemd160")
    username = request.POST.get("username")
    tmpPassword = request.POST.get("password")
    confirmPassword = request.POST.get("password2")
    if tmpPassword != confirmPassword:
        return HttpResponse("两次输入的密码不一致")
    md5Encode.update(tmpPassword)
    password = md5Encode.hexdigest()
    
    veryfyUser = Admin.objects.filter(username = username).all()
    
    try:
        HttpResponse(veryfyUser[0])
    except IndexError,e:
        veryfyUser = None
    if veryfyUser is not None:
        return HttpResponse("This admin is already exits")

    admin = Admin(
        username = username,
        password = password,

        )
    admin.save()
    return render(request,"blog/login.html")
 
def changePasswd(request):
    if request.method == "POST":
        username = request.POST.get("username")
        tmpPassword = request.POST.get("password")
        newPassword = request.POST.get("newPassword")
        md5Encode = hashlib.new("ripemd160")
        md5Encode.update(tmpPassword)
        password = md5Encode.hexdigest()

        user = get_object_or_404(User, username=username)
        if user.password == password:
            newEncode = hashlib.new("ripemd160")
            newEncode.update(newPassword)
            user.password = newEncode.hexdigest()
            user.save()
            del request.session['username']
            return HttpResponseRedirect("login.html")
        else:
            return HttpResponse("密码错误")    
        
    else:
        return render(request,"dc/changePasswd")

def index(request):
    # render(request,'dc/index2.html',{'dept':dept.objects.all()})
    return render(request,'blog/index.html')


########################################################
# this view is about the School 
# contains show schl list , add schl , change schl, 
# delete schl,and add new schl
# News contain a couple of  parts , title content date                 
########################################################

def schl(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addSchl' :
        label = request.POST.get('label')
        weight = request.POST.get("weight")
        schl = School(
            label = label,
            weight = weight,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username'],
            )
        schl.save()
        ##add a link 
        schlLink = SchlLink(
                originUid = schl.id,
                endUid = schl.id,
                originLabel = schl.label,
                endLabel = schl.label,
                weight = schl.weight,
                uploadTime = datetime.datetime.now(),
                uploadUser = request.session['username'],
            )
        schlLink.save()
        #Oid = schl.id
        return HttpResponseRedirect('/dc/schl/show')
    elif method == 'change':
        schl = School.objects.get(id=Oid)
        School.date_format(schl)
        links = SchlLink.objects.filter(originUid = schl.id )
        #return HttpResponse(Oid)
        return render(request,'blog/changeSchl.html',{'schl':schl,'data':links})
    elif method == 'save':
        if request.method == 'POST':
            schl = {'id' : request.POST.get('id'),
                'label' : request.POST.get('label'),
                'weight' : request.POST.get("weight")
                }

        School.objects.filter(id=schl['id']).update(label=schl['label'],weight=schl['weight'])
        #change the self-link
        SchlLink.objects.filter(originUid=schl['id'],endUid = schl['id']).update(weight=schl['weight'])
        #change the other label 
        schlLinks = SchlLink.objects.filter(originUid = schl['id']).update(originLabel=schl['label'])
        schlLinks = SchlLink.objects.filter(endUid = schl['id']).update(endLabel=schl['label'])
        return HttpResponseRedirect('/dc/schl/show')
    elif method == "addSchlLink":
        if request.method == 'POST':
            link = {
                'label' : request.POST.get('endNodeLabel'),
                'weight' : request.POST.get('weight')
                }
        '''
        1. find the otherName of the school  
        2. find the node is exist or not 
        3. find the link is exist or not 
        3. if exist, change the value 
        4. if not , add a link 
        '''
        orinSchl = School.objects.get(id=Oid)
        targetSchl = get_object_or_404(School,label=link['label'])

        linkOT = SchlLink.objects.filter(originUid=orinSchl.id,endUid=targetSchl.id)
        if len(linkOT) == 0:
            newLink = SchlLink(
                originUid = orinSchl.id,
                endUid = targetSchl.id,
                originLabel = orinSchl.label,
                endLabel = targetSchl.label,
                weight = link['weight'],
                uploadTime = datetime.datetime.now(),
                uploadUser = request.session['username'],
                )
            newLink.save()
            newLink = SchlLink(
                endUid = orinSchl.id,
                originUid = targetSchl.id,
                endLabel = orinSchl.label,
                originLabel = targetSchl.label,
                weight = link['weight'],
                uploadTime = datetime.datetime.now(),
                uploadUser = request.session['username'],
                )
            newLink.save()
        else:
            linkOT.update(weight=link['weight'])
            SchlLink.objects.filter(endUid=orinSchl.id,originUid=targetSchl.id).update(weight=link['weight'])
        return HttpResponseRedirect('/dc/schl/show')

    elif method == 'delete':
        School.objects.filter(id=Oid).delete()
        #delete the relate link
        schlLinks = SchlLink.objects.filter(originUid=Oid).delete()
        schlLinks = SchlLink.objects.filter(endUid=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        return render(request,'blog/addSchlView.html')
    elif method == 'show' or method == '':
        allSchl = School.objects.all()
        for element in allSchl:
             School.date_format(element)
        return render(request,'blog/showSchlList.html',{'schl':allSchl})
    else:
        return HttpResponse('没有该方法')



########################################################
# this view is about the Department 
# contains show dept list , add dept , change dept, 
# delete dept,and add new dept
# News contain a couple of  parts , title content date                 
########################################################

def dept(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addDept' :
        image_url = "a" #request.POST.get('image_url')
        collaboration = request.POST.get('collaboration')
        label = request.POST.get('label')
        Total = request.POST.get('Total')
        CollaMap = request.POST.get('CollaMap')
        schlId = request.POST.get("school")
        school = School.objects.get(id=schlId)
        dept = Department(
            image_url = image_url,
            collaboration = collaboration,
            label = label,
            Total = Total,
            school = school.label,
            schlId = schlId,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username'],
            )
        dept.save()
        #add the self-link
        selfLink = DeptLink(
            originUid = dept.id,
            endUid = dept.id,
            originLabel = dept.label,
            endLabel = dept.label,
            weight = dept.Total,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username'],
            )
        selfLink.save()
        return HttpResponseRedirect('/dc/dept/show')
    elif method == 'change':
        dept = Department.objects.get(id=Oid)
        Department.date_format(dept)
        links = DeptLink.objects.filter(originUid = dept.id )
        schools = School.objects.all()    
        return render(request,'blog/changeDept.html',{'dept':dept,'data':links,'schools':schools})
    elif method == 'save':
        if request.method == 'POST':
            dept = {'id' : request.POST.get('id'),
                'collaboration' : request.POST.get('collaboration'),
                'label' : request.POST.get('label'),
                'Total' : request.POST.get('Total'),
                'schoolId' : request.POST.get("school"),
                }
        #change the typical value of the data
        school = get_object_or_404(School,id=dept['schoolId'])
        Department.objects.filter(id=dept['id']).update(collaboration=dept['collaboration'],
                                                        label=dept['label'],
                                                        Total=dept['Total'],
                                                        schlId=dept['schoolId'],
                                                        school=school.label)
        #change the self link
        selfLink = DeptLink.objects.filter(originUid=dept['id'],endUid=dept['id']).update(weight=dept['Total'])
        # If change the Name We should change the link Info
        deptLinks = DeptLink.objects.filter(originUid=dept['id']).update(originLabel = dept['label'])
        deptLinks = DeptLink.objects.filter(endUid=dept['id']).update(endLabel = dept['label'])
        return HttpResponseRedirect('/dc/dept/show')
    elif method == "addDeptLink":
        if request.method == 'POST':
            link = {
                'label' : request.POST.get('endNodeLabel'),
                'weight' : request.POST.get('weight')
                }
        '''
        1. find the otherName of the department  
        2. find the node is exist or not 
        3. find the link is exist or not 
        3. if exist, change the value 
        4. if not , add a link 
        '''
        orinDept = Department.objects.get(id=Oid)
        targetDept = get_object_or_404(Department,label=link['label'])

        linkOT = DeptLink.objects.filter(originUid=orinDept.id,endUid=targetDept.id)
        if len(linkOT) == 0:
            newLink = DeptLink(
                originUid = orinDept.id,
                endUid = targetDept.id,
                originLabel = orinDept.label,
                endLabel = targetDept.label,
                weight = link['weight'],
                uploadTime = datetime.datetime.now(),
                uploadUser = request.session['username'],
                )
            newLink.save()
            newLink = DeptLink(
                endUid = orinDept.id,
                originUid = targetDept.id,
                endLabel = orinDept.label,
                originLabel = targetDept.label,
                weight = link['weight'],
                uploadTime = datetime.datetime.now(),
                uploadUser = request.session['username'],
                )
            newLink.save()
        else:
            linkOT.update(weight=link['weight'])
            DeptLink.objects.filter(endUid=orinDept.id,originUid=targetDept.id).update(weight=link['weight'])
        return HttpResponseRedirect('/dc/dept/show')

    elif method == 'delete':
        #delete the nodes and links
        Department.objects.filter(id=Oid).delete()
        DeptLink.objects.filter(originUid=Oid).delete()
        DeptLink.objects.filter(endUid=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        schools = School.objects.all()
        return render(request,'blog/addDeptView.html',{'schools':schools})
    elif method == 'show' or method == '':
        allDept = Department.objects.all()
        for element in allDept:
             Department.date_format(element)
        return render(request,'blog/showDeptList.html',{'dept':allDept})
    else:
        return HttpResponse('没有该方法')


########################################################
# this view is about the Library 
# contains show lib list , add lib , change lib, 
# delete lib,and add new lib
# News contain a couple of  parts , title content date                 
########################################################

def lib(request,method,Oid):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')

    if method == 'addLib' :
        name = request.POST.get('name')
        label = request.POST.get('label')
        deptId = request.POST.get('dept')
        uniqueID = request.POST.get('uniqueID')
        fullname = request.POST.get('fullname')
        dept = get_object_or_404(Department,id=deptId)
        lib = Library(
            name = name,
            label = label,
            deptId = deptId,
            department = dept.label,
            uniqueID = uniqueID,
            fullname = fullname,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username'],
            )
        lib.save()

        return HttpResponseRedirect('/dc/lib/show')
    elif method == 'change':
        lib = Library.objects.get(id=Oid)
        Library.date_format(lib)
        links = LibLink.objects.filter(originUid = lib.id )
        departments = Department.objects.all()        
        return render(request,'blog/changeLib.html',{'lib':lib,'data':links,'departments':departments})
    elif method == 'save':
        if request.method == 'POST':
            lib = {'id':request.POST.get("id"),
                'name': request.POST.get('name'),
                'label' :request.POST.get('label'),
                'deptId' :request.POST.get('dept'),
                'uniqueID' :request.POST.get('uniqueID'),
                'fullname': request.POST.get('fullname'),
                }
        department =  get_object_or_404(Department,id=lib['deptId'])
        Library.objects.filter(id=lib['id']).update(name=lib['name'],
                                                    label = lib['label'],
                                                    deptId = lib['deptId'],
                                                    department = department.label,
                                                    uniqueID = lib['uniqueID'],
                                                    fullname = lib['fullname'])
        return HttpResponseRedirect('/dc/lib/show')
    elif method == "addLibLink":
        if request.method == 'POST':
            link = {
                    "name" : request.POST.get('endNodeLabel'),
                    "weight" : request.POST.get('weight'),
                }

            '''
            1. find the otherName of the school  
            2. find the node is exist or not 
            3. find the link is exist or not 
            3. if exist, change the value 
            4. if not , add a link 
            '''
            orinLib = Library.objects.get(id=Oid)
            
            targetLib = get_object_or_404(Library,name=link['name'])

            linkOT = LibLink.objects.filter(originUid=orinLib.id,endUid=targetLib.id)
            if len(linkOT) == 0:
                newLink = LibLink(
                    originUid = orinLib.id,
                    endUid = targetLib.id,
                    originLabel = orinLib.name,
                    endLabel = targetLib.name,
                    weight = link['weight'],
                    uploadTime = datetime.datetime.now(),
                    uploadUser = request.session['username'],
                    )
                newLink.save()
                newLink = LibLink(
                    endUid = orinLib.id,
                    originUid = targetLib.id,
                    endLabel = orinLib.name,
                    originLabel = targetLib.name,
                    weight = link['weight'],
                    uploadTime = datetime.datetime.now(),
                    uploadUser = request.session['username'],
                    )
                newLink.save()
            else:
                linkOT.update(weight=link['weight'])
                LibLink.objects.filter(endUid=orinLib.id,originUid=targetLib.id).update(weight=link['weight'])
            return HttpResponseRedirect('/dc/lib/show')
        else:
            return HttpResponse("A error")

    elif method == 'delete':
        #delete the nodes and links
        Library.objects.filter(id=Oid).delete()
        LibLink.objects.filter(originUid=Oid).delete()
        LibLink.objects.filter(endUid=Oid).delete()
        return HttpResponseRedirect('../show')
    elif method == 'add':
        departments = Department.objects.all() 
        return render(request,'blog/addLibView.html',{'departments':departments})
    elif method == 'show' or method == '':
        allLib = Library.objects.all()
        for element in allLib:
             Library.date_format(element)
        return render(request,'blog/showLibList.html',{'lib':allLib})
    else:
        return HttpResponse('没有该方法')


def mapGraph(request,method,Oid):
    return render(request,"blog/map.html")

##################################################################################################
#  file operation 
#   about image and video
##################################################################################################

def addImage(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')   
    if request.method == "POST":
        return HttpResponse(1)
    return render(request,'blog/addImage.html')

def addImageInfo(request):
    if request.method == "POST":
        des_origin_path = settings.UPLOAD_PATH+'/images/'+request.POST.get('title')
        des_origin_f = open(des_origin_path, "ab") 
        tmpImg = request.FILES['img']
        for chunk in tmpImg.chunks():  
            des_origin_f.write(chunk)   
        des_origin_f.close() 
        img = Image(
            title = request.POST.get('title'),
            location = des_origin_path,
            uploadUser = request.session['username'],
            )
        img.save()
        return HttpResponseRedirect('showImgList')
    return HttpResponse('allowed only via POST')

def showImgList(request):
    try:
        request.session['username']
    except KeyError,e:
        return HttpResponseRedirect('login.html')    
    return render(request,'dc/showImgList.html',{'image':Image.objects.all() })

def deleteImg(request,Oid):
    Image.objects.filter(id=Oid).delete()
    return HttpResponseRedirect('../showImgList')

def test(request):
    return   render(request,"blog/ust.html")

def generateSchl():
    outputFile = file(settings.STATIC_ROOT+'blog/js/schl.json','w')
    #write the head
    outputFile.write("{\n")
    outputFile.write("\t\"directed\": false,\n")
    outputFile.write("\t\"graph\": [],\n")
    #end the head

    indexNode = {}
    nodeCount = 0
    nodes = []
    links = []
    allSchool = School.objects.order_by('label')
    for element in allSchool:
        indexNode[element.id] = {}
        indexNode[element.id]['index'] = nodeCount
        indexNode[element.id]['label'] = element.label
        tmpNode = {}
        tmpNode['id'] = nodeCount
        tmpNode['label'] = str(element.label)
        nodes.append(tmpNode)
        nodeCount += 1
    allLink = SchlLink.objects.all()
    for element in allLink:
        tmpLink = {}
        tmpLink['source'] = indexNode[element.originUid]['index']
        tmpLink['target'] = indexNode[element.endUid]['index']  
        tmpLink['weight'] = element.weight
        if tmpLink['source'] <= tmpLink['target']:
            links.append(tmpLink)
    #print Nodes 
    outputFile.write("\t\"nodes\": [\n")
    count = 1
    nodeLen = len(nodes)    
    for element in nodes:
        outputFile.write("\t\t{\n")
        outputFile.write("\t\t\t\"id\":"+str(element['id'])+",\n")
        outputFile.write("\t\t\t\"label\":\""+str(element['label'])+"\"\n")
        if count == nodeLen:
            outputFile.write("\t\t}\n")
        else:
            outputFile.write("\t\t},\n")
            count += 1
    outputFile.write("\t],\n")
    #end print nodes

    #print links 
    outputFile.write("\t\"links\": [\n")
    count = 1
    linkLen = len(links)
    for element in links:
    
        outputFile.write("\t\t{\n")
        outputFile.write("\t\t\t\"source\":"+str(element['source'])+",\n")
        outputFile.write("\t\t\t\"target\":"+str(element['target'])+",\n")
        outputFile.write("\t\t\t\"weight\":"+str(element['weight'])+"\n")
        
        if count == linkLen:
            outputFile.write("\t\t}\n")
        else:
            outputFile.write("\t\t},\n")
        count += 1

    outputFile.write("\t],\n")
    #end print links

    #print button
    outputFile.write("\t\"multigraph\": false\n}\n")
    

    return HttpResponse("success")

def generateDept():

    indexNode = {}
    nodeCount = 0
    nodes = []
    links = []
    allDepartment = Department.objects.all()
    for element in allDepartment:
        indexNode[element.id] = {}
        indexNode[element.id]['index'] = nodeCount

        tmpNode = {}
        tmpNode['index'] = nodeCount
        tmpNode['url'] = element.image_url
        tmpNode['label'] = element.label
        tmpNode['Total'] = element.Total
        tmpNode['collaboration'] = element.collaboration
        tmpNode['CollaMap'] = {}
        nodes.append(tmpNode)
        nodeCount += 1

    allLink = DeptLink.objects.all()
    for element in allLink:
        tmpLink = {}
        tmpLink['source'] = indexNode[element.originUid]['index']
        tmpLink['target'] = indexNode[element.endUid]['index']  
        tmpLink['weight'] = element.weight
        indexN = indexNode[element.originUid]['index']
        if tmpLink['source'] != tmpLink['target']:
            nodes[indexN]['CollaMap'][tmpLink['target']] = tmpLink['weight']
        if tmpLink['source'] <= tmpLink['target']:
            links.append(tmpLink)
    

    """
    write the graph begin 
    """
    outputFile = file(settings.STATIC_ROOT+'blog/js/dept.json','w')
    #write the head
    outputFile.write("{\n")
    outputFile.write("\t\"directed\": false,\n")
    outputFile.write("\t\"graph\": [],\n")
    #end the head

    #print Nodes 
    outputFile.write("\t\"nodes\": [\n")
    count = 1
    nodeLen = len(indexNode)
    for element in nodes:
        outputFile.write("\t\t{\n")
        outputFile.write("\t\t\t\"url\":\""+str(element['url'])+"\",\n")
        outputFile.write("\t\t\t\"collaboration\":"+str(element['collaboration'])+",\n")
        outputFile.write("\t\t\t\"Total\":"+str(element['Total'])+",\n")
        outputFile.write("\t\t\t\"label\":\""+str(element['label'])+"\",\n")
        outputFile.write("\t\t\t\"id\":"+str(element['index'])+",\n")
        outputFile.write("\t\t\t\"CollaMap\":{\n")
        cCount = 1
        mapLen = len(element['CollaMap'])
        for tNode in element['CollaMap']:
            wt = element['CollaMap'][tNode]

            if cCount == mapLen:
                outputFile.write("\t\t\t\t\""+str(tNode)+"\":"+str(wt)+"\n")
            else:
                outputFile.write("\t\t\t\t\""+str(tNode)+"\":"+str(wt)+",\n")
            cCount += 1
        outputFile.write("\t\t\t}\n")
        if count == nodeLen:
            outputFile.write("\t\t}\n")
        else:
            outputFile.write("\t\t},\n")
            count += 1
    outputFile.write("\t],\n")
    #end print nodes

    #print links 
    outputFile.write("\t\"links\": [\n")
    count = 1
    linkLen = len(links)
    for element in links:
        if element['source'] <= element['target']:
            outputFile.write("\t\t{\n")
            outputFile.write("\t\t\t\"source\":"+str(element['source'])+",\n")
            outputFile.write("\t\t\t\"target\":"+str(element['target'])+",\n")
            outputFile.write("\t\t\t\"weight\":"+str(element['weight'])+"\n")
            if count == linkLen:
                outputFile.write("\t\t}\n")
            else:
                outputFile.write("\t\t},\n")
                count += 1
        else:
            count += 1
    outputFile.write("\t],\n")
    #end print links

    #print button
    outputFile.write("\t\"multigraph\": false\n}\n")
    

    return HttpResponse("success")




def generateLib():

    indexNode = {}
    nodeCount = 0
    nodes = []
    links = []
    allLibrary = Library.objects.all()
    for element in allLibrary:
        indexNode[element.id] = {}
        indexNode[element.id]['index'] = nodeCount
        tmpNode  = {}
        tmpNode['index'] = nodeCount
        tmpNode['name'] = element.name
        tmpNode['label'] = element.label
        tmpNode['uniqueID'] = element.uniqueID
        tmpNode['dept'] = element.department
        tmpNode['fullname'] = element.fullname
        nodes.append(tmpNode)
        nodeCount += 1

    allLink = LibLink.objects.all()
    for element in allLink:
        tmpLink = {}
        tmpLink['source'] = indexNode[element.originUid]['index']
        tmpLink['target'] = indexNode[element.endUid]['index']  
        tmpLink['weight'] = element.weight
        if tmpLink['source'] <= tmpLink['target']:
            links.append(tmpLink)
    

    """
    write the graph begin 
    """
    outputFile = file(settings.STATIC_ROOT+'blog/js/lib.json','w')
    #write the head
    outputFile.write("{\n")
    outputFile.write("\t\"directed\": false,\n")
    outputFile.write("\t\"graph\": [],\n")
    #end the head

    #print Nodes 
    outputFile.write("\t\"nodes\": [\n")
    count = 1
    nodeLen = len(indexNode)
    for element in nodes:
        outputFile.write("\t\t{\n")
        outputFile.write("\t\t\t\"name\":\""+str(element['name'])+"\",\n")
        outputFile.write("\t\t\t\"label\":\""+str(element['label'])+"\",\n")
        outputFile.write("\t\t\t\"dept\":\""+str(element['dept'])+"\",\n")
        outputFile.write("\t\t\t\"uniqueID\":\""+str(element['uniqueID'])+"\",\n")
        outputFile.write("\t\t\t\"fullname\":\""+str(element['fullname'])+"\",\n")
        outputFile.write("\t\t\t\"id\":"+str(element['index'])+"\n")
        if count == nodeLen:
            outputFile.write("\t\t}\n")
        else:
            outputFile.write("\t\t},\n")
            count += 1
    outputFile.write("\t],\n")
    #end print nodes

    #print links 
    outputFile.write("\t\"links\": [\n")
    count = 1
    linkLen = len(links)
    for element in links:
        if element['source'] <= element['target']:
            outputFile.write("\t\t{\n")
            outputFile.write("\t\t\t\"source\":"+str(element['source'])+",\n")
            outputFile.write("\t\t\t\"target\":"+str(element['target'])+",\n")
            outputFile.write("\t\t\t\"weight\":"+str(element['weight'])+"\n")
            if count == linkLen:
                outputFile.write("\t\t}\n")
            else:
                outputFile.write("\t\t},\n")
                count += 1
        else:
            count += 1
    outputFile.write("\t],\n")
    #end print links

    #print button
    outputFile.write("\t\"multigraph\": false\n}\n")
    

    return HttpResponse("success")


def generateJs():
    schools = School.objects.all()
    departments = Department.objects.all()
    outputFile = file(settings.STATIC_ROOT+'blog/js/dept.js','w')
    school = []
    schoolIndex = {}
    count = 0
    for element in schools:
        schoolIndex[element.id] = {}
        schoolIndex[element.id]['index'] = count
        tmpSchool = {}
        tmpSchool['index'] = count
        tmpSchool['label'] = element.label
        tmpSchool['dept'] = []
        school.append(tmpSchool)
        count += 1

    for element in departments :
        schoolI = schoolIndex[element.schlId]['index']
        school[schoolI]['dept'].append(element.label)

    '''  print school '''
    outputFile.write("var school={\n")
    for element in school:
        outputFile.write("\t\""+element['label']+"\":"+str(element['index'])+",\n")
    outputFile.write("};\n")

    """" print dept """
    outputFile.write("var dept={\n")
    for element in school:
        for dept in element['dept']:
            outputFile.write("\t\""+dept+"\":"+str(element['index'])+",\n")
    outputFile.write("};\n")
 

    """" print deptName """
    outputFile.write("var deptNames=[\n")
    for element in school:
        for dept in element['dept']:
            outputFile.write("\t\""+dept+"\",\n")
    outputFile.write("];\n")
 

    """" print Index """
    outputFile.write("var deptIndex={\n")
    deptCount = 0
    for element in school:
        for dept in element['dept']:
            outputFile.write("\t\""+dept+"\":"+str(deptCount)+",\n")
            deptCount += 1
    outputFile.write("};\n")

    """" print deptIndexS """
    outputFile.write("var deptIndexS={\n")
    
    for element in school:
        deptCount = 0
        for dept in element['dept']:
            outputFile.write("\t\""+dept+"\":"+str(deptCount)+",\n")
            deptCount += 1
    outputFile.write("};\n")

    """print button"""
    outputFile.write("var schoolList=[")
    schCount = 1
    for element in school:
        outputFile.write("\""+element['label']+"\"")
        if not schCount == len(school):
            schCount += 1
            outputFile.write(",")
    outputFile.write("];\n")
    outputFile.write("var schoolOffset = [")
    count = 1
    addNum = 0
    schlLen = len(school) 
    schoolOffset = {}
    for data in school:
        schoolOffset[data['index']] = len(data['dept'])

    for i in range(len(schoolOffset)):
        outputFile.write(""+str(addNum)+",")    
        addNum += schoolOffset[i]
    outputFile.write(str(addNum)+"];\n")
    outputFile.write("function getSchoolName(departmentName){    return schoolList[dept[departmentName]];}\nfunction getSchoolIndex(departmentName) {    return dept[departmentName];}")

    return HttpResponse("success")

def generate(request):
    generateLib()
    generateJs()
    generateDept()
    generateSchl()
    return HttpResponse("hello")

def demo(request):
    return render(request,"blog/demo.html")


def parseData(request):
    natureFile = settings.STATIC_ROOT+"countrys/Nature.txt"
    pnasFile = settings.STATIC_ROOT+"countrys/Pnas.txt"
    PRLFile = settings.STATIC_ROOT+"countrys/PRL.txt"
    ScienceFile = settings.STATIC_ROOT+"countrys/Science.txt"

    

    schoolCollection = {}
    for i in range(4):
        school = School(
            label = str(i+2007),
            weight = 200,
            uploadTime = datetime.datetime.now(),
            uploadUser = request.session['username']
        )
        school.save()
        schoolCollection[str(i+2007)] =school.id

    print schoolCollection
    saveNodesAndLinks(natureFile,'nature',schoolCollection)
    saveNodesAndLinks(pnasFile,'pnas',schoolCollection)    
    saveNodesAndLinks(PRLFile,'PRL',schoolCollection)
    saveNodesAndLinks(ScienceFile,'Science',schoolCollection)
    return HttpResponse("uploadSuccess!")

def saveNodesAndLinks(fileName,journalName,schoolCollection):
    Connection = {}
    sumPaperNum = {}
    sumCoPaperNum = {}
    countrySum = {}

    for element in file(fileName):
        tmpCountryList = {}
        Info = element.strip().split("\t")
        countryName = Info[0]
        year = int(Info[1])
        if year <= 2006 or year >=2011:
            continue
        year = str(year)
        if not Connection.has_key(year):
            Connection[year] = {}

        if not countrySum.has_key(year):
            countrySum[year] = {}

        countries = countryName.split("@")
        for eachCountry in countries:
            if eachCountry != "":
                if tmpCountryList.has_key(eachCountry):
                    tmpCountryList[eachCountry] += 1
                else:
                    tmpCountryList[eachCountry] = 1

        

        if len(tmpCountryList) != 1:
            if sumCoPaperNum.has_key(year):
                sumCoPaperNum[year] += 1
            else:
                sumCoPaperNum[year] = 1.0
               
            tmpSavedList = []
            #print tmpCountryList
            for firstCountry in tmpCountryList:
                tmpSavedList.append(firstCountry)
                for secondCountry in tmpCountryList:
                    #time.sleep(10)
                    #print secondCountry,secondCountry in tmpSavedList

                    if secondCountry in tmpSavedList:
                        continue
                    else:

                        #print firstCountry,secondCountry
                        if Connection[year].has_key((firstCountry,secondCountry)):
                            Connection[year][(secondCountry,firstCountry)] += 1
                            Connection[year][(firstCountry,secondCountry)] += 1
                        
                        else:
                            Connection[year][(firstCountry,secondCountry)] = 1
                            Connection[year][(secondCountry,firstCountry)] = 1
            
        if sumPaperNum.has_key(year):
            sumPaperNum[year] += 1
        else:
            sumPaperNum[year] = 1.0

        for eachCon in tmpCountryList:
            if countrySum[year].has_key(eachCon):
                countrySum[year][eachCon] += tmpCountryList[eachCon]
            else:
                countrySum[year][eachCon] = tmpCountryList[eachCon]
    #print countrySum   

    #print Connection

    """
        save data to the database
    """


    #create the jounal  and journalName is 
    for element in Connection:
        dept = Department(
            image_url = journalName,
            collaboration = len(Connection[element]),
            label = element+"_"+journalName,
            Total = len(Connection[element]),
            schlId = schoolCollection[element],
            school = element,
            uploadTime = timezone.now(),
            uploadUser = "dai"
        )
        dept.save()
        '''
            save the country in every journal
        '''
        libName2Id = {}
        for eachCon in countrySum[element]:
            if countrySum[element][eachCon] < 10:
                continue
            lib = Library(
                name = eachCon+"_"+journalName+"_"+element,
                label = eachCon+"_"+journalName+"_"+element,
                uniqueID = eachCon,
                fullname = eachCon+"_"+journalName+"_"+element,
                deptId = dept.id,
                department = dept.label,
                uploadTime = timezone.now(),
                uploadUser = "dai"
            )
            lib.save()
            libName2Id[lib.uniqueID] = lib.id
        '''
            save the links between every two countries
        '''
        for eachLink in Connection[element]:
            if countrySum[element][eachLink[0]] < 10 or countrySum[element][eachLink[1]] < 10:
                continue

            liblink = LibLink(
                originUid = libName2Id[eachLink[0]],
                endUid = libName2Id[eachLink[1]],
                originLabel = eachLink[0],
                endLabel = eachLink[1],
                weight = Connection[element][eachLink],
                uploadTime = timezone.now(),
                uploadUser = "dai"
            )
            liblink.save()


    """
        save the link between journal 
    """
    isFirst = 1
    for element in Connection:

        presentProperty = int(100*sumCoPaperNum[element]/sumPaperNum[element])
        #print presentProperty
        presentObject = Department.objects.get(label=element+"_"+journalName)
        singleYear = Department.objects.filter(label=element).update(Total = presentProperty)
        if isFirst == 0 :
            #print presentObject,lastObject
            if lastProperty > presentProperty:
                weight = 200
            else:
                weight = 20

            deptLink = DeptLink(
                originUid = lastObject.id,
                endUid = presentObject.id,
                originLabel = lastObject.label,
                endLabel = presentObject.label,
                weight = weight,
                uploadTime = timezone.now(),
                uploadUser = "dai"
            )
            deptLink.save()
        else:
            isFirst = 0
        
        lastProperty = presentProperty
        lastObject = presentObject

def saveDataInMongo(request,day):
    if len(day) == 1:
        day = '0'+str(day)
    filename = "/home/jupiter/Documents/x201408"+str(day)+".txt"
    process(filename)
    print "file "+filename + " complete"
    print "------------------------------"

    return HttpResponse("finished");
def process(filename):
    try:
        originFile = file(filename)
    except:
        print filename+" could not open"
        return
    
    count = 0
    for element in originFile:
        count += 1
        if count % 1000000 == 0:
            print filename,":   ",count*100.0/75000000,'%'
        if element[0] != ",":
            Info = element.split(",")
            try:
                cTime = datetime.datetime.strptime(Info[1],'%Y/%m/%d %H:%M:%S')
            except:
                continue

            trans = Trans(
                    label = Info[0],
                    cTime  = cTime,
                    longitude = Info[2],
                    latitude = Info[3],
                    isService = Info[4],
                )
            trans.save()

def carMap(request):
    return render(request,'blog/carMap.html')

def gethint(request):
    hint = request.GET.get("q")
    labels = Label.objects.filter(label__startswith=hint)[0:10]
    cars  = []
    for element in labels:
        if not element.label in cars:
            cars.append(element.label)

    return HttpResponse(",".join(cars))

def getCarInfo(request):
    label ="A-TA019"#request.GET.get("label")
    Info = {}
    Info['data'] = {}
    carInfo = Trans.objects.filter(label=label)
    for element in carInfo:
        ctime = element.cTime.strftime("%Y-%m-%d")
        
        if Info['data'].has_key(ctime):
            Info['data'][ctime].append([element.longitude,element.latitude])
        else:
            Info['data'][ctime] = [[element.longitude,element.latitude]]
    Info['date'] = []
    for element in Info['data']:
        Info['date'].append(element)
    Info['date'] = sorted(Info['date'])
    
    return HttpResponse(json.dumps(Info))