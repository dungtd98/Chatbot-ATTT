from django import forms
from django.contrib.auth import get_user_model
from django.contrib import admin
from django.contrib.auth.models import Permission
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

UserModel = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = UserModel
        fields = '__all__'
    
