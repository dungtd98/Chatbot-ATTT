from django.apps import AppConfig
# from .signals import reset_login_failures, raise_user_auth_failed_exceptions
# from django.contrib.auth.signals import user_logged_in
# from axes.signals import user_locked_out

class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'
    def ready(self):
        from account import signals
        # return super().ready()
