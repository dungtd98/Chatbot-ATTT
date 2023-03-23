from django.contrib import admin
from .models import AlertNews, News, NewSource
# Register your models here.

admin.site.register(NewSource)
admin.site.register(AlertNews)
admin.site.register(News)