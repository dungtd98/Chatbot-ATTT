from rest_framework import serializers
from .models import CustomUserModel, UserActivityLog
from django.contrib.auth.models import Permission

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'

class UserLogSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        output= super().to_representation(instance)
        user = CustomUserModel.objects.get(pk=output['user'])
        output['user']={
            'id':user.id,
            'email':user.email,
            'role':user.get_role_display(),
        }
        return output
    
    class Meta:
        model = UserActivityLog
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUserModel
        fields = '__all__'
    def validate(self, attrs):
        if attrs['confirm_password'] != attrs['password']:
            raise serializers.ValidationError('password not match')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        return super().create(validated_data)
    # def to_representation(self, instance):
    #     output= super().to_representation(instance)
    #     output.pop('confirm_password')
    #     return output