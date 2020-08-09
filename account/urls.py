from django.urls import path,include
from . import views


urlpatterns = [
    path('',views.home,name="home"),#done
    path('account/',include([
        path('login',views.login),#done
        path('register',views.register),#done
        path('logout',views.logout),#done
        path('<str:username>/dashboard',views.profilebasic),
        path('<str:username>/feed',views.profilefeed),
        path('<str:username>/interest',views.profileinterest),
        path('ajex/<str:username>/interest/loadtag',views.profileloadtag),
        path('ajex/<str:username>/interest/updatetag',views.profileloadupdatetag),
        path('<str:username>/articles',views.profilearticles),
        path('<str:username>/editprofile',views.profileedit),
        path('<str:sender>/<str:reciver>/sendmessage',views.sendmessage),
        path('<str:username>/viewmessage',views.readmessage)
    ])),
    path('ajex/account/register/<username>',views.checkforavailableusername),#done
    path('community',views.community),#done
    path('community/addquestion',views.addquestion),#done
    path('community/tag/<str:qtag>',views.communitytags),
    path('ajex/community/question/solution/<id>',views.questionsolution),#done
    path('ajex/community/question/like/<id>',views.questionlike),#done
    path('ajex/community/question/dislike/<id>',views.questiondislike),#done
    path('ajex/community/question/solutionpost',views.questionsolutionpost),#done
    path('subject/<subjectname>',views.subjectdetails),#done
    path('subject/<subjectname>/<topicid>',views.subjecttopic),#done
    path('topics/tags/<tag>',views.topictagtopicslist),#done
    path('topics/tags/<tag>/<topicid>',views.topictagtopic),#done
    path('ajex/topic/comments/view/<id>',views.topiccommentsview),#done
    path('ajex/topic/comments/write',views.topiccommentswrite),#done
    path('ajex/like/topic/<id>',views.liketopic,name="liketopic"),#done
    path('ajex/dislike/topic/<id>',views.disliketopic,name="liketopic")#done
]