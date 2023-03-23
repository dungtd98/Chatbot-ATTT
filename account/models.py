from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth import get_user_model
# Create your models here.
class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password=None, **kwargs):
        
        if not email:
            raise ValueError('email is required')
        user = self.model(
            email = email,
            **kwargs
        )
        email = self.normalize_email(email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_user(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', False)
        kwargs.setdefault('is_staff', False)
        return self._create_user(email, password, **kwargs)
    
    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Admin must be superuser')
        if kwargs.get('is_staff') is not True:
            raise ValueError('Admin must be staff')
        return self._create_user(email, password, **kwargs)
    
class CustomUserModel(AbstractBaseUser, PermissionsMixin):
    # username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    fulname = models.CharField(max_length=100, blank=True, verbose_name='Họ và tên')
    
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ROLE_CHOICES = [
        ('PROFESSIONAL','Cán bộ chuyên môn'),
        ('MODERATOR','Cán bộ kiểm duyệt'),
        ('LEADER', 'Lãnh đạo'),
        ('ADMIN','Cán bộ quản trị hệ thống')
    ]
    role= models.CharField(choices=ROLE_CHOICES, max_length=30, default='PROFESSIONAL')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()
    def __str__(self) -> str:
        return self.email
    
    class Meta:
        default_permissions=()

UserModel = get_user_model()

class UserActivityLog(models.Model):
    user_agent = models.CharField(max_length=255)
    ipAddress = models.CharField(max_length=100)
    path = models.CharField(max_length=255)
    response_status = models.CharField(max_length=10)
    request_method = models.CharField(max_length=10)
    location = models.CharField(max_length=255, null=True)
    browser = models.CharField(max_length=255, null=True)
    device = models.CharField(max_length=255, null=True)
    request_body = models.JSONField(default=dict)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='user_log')
    def __str__(self) -> str:
        return f'{self.request_method} by {self.user.email} on {self.time}'

def add_user_permisson_group(permission_list, instance):
    """Add user permission when create user base on their role"""
    for permission in permission_list:
        instance.user_permissions.add(Permission.objects.get(codename=permission))  
    instance.user_permissions.add()
@receiver(post_save, sender = CustomUserModel)
def set_userpermission(sender, instance, created, **kwargs):
    """Create user permission when created"""
    # print("Các quyền của user", instance.get_all_permissions())
    if created is not True:
        return 
    if instance.role == 'PROFESSIONAL':
        permission_list = [# Quyền liên quan đến bản tin/Tin báo 
                            'create_alertnews','view_detail_alertnews','view_list_alertnews',
                            'update_alertnews','delete_no_approved_alertnews',
                            # Quyền liên quan đến nhóm câu hỏi
                            "create_question_category", "detail_question_category", 'list_question_category',
                            'delete_question_category', "update_question_category",
                            # Quyền lien quan đến câu hỏi
                            "create_question","detail_question","list_question",
                            "delete_question","update_question"]
        group = Group.objects.get(name = 'CONTENT_CREATOR')
        group.user_set.add(instance)
        add_user_permisson_group(permission_list, instance)

    if instance.role == 'MODERATOR':
        permission_list =['moderate_alertnews','view_detail_alertnews', 'view_list_alertnews']
        group = Group.objects.get(name = 'CONTENT_MODERATOR')
        group.user_set.add(instance)
        add_user_permisson_group(permission_list, instance)
    if instance.role == 'LEADER':
        permission_list = [
                "moderate_alertnews", "create_alertnews", "view_detail_alertnews",
                "view_list_alertnews", "update_alertnews", "delete_no_approved_alertnews",
                "create_question_category", "detail_question_category", "list_question_category",
                "delete_question_category", "update_question_category",
                "create_question", "list_question", "detail_question",
                "delete_question", "update_question", "update_question_status",
                "create_hashtags", "list_hashtags", "retrieve_hashtags",
                "update_hashtags", "delete_hashtags",
        ]
        group = Group.objects.get(name = 'CONTENT_MODERATOR')
        group.user_set.add(instance)
        add_user_permisson_group(permission_list, instance)