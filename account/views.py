from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.db import IntegrityError
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from .models import userdetails,usershashtag,tips,messagedata
from article.models import tarticle,hashtag,hashtag_in_tarticles,tarticle_comments,subject,topic,tarticle_liked_users,topic_liked_users,topic_comments,hashtag_in_topic
from material.models import tag_in_question,question,questioncomments,question_liked_user
import json
from django.http import JsonResponse
import datetime
import re
import random

from .models import tips
# Create your views here.
def home(request):#done
    
    sub=subject.objects.all().order_by("id")
    topics=topic.objects.only("id","heading","likes","level","subject").all().order_by('-likes')[:10]
    topiclist=[]
    for t in topics:
        temp=dict()
        temp['article']=t
        
        temp['tags']=hashtag_in_topic.objects.filter(topic_id=t.id)
        topiclist+=[temp]
        print(temp['tags'])
    context={
        'subjects':sub,
        'topics':topiclist
    }
    return render(request,"account/home.html",context)
    

def login(request):#done
    if request.method=="POST":
        user=auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect("/")
        else:
            messages.add_message(request,messages.ERROR,"wrong credential !")
            return HttpResponseRedirect("/account/login")
    else:
        return render(request,'account/login.html')
def register(request):#done
    if request.method=="POST":
        try:
            obj=User.objects.create_user(first_name=request.POST['fname'] ,last_name=request.POST['lname'] ,username=request.POST['username'] ,password=request.POST['password1'],email=request.POST['email'] )
            userdetail=userdetails()
            userdetail.user=obj
            userdetail.save()
            e="User created sucessfully !"
            try:
                tempobj=hashtag.objects.get(id=1)
            except hashtag.DoesNotExist:
                messages.add_message(request,messages.INFO,"Opps something went wrong,but your account is created")
                return redirect("/account/login")
            temp=usershashtag()
            temp.user=obj
            temp.hashtag=tempobj
            temp.save()
            tempobj.followers+=1
            tempobj.save()
            
        except IntegrityError:
            e="Username already exist !"

        messages.add_message(request,messages.ERROR,e)
        return HttpResponseRedirect("/account/login")

    else:
        return render(request,'account/login.html')

def checkforavailableusername(request,username):#done
    try:
        obj=User.objects.get(username=username)
        return HttpResponse("username is not available")
    except User.DoesNotExist:
        return HttpResponse("username is available")
def logout(request):#done
    auth.logout(request)
    return redirect("/")
def profilebasic(request,username):
    try:
        user1=User.objects.get(username=username)
        user2=userdetails.objects.get(user__username=username)
        tip=tips.objects.get(id=random.choice([1]))
        context={
            'user1':user1,
            'user2':user2,
            'tip':tip
        }
    except (userdetails.DoesNotExist,User.DoesNotExist):
        return render(request,'account/nouserfound.html')
    return render(request,'account/profile_basic.html',context)

def profilefeed(request,username):
    try:
        user1=User.objects.get(username=username)
        user2=userdetails.objects.only("profileimg","college").get(user__username=username) #only used herer
        eventtag=hashtag_in_tarticles.objects.filter(hashtag__name="event").order_by('-id')
        
        eventlist=[]
        for k in eventtag:
            temp=dict()
            temp['article']=tarticle.objects.get(id=k.article_id)
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            eventlist+=[temp]
            
        context={
            'user1':user1,
            'eventlist':eventlist,
            'user2':user2
        }
    except (userdetails.DoesNotExist,User.DoesNotExist):
        return render(request,'account/nouserfound.html')
    return render(request,'account/profile_feed.html',context)

def profileinterest(request,username):
    try:
        user1=User.objects.get(username=username)
        user2=userdetails.objects.get(user__username=username)
        usertaglist=usershashtag.objects.filter(user=user1)
        for k in usertaglist:
            print(1)
    except (userdetails.DoesNotExist,User.DoesNotExist):
        return render(request,'account/nouserfound.html')
    return render(request,'account/profile_interest.html',{'user1':user1,'user2':user2,'usertaglist':usertaglist})

