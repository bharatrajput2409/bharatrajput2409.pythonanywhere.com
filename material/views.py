from django.shortcuts import render
from django.contrib.auth.models import User,auth
from .models import subjectmaterial,materialsolution,solutioncomment,question,tag_in_question,questioncomments,subjectcomment
from django.http import HttpResponseRedirect,HttpResponse
import datetime
from django.core.files.storage import FileSystemStorage
import json
from django.http import JsonResponse
# Create your views here.
def courses(request):

    return render(request,'material/courses.html')


def subjectmaterail(request):
    if request.method=="POST":
        ccode=request.POST['ccode']
    if request.method=="GET":
        ccode=request.GET['ccode']
    ccode=ccode.lower()
    
    coursematerial=subjectmaterial.objects.filter(coursecode=ccode).order_by('-id')
    context={
        'coursematerial':coursematerial,
        'ccode':ccode
    }
    print(coursematerial)
    return render(request,'material/subjectmaterial.html',context)


def loadsolution(request,ccode,materialid):
    solutionlist=materialsolution.objects.filter(material_id=materialid).order_by('-id')
    
    context={
        'solutionlist':solutionlist,
        'materialid':materialid,
        'ccode':ccode
    }
    return render(request,'material/solutionpage.html',context)

def uploadmaterial(request):
    if request.method=="POST" and request.FILES['file']:
        heading=request.POST['heading']
        myfile=request.FILES['file']
        fs=FileSystemStorage()
        uploaded_url=fs.save("material/"+myfile.name,myfile)
        obj=subjectmaterial()
        obj.heading=heading
        obj.coursecode=request.POST['ccode']
        obj.img=uploaded_url
        obj.uploader=request.user
        obj.date=datetime.date.today()
        obj.save()
        return HttpResponseRedirect("/courses/subjectmaterial?ccode="+str(obj.coursecode))


def uploadsolution(request):
    if request.method=="POST" and request.FILES['file']:
        heading=request.POST['heading']
        myfile=request.FILES['file']
        fs=FileSystemStorage()
        uploaded_url=fs.save("materialsolutions/"+myfile.name,myfile)
        obj=materialsolution()
        obj.heading=heading
        obj.material_id=request.POST['materialid']
        obj.img=uploaded_url
        obj.uploader=request.user
        obj.date=datetime.date.today()
        obj.save()
        ccode=request.POST['ccode']
        print(request.POST['materialid'])
        print("bharat singh shekhawat")
        return HttpResponseRedirect("/courses/subjectmaterial/"+str(ccode)+"/"+str(request.POST['materialid']))

def solutioncomments(request,id):
    comment=solutioncomment.objects.filter(solution_id=id).order_by('-id')
    commentlist=[]
    for c in comment:
        temp=dict()
        username=User.objects.only("username").get(id=c.writer_id)
        temp["writer"]=username.username
        print(username.username)
        temp["datetime"]=str(c.date)
        temp["content"]=c.content
        commentlist+=[json.dumps(temp)]
    
    return JsonResponse({'comments':commentlist})

def postsolutioncomments(request):
    if request.user.is_authenticated:
        obj=solutioncomment()
        obj.content=request.GET['content']
        obj.solution_id=request.GET['solutionid']
        obj.date=datetime.datetime.now()
        obj.writer=request.user
        obj.save()
        return HttpResponse("success")
    else:
        return HttpResponse("login to post comments")

def subjectmaterialcommentview(request,ccode):
    commentquery=subjectcomment.objects.filter(subject=subjectmaterial.objects.get(coursecode=ccode)).order_by('-id')
    commentlist=[]
    for k in commentquery:
        temp=dict()
        temp['writer']=User.objects.get(id=k.writer_id).username
        temp['datetime']=str(k.date)
        temp['content']=k.content
        commentlist+=[json.dumps(temp)]

    return JsonResponse({'commentlist':commentlist})


def subjectmaterialcommentupload(request):
    if request.user.is_authenticated:
        temp=subjectcomment()
        try:
            temp.subject=subjectmaterial.objects.get(coursecode=request.GET['ccode'])
        except subjectmaterial.DoesNotExist:
            return HttpResponse("something is missing")
        temp.writer=request.user
        temp.content=request.GET['content']
        temp.date=datetime.date.today()
        temp.save()
        return HttpResponse("success")
    else:
        return HttpResponse("login to post comments")