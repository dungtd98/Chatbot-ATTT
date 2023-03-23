from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
UserModel = get_user_model()


@receiver(post_save, sender = UserModel)
def set_userpermission(sender, instance, **kwargs):
    if instance.role == 'PROFESSIONAL':
        print('Chuyên viên nghiệp vụ khởi tạo')
