from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import QuestionViewset, QuestionTagViewset, QuestionCategoryViewset

router = SimpleRouter()
router.register(r'questions-hashtags', QuestionTagViewset, basename='question-tag')
router.register(r'questions-categories', QuestionCategoryViewset, basename='question-category')
router.register(r'questions-answers', QuestionViewset, basename='question')

urlpatterns = [

]
urlpatterns+=router.urls