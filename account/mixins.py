import logging
from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from rest_framework.exceptions import ValidationError
from .models import UserActivityLog

class ActivityLogMixin:
    log_messenge = None
    @staticmethod
    def _get_user(request):
        return request.user if request.user.is_authenticated else None
    def _write_log(self, request, response):
        response_status = response.status_code
        request_user = self._get_user(request)
        if request_user:
            logging.info('Start log entry')
            data = {
                "user":request_user,
                "response_status":response_status,
                "user_agent":request.META.get('HTTP_USER_AGENT'),
                "path":request.path,
                "ipAddress":request.META.get('REMOTE_ADDR'),
                "request_body":request.data,
                "request_method":request.method
            }
        UserActivityLog.objects.create(**data)
    def finalize_response(self, request, *args, **kwargs):
        response = super().finalize_response(request, *args, **kwargs)
        self._write_log(request, response)
        return response