# from account.serializers import UserSerializer
from .models import QuestionTag, QuestionCategory, Question, Answer
from rest_framework import serializers

from account.models import CustomUserModel

class CreatorSerializer(serializers.ModelSerializer):
    fullname = serializers.SerializerMethodField()
    class Meta:
        model = CustomUserModel
        fields = ('id', 'email', 'first_name','last_name','fullname')
    def get_fullname(self, obj):
        return obj.first_name+' '+obj.last_name
class QuestionTagSerialier(serializers.ModelSerializer):
    class Meta:
        model = QuestionTag
        fields = ['id','name']
    def to_representation(self, instance):
        output = super().to_representation(instance)
        output['created_at'] = instance.created
        output['updated_at'] = instance.updated
        return output

class QuestionCategorySerailzier(serializers.ModelSerializer):
    # creator = CreatorSerializer()
    class Meta:
        model = QuestionCategory
        fields = '__all__'
    def to_representation(self, instance):
        output = super().to_representation(instance)
        creator_id = output['creator']
        creator = CustomUserModel.objects.get(pk=creator_id)
        output['creator']={
            "id":creator.id,
            "email":creator.email,
            "name":creator.fulname,
            "lastLoginTime":creator.last_login,
            "created_at":creator.created_at,
            "updated_at":creator.updated_at ,
        }
        return output
    def to_internal_value(self, data):
        request_user = self.context['request'].user
        data['creator'] = request_user.id
        return super().to_internal_value(data)
    
class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ('id','content',)
class QuestionSerailzier(serializers.ModelSerializer):
    answers = AnswerSerializer(many = True)
    class Meta:
        model = Question
        fields = '__all__'
    def create(self, validated_data):
        answers = validated_data.pop('answers')
        
        hashtags = validated_data.pop('hashtags')
        question = Question.objects.create(**validated_data)
        for item in  hashtags:
            question.hashtags.add(item)
        for answer in answers:
            Answer.objects.create(question=question, **answer)
        return question

    def update(self, instance, validated_data):
        # Lấy dữ liệu về câu trả lời trong request, Xóa câu trả lời cũ, Update câu mới
        updated_answers = validated_data.pop('answers')
        updated_hashtags = validated_data.pop('hashtags')
        instance.hashtags.clear()
        for item in updated_hashtags:
            instance.hashtags.add(item)
        current_answers = Answer.objects.filter(question=instance.id)
        for answer in current_answers:
            answer.delete()
        for item in updated_answers:
            Answer.objects.create(question=instance, **item)
        return super().update(instance, validated_data)
    
    def to_internal_value(self, data):
        request_user = self.context['request'].user
        data['creator'] = request_user.id
        return super().to_internal_value(data)
    def to_representation(self, instance):
        output = super().to_representation(instance)
        # CATEGORY data present  
        category_id = output['category']
        category = QuestionCategory.objects.get(pk = category_id)
        output['category'] = {
            'id':category_id,
            'name':category.name,
            'description':category.description
        }
        # CREATOR data present
        creator_id = output['creator']
        creator = CustomUserModel.objects.get(id= creator_id)
        output['creator'] = {
            "id":creator.id,
            "email":creator.email,
            "name":creator.fulname,
            "lastLoginTime":creator.last_login,
            "created_at":creator.created_at,
            "updated_at":creator.updated_at ,
        }
        # Hashtags data present
        hashtags_id = output['hashtags']
        hashtag_data = []
        for id in  hashtags_id:
            hashtag = QuestionTag.objects.get(id = id)
            hashtag_data.append({
                'id':id,
                'name': hashtag.name,
                'created_at':hashtag.created,
                'updated_at':hashtag.updated
            })

        return output