from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import CustomUserChangeForm, CustomUserCreationForm
from django.contrib.auth.models import Permission
UserModel = get_user_model()
# Register your models here.

class UserAdmin(BaseUserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    list_display = ('email', 'is_active')

    fieldsets = (
        ('Account',{'fields':('email', 'is_active','is_superuser','is_staff')}),
        ('Personal Infor',{'fields':('fulname','groups','user_permissions','role',)}),   
    )
    add_fieldsets = (
        ('Account',{'fields':('email','password1','password2', 'is_active', 'is_superuser','is_staff')}),
        ('Personal Infor',{'fields':('fulname','role')})
    )
    search_fields = ['email', 'fulname']
    ordering = ['email',]
admin.site.register(UserModel, UserAdmin)
admin.site.register(Permission)