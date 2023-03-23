from celery import Celery
import logging
from .models import AlertNews
from django.db.models import F, Case, When
app = Celery('core', broker='redis://redis:6379/1')

@app.task
def add_task(id):
    instance = AlertNews.objects.get(pk=id)
    if instance.status in ['PENDING_SEND', 'SENT']:
        instance.status = 'SENT'
    instance.save()
    logging.info('RUN TASK SEND ALERTNEWS')
    