def profilearticles(request,username):
    try:
        user1=User.objects.get(username=username)
        user2=userdetails.objects.only("profileimg","college").get(user__username=username)
        article=tarticle.objects.filter(writer__username=username)
        
        articlelist=[]
        for k in article:
            temp=dict()
            temp['article']=k
            temp['tags']=hashtag_in_tarticles.objects.filter(article=temp['article'])
            articlelist+=[temp]
            
        context={
            'user1':user1,
            'articlelist':articlelist,
            'user2':user2
        }
    except (userdetails.DoesNotExist,User.DoesNotExist):
        return render(request,'account/nouserfound.html')
    return render(request,'account/profile_articles.html',context)

def profileedit(request,username):
    try:
        user1=User.objects.get(username=username)
        user2=userdetails.objects.get(user__username=username)
    except (userdetails.DoesNotExist,User.DoesNotExist):
        return render(request,'account/nouserfound.html')
    return render(request,'account/profile_edit.html',{'user1':user1,'user2':user2})


def community(request):
    if request.user.is_authenticated:
        print("i am here")
        hashtag=usershashtag.objects.filter(user=request.user)
        questionlistno=[]
        for k in hashtag:
            temp=tag_in_question.objects.filter(hashtag=k.hashtag)
            for t in temp:
                questionlistno+=[t.question_id]

        
        questionlistno=list(dict.fromkeys(questionlistno))
        questionlistno.sort(reverse=True)
        
        questionlist=[]
        for k in questionlistno:
            temp=dict()
            temp['question']=question.objects.get(id=k)
            temp['tags']=tag_in_question.objects.filter(question=temp['question'])
            try:
                temp['liked']=question_liked_user.objects.get(question=temp['question'],user=request.user).like_dislike
            except question_liked_user.DoesNotExist:
                temp['liked']="n"

            questionlist+=[temp]
            print(temp["tags"])

        
    else:
        print("in else")
        questionlist=[]
        que=question.objects.only("id","likes").all().order_by('-likes')[:10]
        for k in que:
            temp=dict()
            temp['question']=question.objects.get(id=k.id)
            temp['tags']=tag_in_question.objects.filter(question=temp['question'])
            temp["liked"]="n"
            questionlist+=[temp]

    
    context={
        'questionlist':questionlist
    }

    return render(request,'material/nitkcommunity.html',context)

def addquestion(request):
    if request.user.is_authenticated:
        obj=question()
        obj.writer=request.user
        obj.content=request.GET['content']
        obj.date=datetime.date.today()
        obj.save()
        tag=request.GET['hashtag']
        tag=tag.replace(" ","")
        print(tag)
        tag=re.split("#",tag)
        
        taglist=tag[1:-1]
        taglist+=[tag[-1]]
        print(taglist)
        for k in taglist:
            if len(k)<50:
                try:
                    temp=hashtag.objects.get(name=k)
                    temp.used_count+=1
                    temp.save()
                except hashtag.DoesNotExist:
                    temp=hashtag()
                    temp.name=k
                    temp.creator=request.user
                    temp.save()
                try:
                    newtag=usershashtag()
                    newtag.user=request.user
                    newtag.hashtag=temp
                    newtag.save()
                    temp.followers+=1
                    temp.save()
                except IntegrityError:
                    print("already added")
                
                objtemp=tag_in_question()
                objtemp.hashtag=temp
                objtemp.question=obj
                objtemp.save()
            else:
                e="one hash(#) tag length should not exceed 50"
                messages.add_message(request,messages.ERROR,e)
        e="Article posted "
        messages.add_message(request,messages.SUCCESS,e)
        return HttpResponseRedirect("/community")
    else:
        messages(request,messages.INFO,"please login to post a question")
        return render(request,'account/notauthorised.html')

def questionsolutionpost(request):
    if request.user.is_authenticated:
        temp=questioncomments()
        temp.question_id=request.GET['questionid']
        temp.writer=request.user
        temp.date=datetime.date.today()
        temp.content=request.GET['content']
        temp.save()
        return HttpResponse("sucess")
    else:
        return HttpResponse("login to post comment")
