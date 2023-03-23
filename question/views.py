from django.shortcuts import render, get_object_or_404
from .serializers import (QuestionTagSerialier, 
                          QuestionCategorySerailzier, 
                          QuestionSerailzier)
from .models import (QuestionTag, 
                     QuestionCategory, 
                     Question)
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from account.mixins import ActivityLogMixin
# Create your views here.
class QuestionTagViewset(ModelViewSet, ActivityLogMixin):
    queryset = QuestionTag.objects.all()
    serializer_class = QuestionTagSerialier
    def list(self, request, *args, **kwargs):
        if request.user.has_perm('question.list_hashtags'):
            return super().list(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
                        
    def create(self, request, *args, **kwargs):
        if request.user.has_perm('question.create_hashtags'):
            return super().create(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, *args, **kwargs):
        if request.user.has_perm('question.retrieve_hashtags'):
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        if request.user.has_perm('question.update_hashtags'):
            return super().update(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    def destroy(self, request, *args, **kwargs):
        if request.user.has_perm('question.delete_hashtags'):
            return super().destroy(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
class QuestionCategoryViewset(ModelViewSet, ActivityLogMixin): 
    serializer_class = QuestionCategorySerailzier
    def get_queryset(self):
        queryset = QuestionCategory.objects.all()
        sort_time = self.request.query_params.get('sort_time', None)
        keyword = self.request.query_params.get('keyword', None)
        if sort_time is not None and sort_time=='DESC':
            queryset = queryset.order_by('-created')
        else:
            queryset = queryset.order_by('created')
        if keyword is not None:
            queryset = queryset.filter(name__icontains=keyword)
        return queryset

    def create(self, request, *args, **kwargs):
        # print(request.user.get_all_permissions())
        user_perm = request.user.has_perm('question.create_question_category')
        if user_perm:
            return super().create(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    def retrieve(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.detail_question_category')
        if user_perm:
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    def list(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.list_question_category')
        if user_perm:
            return super().list(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def __check_creator(self, request, obj_id):
        request_userID = request.user
        object = get_object_or_404(QuestionCategory, id=obj_id)
        return request_userID == object.creator

    def destroy(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.delete_question_category')
        object_id = self.kwargs['pk']
        check_creator = self.__check_creator(request, object_id)
        if (user_perm and check_creator) or request.user.is_superuser:
            return super().destroy(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.update_question_category')
        object_id = self.kwargs['pk']
        check_creator = self.__check_creator(request, object_id)
        if (user_perm and check_creator) or request.user.is_superuser:
            return super().update(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN) 
class QuestionViewset(ModelViewSet, ActivityLogMixin):
    queryset = Question.objects.all()
    serializer_class = QuestionSerailzier

    def get_queryset(self):
        queryset = Question.objects.all().order_by('-created')
        sort_time = self.request.query_params.get('sort_time', None)
        keyword = self.request.query_params.get('keyword',None)
        categories = self.request.query_params.get('categories', None)
        created_from = self.request.query_params.get('created_from', None)
        created_to = self.request.query_params.get('created_to', None)
        hashtag = self.request.query_params.get('hashtag', None)
        if categories is not None:
            queryset = queryset.filter(category__id__in = categories)
        if hashtag is not None:
            queryset = queryset.filter(hashtag__id__in = hashtag)
        if keyword is not None:
            queryset = queryset.filter(question__icontains = keyword)
        if created_from and created_to:
            queryset = queryset.filter(created__range = (created_from, created_to))
        if sort_time is not None and sort_time=='ASC':
            queryset = queryset.order_by('created')
        return queryset

    def create(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.create_question')
        if user_perm:
            return super().create(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)

    def retrieve(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.detail_question')
        if user_perm:
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def list(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.list_question')
        if user_perm:
            return super().list(request, *args, **kwargs)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        user_perm = request.user.has_perm('question.delete_question')
        if user_perm:
            instance = self.get_object()
            self.perform_destroy(instance)
            return Response({'message': 'Object deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()      
        user_perm = request.user.has_perm('question.update_question')
        check_creator = request.user == instance.creator
        update_status_permission = self.__check_update_status(instance, request)
        if (user_perm and check_creator):
            if update_status_permission:
                return super().update(request, *args, **kwargs)            
        return Response({"detail":"You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN)
    
    def __check_update_status(self, instance, request):
        # Check if user have permission
        # Check if status field is request changed in request data
        user_change_perm = request.user.has_perm('question.update_question_status')
        current_data = instance.type
        request_data = request.data['type']
        if user_change_perm is not True:
            if current_data !=request_data:
                return False
        return True


