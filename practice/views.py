from django.shortcuts import render
from django.contrib.auth.models import User,auth
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponseRedirect,HttpResponse
from account.models import userdetails
from .models import questiontag,quiz,question,tag_in_question,submission,editorial,editorial_comment
import datetime
import json
from django.http import JsonResponse
# Create your views here.
def contestlist(request):

    return render(request,'practice/contestlist.html')

def topictags(request):

    return render(request,'practice/topictags.html')

def quizzeslist(request):
    quizlist=quiz.objects.all()
    return render(request,'practice/quizzeslist.html',{'quizlist':quizlist})

def loadquiz(request,quizname):
    if request.user.is_authenticated:
        questionid=question.objects.values("id").filter(quiz__name=quizname)
        print(questionid)
        questiondata=question.objects.values("id","content","option1","option2","option3","option4").get(id=questionid[0]['id'])    
        print(questiondata)

        
        context={
            'questionid':questionid,
            'question':questiondata
        }
        return render(request,'practice/quizquestions.html',context)
    else:
        messages.add_message(request,messages.INFO,"login to solve quiz !")
        return redirect("/account/login")

def questionsubmit(request,qid):
    if request.user.is_authenticated:
        try:
            submissionobj=submission.objects.get(user=request.user,question_id=qid,status=1)
            return HttpResponse("submitted successfully")
        except submission.DoesNotExist:
            temp=submission()
            temp.user=request.user
            temp.datetime=datetime.datetime.now()
            temp.question_id=qid
            temp.response=request.GET['ans']
            print(temp.response)
            try:
                queobj=question.objects.get(id=qid)
            except question.DoesNotExist:
                return HttpResponse("Opps something went wrong...kindly refresh the page...")
            try:
                userobj=userdetails.objects.get(user=request.user)
            except userdetails.DoesNotExist:
                return HttpResponse("Opps something went wrong...kindly refresh the page...")
            if queobj.correct_ans[0]==request.GET['ans']:
                temp.status=True
                userobj.correctsubmission+=1
                userobj.score+=int(queobj.difficulty_level[0],10)
            else:
                temp.status=False
            userobj.totalsubmission+=1
            
            
            temp.save()
            userobj.save()
            return HttpResponse("submitted successfully")
            

    else:
        messages.add_message(request,messages.INFO,"login to access this feature")
        return redirect("/account/login")

def loadquestion(request,id):
    if request.user.is_authenticated:
        try:
            temp=question.objects.get(id=id)
        except question.DoesNotExist:
            return HttpResponse("Opps something went wrong...kindly refresh the page...")
        questiondata=dict()
        print(temp.option1)
        questiondata['content']=temp.content
        questiondata['id']=temp.id
        questiondata['option1']=temp.option1
        questiondata['option2']=temp.option2
        questiondata['option3']=temp.option3
        questiondata['option4']=temp.option4
        return JsonResponse({'question':questiondata})
    else:
        messages.add_message(request,messages.INFO,"login to access this feature")
        return redirect("/account/login")
def quizreport(request,quizname):
    if request.user.is_authenticated:
        questionlist=[]
        temp=question.objects.filter(quiz__name=quizname)
        for k in temp:
            d=dict()
            print(k.correct_ans)
            d['content']=k.content
            d['option1']=k.option1
            d['option2']=k.option2
            d['option3']=k.option3
            d['option4']=k.option4
            d['ans']=k.correct_ans
            d['response']=submission.objects.get(user=request.user,question=k)
    else:
        messages.add_message(request,messages.INFO,"login to access this feature")
        return redirect("/account/login")