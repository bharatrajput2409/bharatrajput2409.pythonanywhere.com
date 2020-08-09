from django.urls import path
from . import views
urlpatterns = [
    path('contest',views.contestlist,name="contestlist"),
    path('topics',views.topictags,name="topictags"),
    path('quizzes',views.quizzeslist,name="quizzeslist"),
    path('quizzes/<str:quizname>',views.loadquiz),
    path('quizzes/<str:quizname>/quizreport',views.quizreport),
    path('ajex/question/<int:qid>/submit',views.questionsubmit),
    path('ajex/question/<int:id>/loadquestion',views.loadquestion)
]