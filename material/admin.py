from django.contrib import admin
from .models import subjectmaterial,materialsolution,solutioncomment,question,tag_in_question,questioncomments
# Register your models here.

admin.site.register(subjectmaterial)
admin.site.register(materialsolution)
admin.site.register(solutioncomment)
admin.site.register(question)
admin.site.register(questioncomments)
admin.site.register(tag_in_question)