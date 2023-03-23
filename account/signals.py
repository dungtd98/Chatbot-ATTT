from django.dispatch import receiver

from axes.signals import user_locked_out
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.signals import user_logged_in, user_login_failed
from axes.models import AccessFailureLog
from .models import UserActivityLog
@receiver(user_locked_out)
def raise_permission_denied(*args, **kwargs):
    raise PermissionDenied("Too many failed login attempts")

def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )

@receiver(user_logged_in)
def reset_user_login_failure(sender, request, user, *args, **kwargs):
    message = f"{user.fulname} is logged in with ip:{get_client_ip(request)}"
    # UserActivityLog.objects.create(actor=user, action_type=LOGIN, remarks=message)
    
@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}"
    # UserActivityLog.objects.create(action_type=LOGIN_FAILED, remarks=message)
