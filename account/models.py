from django.db import models
from django.contrib.auth.models import User,auth
from article.models import hashtag
# Create your models here.
class userdetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    college=models.CharField(max_length=100,default="national institute of technology karnataka")
    profileimg=models.ImageField(upload_to='profileimg/',default='profileimg/me.jpg')
    totalsubmission=models.IntegerField(default=0)
    correctsubmission=models.IntegerField(default=0)
    ratting=models.IntegerField(default=1000)
    score=models.IntegerField(default=0)
    availablepost=(
        ('s','student'),
        ('t','teacher')
    )
    post=models.CharField(max_length=2,choices=availablepost,default='s')
    varification=(
        ('v',"verified"),
        ('u','unverified')
    )
    verified=models.CharField(max_length=2,choices=varification,default='u')
    contribution=models.IntegerField(default=0)
    def __str__(self):
        return self.college

    
class usershashtag(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    hashtag=models.ForeignKey(hashtag,on_delete=models.CASCADE)
    class Meta:
        unique_together=(("user","hashtag"),)
class tips(models.Model):
    content=models.TextField()

    def __str__(self):
        return self.content

class messagedata(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE)
    reciver=models.ForeignKey(userdetails,on_delete=models.CASCADE)
    datetime=models.DateTimeField()
    seenchoice=(
        ("seen","seen"),
        ("unseen","unseen")
    )
    seenstatus=models.CharField(max_length=6,default="unseen")
    content=models.CharField(max_length=250)