def questionsolution(request,id):
    
    sol=questioncomments.objects.filter(question_id=id)
    
    solutionlist=[]
    for s in sol:
        temp=dict()
        username=User.objects.only("username").get(id=s.writer_id)
        temp['writer']=username.username
        temp['datetime']=str(s.date)
        temp['content']=s.content
        solutionlist+=[json.dumps(temp)]
    return JsonResponse({'solutionlist':solutionlist})
def subjectdetails(request,subjectname):#done
    try:
        sub=subject.objects.get(name=subjectname)    
    except subject.DoesNotExist:
        return render(request,'account/nocontentfound.html')
    easytopic=topic.objects.only("heading").filter(subject=sub,level="easy").order_by('id')
    mediumtopic=topic.objects.only("heading").filter(subject=sub,level="medium").order_by('id')
    hardtopic=topic.objects.only("heading").filter(subject=sub,level="hard").order_by('id')
    context={
        'subject':sub,
        'easytopic':easytopic,
        'mediumtopic':mediumtopic,
        'hardtopic':hardtopic
    }
    return render(request,'articles/subjectdetails.html',context)


def subjecttopic(request,subjectname,topicid):#done
    try:
        topicdetail=dict()
        topicdetail['article']=topic.objects.get(id=topicid)
        topicdetail['tags']=hashtag_in_topic.objects.filter(topic=topicdetail['article'])
        try:
            if request.user.is_authenticated:
                topicdetail['liked']=topic_liked_users.objects.get(user=request.user,topic=topicid).like_dislike
            else:
                topicdetail['liked']="n"
        except topic_liked_users.DoesNotExist:
            topicdetail['liked']="n"
    except topic.DoesNotExist:
        return render(request,'account/nocontentfound.html')
    return render(request,'articles/subjecttopic.html',{'topicdetail':topicdetail})


def topictagtopicslist(request,tag):#done
    try:
        topictag=hashtag.objects.get(name=tag)
    except hashtag.DoesNotExist:
        return render(request,'account/nocontentfound.html')
    
    easytopic=topic.objects.only("heading").filter(hashtag_in_topic__hashtag=topictag,level="easy").order_by('id')
    
    mediumtopic=topic.objects.only("heading").filter(hashtag_in_topic__hashtag=topictag,level="medium").order_by('id')
    hardtopic=topic.objects.only("heading").filter(hashtag_in_topic__hashtag=topictag,level="hard").order_by('id')
    context={
        'topictag':topictag,
        'easytopic':easytopic,
        'mediumtopic':mediumtopic,
        'hardtopic':hardtopic
    }
    return render(request,'articles/topictagtopics.html',context)
def topictagtopic(request,tag,topicid):#done
    try:
        topicdetail=dict()
        topicdetail['article']=topic.objects.get(id=topicid)
        topicdetail['tags']=hashtag_in_topic.objects.filter(topic=topicdetail['article'])
        try:
            if request.user.is_authenticated:
                topicdetail['liked']=topic_liked_users.objects.get(user=request.user,topic=topicid).like_dislike
            else:
                topicdetail['liked']="n"
            
        except topic_liked_users.DoesNotExist:
            topicdetail['liked']="n"
    except topic.DoesNotExist:
        return render(request,'account/nocontentfound.html')
    return render(request,'articles/subjecttopic.html',{'topicdetail':topicdetail})



def liketopic(request,id):#done
    if request.user.is_authenticated:
        
        try:
            topictolike=topic.objects.get(id=id)
            temp=topic_liked_users()
            try:
                temp.topic=topictolike
                temp.user=request.user
                temp.like_dislike="l"
                temp.save()
                topictolike.likes+=1
                topictolike.save()
            except IntegrityError:
                temp=topic_liked_users.objects.get(topic_id=id,user=request.user)
                if temp.like_dislike=="d":                  
                    temp.like_dislike="l"
                    temp.save()
                    topictolike.likes+=2
                    topictolike.save()
        except topic.DoesNotExist:
            return render(request,'account/nocontentfound.html')
        return HttpResponse(topictolike.likes)
    else:
        return HttpResponse("login to hit like")

