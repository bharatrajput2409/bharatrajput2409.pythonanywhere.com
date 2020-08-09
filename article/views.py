from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from account.models import userdetails,usershashtag
from .models import tarticle,hashtag,hashtag_in_tarticles,tarticle_comments,subject,topic,tarticle_liked_users,topic_liked_users,topic_comments,hashtag_in_topic
import re
import datetime
import json
from django.http import JsonResponse
# Create your views here.


def allarticles(request):#done
    if request.user.is_authenticated:
        usershash=usershashtag.objects.filter(user=request.user)
        articleno=[]
        
        for k in usershash:
            temp=hashtag_in_tarticles.objects.filter(hashtag=k.hashtag)
            
            for no in temp:
                articleno+=[no.article_id]
        articleno = list(dict.fromkeys(articleno))
        
        articleno.sort(reverse=True)
        articlelist=[]
        for k in articleno:
            temp=dict()
            temp['article']=tarticle.objects.get(id=k)
            try:
                liked=tarticle_liked_users.objects.get(article=temp['article'],user=request.user)
                temp['liked']=liked.like_dislike
            except tarticle_liked_users.DoesNotExist:
                temp['liked']="n"
            
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            
            writer=dict()
            t=User.objects.get(id=temp['article'].writer_id).username
            writer['username']=t
            writer['img']=userdetails.objects.get(user__username=t).profileimg
            temp['writer']=writer
            articlelist+=[temp]
    else:
        print("in else")
        articletemp=tarticle.objects.only("id","likes").all().order_by('-likes')
        articlelist=[]
        for k in articletemp:
            temp=dict()
            temp['article']=tarticle.objects.get(id=k.id)
            temp['liked']="n"            
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            print(temp['tags'])
            writer=dict()
            t=User.objects.get(id=temp['article'].writer_id).username
            writer['username']=t
            writer['img']=userdetails.objects.get(user__username=t).profileimg
            temp['writer']=writer
            articlelist+=[temp]
        print(articlelist)
        
        
    return render(request,'articles/allarticles.html',{'articlelist':articlelist})


def writearticle(request):#done
    if request.method=="POST":
        heading=request.POST['heading']
        content=request.POST['content']
        hashtagstr=request.POST['hashtag']
        hashtagstr=hashtagstr.replace(" ","")
        temp=re.split("#",hashtagstr)
        hashtagstr=[temp[-1]]
        hashtagstr+=temp[1:-1]
        print(hashtagstr)
        obj=tarticle()
        obj.writer=request.user
        obj.heading=heading
        obj.content=content
        obj.date=datetime.date.today()
        
        obj.save()
        
        for k in hashtagstr:
            k.lower()
            if len(k)<50:
                try:
                    hashobj=hashtag.objects.get(name=k)
                    hashobj.used_count +=1
                    hashobj.save()
                except hashtag.DoesNotExist :
                    hashobj=hashtag()
                    hashobj.name=k
                    hashobj.creator=request.user
                    hashobj.used_count=1
                    hashobj.save()
                try:
                    newtag=usershashtag()
                    newtag.user=request.user
                    newtag.hashtag=hashobj
                    newtag.save()               
                except IntegrityError:
                    print("already added")
                objtemp=hashtag_in_tarticles()
                objtemp.article=obj
                objtemp.hashtag=hashobj
                objtemp.save()
                
            else:
                e="one hash(#) tag length should not exceed 50"
                messages.add_message(request,messages.ERROR,e)
        try:
            userobj=userdetails.objects.get(user=request.user)
            userobj.contribution+=1
            userobj.save()
        except userdetails.DoesNotFound:
            print(0)
        e="Article posted "
        messages.add_message(request,messages.SUCCESS,e)
        return HttpResponseRedirect("/articles/write")
    else:
        if request.user.is_authenticated:
            return render(request,'articles/writearticle.html')
        else:
            messages.add_message(request,messages.ERROR,"please login to access this feature !")
            return redirect("/account/login")


def hashtagarticle(request,hashtag):#done
    if request.user.is_authenticated:
        articlelist=[]
        tempk=hashtag_in_tarticles.objects.filter(hashtag__name=hashtag).order_by('-id')
        for k in tempk:
            temp=dict()
            temp['article']=tarticle.objects.get(id=k.article_id)
            try:
                liked=tarticle_liked_users.objects.get(article=temp['article'],user=request.user)
                temp['liked']=liked.like_dislike
            except tarticle_liked_users.DoesNotExist:
                temp['liked']="n"
            
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            
            writer=dict()
            t=User.objects.get(id=temp['article'].writer_id).username
            writer['username']=t
            writer['img']=userdetails.objects.get(user__username=t).profileimg
            temp['writer']=writer
            articlelist+=[temp]       
        
    else:
        print("in else")
        articletemp=hashtag_in_tarticles.objects.filter(hashtag__name=hashtag)
        articlelist=[]
        for k in articletemp:
            temp=dict()
            temp['article']=tarticle.objects.get(id=k.article_id)
            temp['liked']="n"            
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            print(temp['tags'])
            writer=dict()
            t=User.objects.get(id=temp['article'].writer_id).username
            writer['username']=t
            writer['img']=userdetails.objects.get(user__username=t).profileimg
            temp['writer']=writer
            articlelist+=[temp]
        print(articlelist)
        
    return render(request,'articles/allarticles.html',{'articlelist':articlelist})

