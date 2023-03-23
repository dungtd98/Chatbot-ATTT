from django.contrib import admin
from .models import Question, QuestionTag, QuestionCategory, Answer
# Register your models here.

admin.site.register(QuestionTag)
admin.site.register(QuestionCategory)
admin.site.register(Question)
admin.site.register(Answer)
