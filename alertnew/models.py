from django.db import models

from django.contrib.auth import get_user_model

from django.contrib.auth.models import Permission, Group
UserModel = get_user_model()
# Create your models here.
class AlertNews(models.Model):
    name = models.CharField(max_length=255, verbose_name='Tên điểm tin/cảnh báo')
    city = models.CharField(max_length=255, verbose_name='Thành phố')
    location = models.CharField(max_length=255, verbose_name='Xã/Phường')
    receiver_range = models.CharField(max_length=255, verbose_name='Phạm vi người nhận')
    ages = models.CharField(max_length=30, verbose_name='Phạm vi tuổi người nhận')
    gender = models.CharField(max_length=20, verbose_name='Giới tính người nhận')
    device = models.CharField(max_length=50, verbose_name='Thiết bị nhận')
    creator = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, null=True)
    TYPE_CHOICES = [
        ('NEWS','Điểm tin ATTT'),
        ('ALERT','Cảnh báo')
    ]
    type = models.CharField(
        max_length=10,
        verbose_name='Loại tin',
        choices=TYPE_CHOICES,
        default='NEWS'
    )
    STATUS_CHOICES = [
        ('PENDING_APPROVE', 'Chờ kiểm duyệt'),
        ('PENDING_SEND', 'Chờ gửi'),
        ('NOT_APPROVED', 'Không được phê duyệt'),
        ('SENT', 'Đã gửi'),
        ('APPROVED', 'Đã qua kiểm duyệt'),
    ]
    status = models.CharField(
        max_length=20,
        verbose_name='Trạng thái kiểm duyệt',
        choices=STATUS_CHOICES,
        default='PENDING_APPROVE'
    )
    
    # is_send = models.DateTimeField(null=True)
    reason_not_approved = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) -> str:
        return self.name[:50]+'...'
    
    class Meta:
        default_permissions  = ()
    
class News(models.Model):
    parent_new = models.ForeignKey(AlertNews, on_delete=models.CASCADE, related_name='news')
    title = models.CharField(max_length=255, blank=False)
    link = models.TextField(blank=False)
    image = models.ImageField(upload_to='images', verbose_name='Ảnh bìa', blank=True)
    source = models.TextField(blank=False)

    NEWS_TYPE = [
        ('MAIN','Tin chính'),
        ('SUB', 'Tin phụ')
    ]
    type = models.CharField(
        verbose_name='Loại tin',
        max_length=7,
        choices=NEWS_TYPE,
        blank=False
    )
    def __str__(self) -> str:
        return self.title
    class Meta:
        default_permissions = ()

class NewSource(models.Model):
    source_new = models.TextField(blank=False)
    source_link = models.TextField()
    STATUS_CHOICES = [
        ('PAUSE','pause'),
        ("FETCHING",'fetching')
    ]
    source_status = models.CharField(
        verbose_name='Trạng thái bản tin',
        max_length=10,
        choices=STATUS_CHOICES,
        default='PAUSE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.source_new[:50]+'...'