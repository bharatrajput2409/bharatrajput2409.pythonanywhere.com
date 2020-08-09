from django.db import models
from django.contrib.auth.models import User,auth
from article.models import hashtag
# Create your models here.



class subjectmaterial(models.Model):
    heading=models.CharField(max_length=60)
    coursecode=models.CharField(max_length=30,unique=True)
    img=models.ImageField(upload_to='material')
    uploader=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    

    def __str__(self):
        return self.heading


class subjectcomment(models.Model):
    subject=models.ForeignKey(subjectmaterial,on_delete=models.CASCADE)
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.content


class materialsolution(models.Model):
    heading=models.CharField(max_length=60)
    img=models.ImageField(upload_to='material')
    uploader=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    material=models.ForeignKey(subjectmaterial,on_delete=models.CASCADE)

    def __str__(self):
        return self.heading
    
class solutioncomment(models.Model):
    solution=models.ForeignKey(materialsolution,on_delete=models.CASCADE)
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    date=models.DateField()

    def __str__(self):
        return self.content


class question(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    date=models.DateField()
    likes=models.IntegerField(default=0)


class tag_in_question(models.Model):
    hashtag=models.ForeignKey(hashtag,on_delete=models.CASCADE)
    question=models.ForeignKey(question,on_delete=models.CASCADE)

class questioncomments(models.Model):
    question=models.ForeignKey(question,on_delete=models.CASCADE)
    content=models.TextField()
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateField()
    

class question_liked_user(models.Model):
    question=models.ForeignKey(question,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like=(
        ("l","like"),
        ("d","dislike")
    )
    like_dislike=models.CharField(max_length=2,choices=like)
    class Meta:
        unique_together=(("question","user"),)


    
