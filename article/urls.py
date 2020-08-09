from django.urls import path
from . import views


urlpatterns=[
    path('',views.allarticles),#done
    path('write',views.writearticle),#done
    path('tags/<hashtag>',views.hashtagarticle),#done
    path('writetopic',views.writesubjectarticle),#done
    path('ajex/like/tarticle/<id>',views.liketarticle),
    path('ajex/dislike/tarticle/<id>',views.disliketarticle),
    path('ajex/tarticle/viewcomments/<id>',views.tarticleviewcomments),
    path('ajex/tarticle/writecomments/',views.tarticlewritecomments),
    
]