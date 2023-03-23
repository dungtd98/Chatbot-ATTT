from .models import AlertNews, News, NewSource
from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()
class NewsSerializer(serializers.ModelSerializer):
    image = serializers.URLField()
    class Meta:
        model = News
        fields = ['id','title','link','image','source','type']

class AlertNewsSerializer(serializers.ModelSerializer):
    """ Thiết kế cho cán bộ nghiệp vụ, không cho phép thay đổi trạng thái kiểm duyệt """
    news = NewsSerializer(many=True)
    class Meta:
        model = AlertNews
        # fields = ['id','news', 'name', 'city', 'location', 'receiver_range','ages','gender', 'device']
        fields = '__all__'

    def create(self, validated_data):
        sub_news_data = validated_data.pop('news')
        safe_new = AlertNews.objects.create(**validated_data)
        for data in sub_news_data:
            News.objects.create(parent_new=safe_new, **data)
        return safe_new
    
    def update(self, instance, validated_data):
        sub_news_data = validated_data.pop('news',None)
        sub_news = News.objects.filter(parent_new = instance.id)
        if sub_news_data:
            for new in sub_news:
                new.delete()
            for data in sub_news_data:
                News.objects.create(parent_new = instance, **data)
        return super().update(instance, validated_data)
    def to_representation(self, instance):
        output = super().to_representation(instance)
        creator = UserModel.objects.get(pk=output['creator'])
        output['creator']={
            "id": creator.id,
            "email":creator.email,
            "name":creator.fulname
        }
        return output
class NewSourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewSource
        fields = '__all__'