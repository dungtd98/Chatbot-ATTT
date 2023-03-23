from .views import Botview, UserInteractionView
from django.urls import path

urlpatterns = [
    path('botapi/', Botview.as_view()),
    path('user-tracking/', UserInteractionView.as_view())
]