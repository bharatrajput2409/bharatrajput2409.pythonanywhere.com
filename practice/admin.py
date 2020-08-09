from django.contrib import admin
from .models import questiontag,quiz,question,tag_in_question,submission,editorial,editorial_comment
# Register your models here.
admin.site.register(questiontag)
admin.site.register(question)
admin.site.register(quiz)
admin.site.register(tag_in_question)
admin.site.register(submission)
admin.site.register(editorial)
admin.site.register(editorial_comment)