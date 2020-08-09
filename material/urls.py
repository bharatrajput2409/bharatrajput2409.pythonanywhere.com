from django.urls import path
from . import views

urlpatterns = [
   path('',views.courses),
   path('subjectmaterial',views.subjectmaterail),
   path('subjectmaterial/<ccode>/<materialid>',views.loadsolution),
   path('subjectmaterial/solution/comments/<id>',views.solutioncomments),
   path('subjectmaterial/uploadmaterial',views.uploadmaterial),
   path('subjectmaterial/uploadsolution',views.uploadsolution),
   path('subjectmaterial/postsolutioncomments',views.postsolutioncomments),
   path('ajex/subjectmaterial/commentview/<ccode>',views.subjectmaterialcommentview),
   path('ajex/subjectmaterial/commentupload/',views.subjectmaterialcommentupload)
]
