from django.db import models
from django.contrib.auth.models import User,auth
# Create your models here.


class questiontag(models.Model):
    name=models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
class quiz(models.Model):
    name=models.CharField(max_length=60,unique=True)
    writer=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    total_question=models.IntegerField(default=0)
    attempts=models.IntegerField(default=0)
    date=models.DateField()
    
    def __str__(self):
        return self.name

class question(models.Model):
    content=models.TextField()
    questiontype=(
        ('objective','objective'),
        ('subjective','subjective')
    )
    q_type=models.CharField(max_length=15,choices=questiontype,default="objective")
    total_submission=models.IntegerField(default=0)
    correct_submission=models.IntegerField(default=0)
    quiz=models.ForeignKey(quiz,null=True,on_delete=models.SET_NULL,verbose_name="quiz id")
    availabledifficulty=(
        ('1','level 1'),
        ('2','level 2'),
        ('3','level 3')
    )
    difficulty_level=models.CharField(max_length=2,choices=availabledifficulty,default=1)
    option1=models.CharField(max_length=150)
    option2=models.CharField(max_length=150)
    option3=models.CharField(max_length=150)
    option4=models.CharField(max_length=150)
    correct_ans=models.CharField(max_length=2)

    def __str__(self):
        return self.content


class tag_in_question(models.Model):
    question=models.ForeignKey(question,on_delete=models.CASCADE)
    topic_tag=models.ForeignKey(questiontag,on_delete=models.CASCADE)
    class Meta:
        unique_together=(("question","topic_tag"),)

    def __str__(self):
        return self.question__name

class submission(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)    
    question=models.ForeignKey(question,on_delete=models.CASCADE)
    response=models.CharField(max_length=2)
    status=models.BooleanField()
    datetime=models.DateTimeField()

class editorial(models.Model):
    question=models.ForeignKey(question,on_delete=models.CASCADE)
    content=models.TextField()

class editorial_comment(models.Model):
    content=models.TextField()
    editorial=models.ForeignKey(editorial,on_delete=models.CASCADE)
    writer=models.ForeignKey(User,on_delete=models.CASCADE)
    datetime=models.DateTimeField()


# contest models for practice


# class contest(models.Model):
#     name=models.CharField(max_length=100)
#     writer=models.ForeignKey(User,on_delete=models.CASCADE)
#     totalquestion=models.IntegerField()
#     start=models.DateTimeField()
#     end=models.DateTimeField()

#     def __str__(self):
#         return self.name

# class contestquestion(models.Model):
#     heading=models.CharField(max_length=100)
#     content=models.TextField()
#     questiontype=(
#         ('o','objective'),
#         ('s','subjective')
#     )
#     q_type=models.CharField(max_length=1)
#     total_submission=models.IntegerField()
#     correct_submission=models.IntegerField()
#     contest=models.ForeignKey(contest,null=True,on_delete=models.SET_NULL,verbose_name="quiz id")
#     availabledifficulty=(
#         ('1','level 1'),
#         ('2','level 2'),
#         ('3','level 3')
#     )
#     difficulty_level=models.CharField(max_length=1,choices=availabledifficulty)
#     option1=models.TextField()
#     option2=models.TextField()
#     option3=models.TextField()
#     option4=models.TextField()

#     def __str__(self):
#         return self.heading



# class contestquestion_topic_tag(models.Model):
#     question=models.ForeignKey(contestquestion,on_delete=models.CASCADE)
#     topic_tag=models.ForeignKey(topic,on_delete=models.CASCADE)
#     class Meta:
#         unique_together=(("question","topic_tag"),)

#     def __str__(self):
#         return self.question__name

# class contestsubmission(models.Model):
#     user=models.ForeignKey(User,on_delete=models.CASCADE)    
#     question=models.ForeignKey(contestquestion,on_delete=models.CASCADE)
#     response=models.CharField(max_length=1)
#     status=models.BooleanField()
#     datetime=models.DateTimeField()

# class contesteditorial(models.Model):
#     question=models.ForeignKey(contestquestion,on_delete=models.CASCADE)
#     content=models.TextField()

# class contesteditorial_comment(models.Model):
#     content=models.TextField()
#     question=models.ForeignKey(contestquestion,on_delete=models.CASCADE)
#     writer=models.ForeignKey(User,on_delete=models.CASCADE)
#     datetime=models.DateTimeField()

    