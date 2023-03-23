from celery import shared_task
from .models import UserInteraction
from datetime import datetime
@shared_task
def scheduled_create_user_track_data():
    today = datetime.today().date()
    UserInteraction.objects.get_or_create(
        date = today
    )
    print("This is a scheduled task")