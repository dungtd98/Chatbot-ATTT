from django.urls import path
from .views import *
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register(r'daily-news', DailyNewsViewset, basename='daily-news')
router.register(r'alert-news', AlertNewsViewset, basename='alert-news')
# router.register(r'news', NewViewset, basename='new')
urlpatterns = [
    path('newsource-list/', NewSourceList.as_view(), name='newsource-list'),
]
urlpatterns+=router.urls