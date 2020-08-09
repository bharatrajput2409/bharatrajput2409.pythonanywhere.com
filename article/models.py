from django.db import models
from django.contrib.auth.models import User,auth
import datetime

# Create your models here.

# only for thought article 

class tarticle(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    heading=models.CharField(max_length=150)
    content=models.TextField()
    likes=models.IntegerField(default=0)
    date=models.DateField()
    def __str__(self):
        return self.heading

class tarticle_liked_users(models.Model):
    article=models.ForeignKey(tarticle,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like=(
        ("l","like"),
        ("d","dislike")
    )
    like_dislike=models.CharField(max_length=2,choices=like)
    class Meta:
        unique_together=(("article","user"),)


class hashtag(models.Model):
    name=models.CharField(max_length=50,unique=True)
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    followers=models.IntegerField(default=0)
    used_count=models.IntegerField(default=1)
    def __str__(self):
        return self.name

class hashtag_in_tarticles(models.Model):
    article=models.ForeignKey(tarticle,on_delete=models.CASCADE)
    hashtag=models.ForeignKey(hashtag,on_delete=models.CASCADE)
    class Meta:
        unique_together=(("article","hashtag"),)

class tarticle_comments(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    article=models.ForeignKey(tarticle,on_delete=models.CASCADE)
    date=models.DateField()
    
    def __str__(self):
        return self.content

# subject article with #tag

class subject(models.Model):
    name=models.CharField(max_length=50,unique=True)
    intro=models.TextField()
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.name

class topic(models.Model):
    heading=models.CharField(max_length=150)
    content=models.TextField()
    subject=models.ForeignKey(subject,on_delete=models.SET_NULL,null=True)
    creator=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    likes=models.IntegerField(default=0)
    date=models.DateField()
    levelchoices=(
        ("easy","easy"),
        ("medium","medium"),
        ("hard","hard")
    )
    level=models.CharField(max_length=8,choices=levelchoices,default="medium")

    def __str__(self):
        return self.heading


class topic_liked_users(models.Model):
    topic=models.ForeignKey(topic,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    like=(
        ("l","like"),
        ("d","dislike")
    )
    like_dislike=models.CharField(max_length=2,choices=like)
    class Meta:
        unique_together=(("topic","user"),)

class topic_comments(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    content=models.TextField()
    article=models.ForeignKey(topic,on_delete=models.CASCADE)
    date=models.DateField()
    
    def __str__(self):
        return self.content


class hashtag_in_topic(models.Model):
    topic=models.ForeignKey(topic,on_delete=models.CASCADE)
    hashtag=models.ForeignKey(hashtag,on_delete=models.CASCADE)
    class Meta:
        unique_together=(("topic","hashtag"),)

    