def disliketopic(request,id):#done
    if request.user.is_authenticated:
        
        try:
            topictolike=topic.objects.get(id=id)
            temp=topic_liked_users()
            try:
                temp.topic=topictolike
                temp.user=request.user
                temp.like_dislike="d"
                temp.save()
                topictolike.likes+=1
                topictolike.save()
            except IntegrityError:
                temp=topic_liked_users.objects.get(topic_id=id,user=request.user)
                if temp.like_dislike=="l":                  
                    temp.like_dislike="d"
                    temp.save()
                    topictolike.likes-=2
                    topictolike.save()
        except topic.DoesNotExist:
            return render(request,'account/nocontentfound.html')
        return HttpResponse(topictolike.likes)
    else:
        return HttpResponse("login to hit dislike")

def topiccommentsview(request,id):#done
    comment=topic_comments.objects.filter(article_id=id).order_by('-id')
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


def topiccommentswrite(request):#done
    if request.user.is_authenticated:
        obj=topic_comments()
        obj.writer=request.user
        obj.content=request.GET['content']
        obj.article_id=request.GET['topicid']
        obj.date=datetime.date.today()
        obj.save()
        return HttpResponse("sucess")
    else:
        return HttpResponse("login to post comment")

def questionlike(request,id):
    if request.user.is_authenticated:
        try:
            queobj=question.objects.get(id=id)
        except question.DoesNotExist:
            return HttpResponse("some thing went wrong")
        try:
            likedobj=question_liked_user.objects.get(question=queobj,user=request.user)
            print(likedobj.like_dislike)
            if likedobj.like_dislike=="d":
                queobj.likes+=2
            likedobj.like_dislike="l"
            likedobj.save()
            print("try")
        except question_liked_user.DoesNotExist:
            likedobj=question_liked_user()
            likedobj.question=queobj
            likedobj.user=request.user
            likedobj.like_dislike="l"
            likedobj.save()
            queobj.likes+=1
        queobj.save()
        return HttpResponse(queobj.likes)
    else:
        return HttpResponse("login to hit like")

def questiondislike(request,id):
    if request.user.is_authenticated:
        try:
            queobj=question.objects.get(id=id)
        except question.DoesNotExist:
            return HttpResponse("some thing went wrong")
        try:
            likedobj=question_liked_user.objects.get(question=queobj,user=request.user)
            print(likedobj.like_dislike)
            if likedobj.like_dislike=="l":
                queobj.likes-=2
            likedobj.like_dislike="d"
            likedobj.save()
            
        except question_liked_user.DoesNotExist:
            likedobj=question_liked_user()
            likedobj.question=queobj
            likedobj.user=request.user
            likedobj.like_dislike="d"
            likedobj.save()
            queobj.likes-=1
        
        queobj.save()
        return HttpResponse(queobj.likes)
    else:
        return HttpResponse("login to hit dislike")


def sendmessage(request,sender,reciver):
    if request.method=="POST":
        if request.user.is_authenticated:
            temp=messagedata()
            temp.sender=request.user
            try:
                temp.reciver_id=userdetails.objects.get(user__username=reciver).id
            except userdetails.DoesNotExist:
                messages.add_message(request,messages.INFO,"reciver does not exist")
                return redirect("/account/"+sender+"/"+reciver+"/sendmessage")
            temp.datetime=datetime.datetime.now()
            temp.content=request.POST['content']
            temp.save()
            e="Message sent"
        else:
            e="login to send message"
        messages.add_message(request,messages.INFO,e)
        return redirect("/account/"+sender+"/"+reciver+"/sendmessage")
    else:
        if request.user.is_authenticated:
            try:
                user1=User.objects.only("username","first_name","last_name","id").get(username=reciver)
                user2=userdetails.objects.only("profileimg").get(user=user1)
                print(user1)
                print(user2)
            except (User.DoesNotExist,userdetails.DoesNotExist):
                return render(request,'account/nouserfound.html')
            context={
                'reciver':reciver,
                'user1':user1,
                'user2':user2
            }
            return render(request,'account/profile_sendmessage.html',context)
        else:
            messages.add_message(request,messages.INFO,"login to access this feature !")
            return redirect("/account/login")

