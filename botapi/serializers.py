from rest_framework.serializers import ModelSerializer
from .models import UserInteraction

class UserInteractionTrackingSerializer(ModelSerializer):
    class Meta:
        model = UserInteraction
        fields = '__all__'
