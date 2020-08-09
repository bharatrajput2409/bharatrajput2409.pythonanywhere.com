from django.contrib import admin
from .models import tarticle,tarticle_comments,tarticle_liked_users,topic,topic_comments,topic_liked_users,hashtag,hashtag_in_tarticles,hashtag_in_topic,subject


# Register your models here.

admin.site.register(tarticle)
admin.site.register(tarticle_comments)
admin.site.register(tarticle_liked_users)
admin.site.register(topic)
admin.site.register(topic_comments)
admin.site.register(topic_liked_users)
admin.site.register(subject)
admin.site.register(hashtag)
admin.site.register(hashtag_in_tarticles)
admin.site.register(hashtag_in_topic)