def readmessage(request,username):
    if request.user.is_authenticated and User.objects.get(username=username)==request.user:
        temp=messagedata.objects.filter(sender=request.user)
        temp=temp.union(messagedata.objects.filter(reciver__user=request.user)).order_by('-id')
        messagelist=[]
        for k in temp:
            d=dict()
            d['sender']=k.sender
            d['reciver']=User.objects.get(id=k.reciver_id)
            d['datetime']=k.datetime
            d['content']=k.content
            if k.seenstatus=="unseen" and k.reciver_id==request.user.id:
                print(k.reciver_id==request.user.id)
                print(k.reciver_id)
                print(request.user.id)
                k.seenstatus="seen"
                k.save()
                k.seenstatus="unseen"
            d['status']=k.seenstatus
            messagelist+=[d]
        try:
            user1=User.objects.only("username","first_name","last_name","id").get(username=username)
            user2=userdetails.objects.only("profileimg").get(user=user1)
            
        except (User.DoesNotExist,userdetails.DoesNotExist):
            return render(request,'account/nouserfound.html')
        context={
            'messagelist':messagelist,
            'user1':user1,
            'user2':user2
        }
        return render(request,'account/viewmessage.html',context)
    else:
        return render(request,'account/notauthorised.html')


def communitytags(request,qtag):
    if request.user.is_authenticated:
        print("i am here")
        questionlistno=[]
        try:
            temp=tag_in_question.objects.filter(hashtag=hashtag.objects.get(name=qtag))
        except hashtag.DoesNotExist:
            return render(request,'account/nocontentfound.html')
        for t in temp:
            questionlistno+=[t.question_id]

        
        questionlistno=list(dict.fromkeys(questionlistno))
        questionlistno.sort(reverse=True)   
        
        questionlist=[]
        for k in questionlistno:
            temp=dict()
            temp['question']=question.objects.get(id=k)
            temp['tags']=tag_in_question.objects.filter(question=temp['question'])
            try:
                temp['liked']=question_liked_user.objects.get(question=temp['question'],user=request.user).like_dislike
            except question_liked_user.DoesNotExist:
                temp['liked']="n"

            questionlist+=[temp]
            print(temp["tags"])

        
    else:
        print("in else")
        questionlist=[]
        que=question.objects.only("id","likes").all().order_by('-likes')[:10]
        for k in que:
            temp=dict()
            temp['question']=question.objects.get(id=k.id)
            temp['tags']=tag_in_question.objects.filter(question=temp['question'])
            temp["liked"]="n"
            questionlist+=[temp]

    
    context={
        'questionlist':questionlist
    }

    return render(request,'material/nitkcommunity.html',context)


def profileloadtag(request,username):
    if request.user.is_authenticated and username==request.user.username:
        alltaglist=[]
        temp=hashtag.objects.all()
        print(temp)
        for k in temp:
            d=dict()
            
            d['id']=k.id
            d['name']=k.name
            d['followers']=k.followers
            try:
                usershashtag.objects.get(user__username=username,hashtag=k)
                d['status']="1"
            except usershashtag.DoesNotExist:
                d['status']="0"
            alltaglist+=[json.dumps(d)]
        return JsonResponse({'alltaglist':alltaglist})
    else:
        return render(request,'account/notauthorised.html')


def profileloadupdatetag(request,username):
    if request.user.is_authenticated and username==request.user.username:
        taglisttemp=json.loads(request.GET['tagid'])
        taglist=[]
        for k in taglisttemp:
            taglist+=[int(k)]
        
        for k in taglist:
            obj=usershashtag()
            try:
                obj.user=request.user
                obj.hashtag_id=k
                obj.save()
            except IntegrityError:
                print(0)
        tempobj=usershashtag.objects.filter(user=request.user)
        
        for k in tempobj:
            inttemp=int(k.hashtag_id)
            try:
                i=taglist.index(inttemp)
            except ValueError:
                k.delete()
        
        alltaglist=[]
        for t in taglist:
            d=dict()
            try:
                k=hashtag.objects.get(id=t)
                d['id']=k.id
                d['name']=k.name
                d['followers']=k.followers
                alltaglist+=[json.dumps(d)]
            except hashtag.DoesNotExist:
                print(0)
        return JsonResponse({'alltaglist':alltaglist})
    else:
        return render(request,'account/notauthorised.html')
    
    