def writesubjectarticle(request):#done
    if request.user.is_authenticated and (userdetails.objects.get(user=request.user).contribution >=100 or userdetails.objects.get(user=request.user).verified=="v"):
        if request.method=="POST":
            heading=request.POST['heading']
            content=request.POST['content']
            hashtagtext=request.POST['hashtag']
            hashtagtext=hashtagtext.replace(" ","")
            temp=re.split("#",hashtagtext)
            hashtaglist=[temp[-1]]
            hashtaglist+=temp[1:-1]
            print(hashtaglist)
            level=request.POST['level']
            sub=request.POST['subject']
            obj=topic()
            obj.heading=heading
            obj.content=content
            obj.subject_id=sub
            obj.creator=request.user
            obj.date=datetime.date.today()
            if level[0]=="e":
                obj.level="easy"
            elif level[0]=="m":
                obj.level="medium"
            elif level[0]=="h":
                obj.level="hard"
            else:
                obj.level="medium"
            obj.save()
            objtemp=hashtag_in_topic()
            for k in hashtaglist:
                if len(k)<50:
                    try:
                        hashobj=hashtag.objects.get(name=k)
                        hashobj.used_count+=1
                        hashobj.save()
                    except hashtag.DoesNotExist :
                        hashobj=hashtag()
                        hashobj.name=k
                        hashobj.creator=request.user
                        hashobj.save()
                    try:
                        newtag=usershashtag()
                        newtag.user=request.user
                        newtag.hashtag=hashobj
                        newtag.save()
                        hashobj.followers+=1
                        hashobj.save()             
                    except IntegrityError:
                        print("already added")
                    objtemp=hashtag_in_topic()
                    objtemp.topic=obj
                    objtemp.hashtag=hashobj
                    objtemp.save()
            
                else:
                    e="one hash(#) tag length should not exceed 50"
                    messages.add_message(request,messages.ERROR,e)
            try:
                userobj=userdetails.objects.get(user=request.user)
                userobj.contribution+=2
                userobj.save()
            except userdetails.DoesNotFound:
                print(0)
            e="topic content added sucessfully !"
            messages.add_message(request,messages.SUCCESS,e)
            return HttpResponseRedirect("/articles/writetopic")
        else:
            subjects=subject.objects.all()
            return render(request,'articles/writetopic.html',{'subjects':subjects})
    else:
        
        return render(request,'account/notauthorised.html')

def liketarticle(request,id):
    if request.user.is_authenticated:
        try:
            art=tarticle.objects.get(id=id)
            try:
                temp=tarticle_liked_users()
                temp.article_id=id
                temp.user=request.user
                temp.like_dislike="l"
                temp.save()
                art.likes+=1
                art.save()
            except IntegrityError:
                temp=tarticle_liked_users.objects.get(article_id=id,user=request.user)
                if temp.like_dislike=="d":
                    temp.like_dislike="l"
                    art.likes+=2
                    art.save()
                    temp.save()
        except tarticle.DoesNotExist:
            return render(request,'account/nocontentfound.html')        
        return HttpResponse(art.likes)
    else:
        return HttpResponse("login to hit like")


def disliketarticle(request,id):
    
    if request.user.is_authenticated:
        try:
            art=tarticle.objects.get(id=id)
            try:
                temp=tarticle_liked_users()
                temp.article_id=id
                temp.user=request.user
                temp.like_dislike="d"
                temp.save()
                art.likes-=1
                art.save()
            except IntegrityError:
                temp=tarticle_liked_users.objects.get(article_id=id,user=request.user)
                if temp.like_dislike=="l":
                    temp.like_dislike="d"
                    art.likes-=2
                    art.save()
                    temp.save()
        except tarticle.DoesNotExist:
            return render(request,'account/nocontentfound.html')        
        return HttpResponse(art.likes)
    else:
        return HttpResponse("login to hit dislike")


def tarticleviewcomments(request,id):
    commentlist=[]
    commentquery=tarticle_comments.objects.filter(article_id=id)
    for k in commentquery:
        temp=dict()
        temp['writer']=User.objects.get(id=k.writer_id).username
        temp['content']=k.content
        temp['datetime']=str(k.date)
        commentlist+=[json.dumps(temp)]

    return JsonResponse({'commentlist':commentlist})

def tarticlewritecomments(request):
    if request.user.is_authenticated:
        temp=tarticle_comments()
        temp.writer=request.user
        temp.content=request.GET['content']
        temp.article_id=request.GET['articleid']
        temp.date=datetime.date.today()
        temp.save()
        return HttpResponse("success")
    else:
        return HttpResponse("login to post comments")
    