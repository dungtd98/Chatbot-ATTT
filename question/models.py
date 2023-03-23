from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import pre_save
from django.dispatch import receiver

# Create your models here.
UserModel = get_user_model()

class QuestionTag(models.Model):
    name = models.CharField(max_length=255, 
                            blank=False, 
                            verbose_name='Tên của tag')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self) -> str:
        return self.name
    class Meta:
        default_permissions = ()
class QuestionCategory(models.Model):
    name = models.CharField(max_length=255, 
                            blank=False, 
                            verbose_name='Nhóm câu hỏi')
    description = models.TextField(blank=True, verbose_name='Miêu tả')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(UserModel, 
                                on_delete=models.DO_NOTHING, 
                                blank=False, null=False)
    def __str__(self) -> str:
        return self.name
    class Meta:
        default_permissions = ()
class Question(models.Model):
    question = models.TextField()
    QUESTION_TYPE = [
        ('OPEN','Câu hỏi mở'),
        ('CLOSE','Câu hỏi đóng')
    ]
    type = models.CharField(
        verbose_name='Loại câu hỏi',
        max_length=10,
        choices=QUESTION_TYPE,
        default='OPEN'
    )
    url = models.URLField()
    attachment = models.URLField()
    hashtags = models.ManyToManyField(QuestionTag, blank=True)
    category = models.ForeignKey(QuestionCategory, 
                                 on_delete = models.CASCADE, 
                                 null=True, 
                                 related_name='child_questions')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    creator = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.question
    class Meta:
        default_permissions  = ()
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, 
                                 blank=False, related_name='answers' )
    content = models.TextField()
    def __str__(self) -> str:
        return 'ANSWER OF: '+self.question.question
    
    class Meta:
        default_permissions  = ()