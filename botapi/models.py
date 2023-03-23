from django.db import models
from django.core.validators import MinValueValidator
# Create your models here.
class UserInteraction(models.Model):
    # user = models.CharField(max_length=255)
    date = models.DateField(auto_now_add=True, unique=True)
    sub_count = models.IntegerField(default=0,validators=[MinValueValidator(0),])
    unsub_count = models.IntegerField(default=0,validators=[MinValueValidator(0),])
    def __str__(self) -> str:
        return "USER TRACK: "+ str(self.date)