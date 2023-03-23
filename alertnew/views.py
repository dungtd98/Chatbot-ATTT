from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from .models import AlertNews, News, NewSource
from .serializers import AlertNewsSerializer, NewsSerializer, NewSourceSerializer

from rest_framework.views import APIView
from gnews import GNews
from rest_framework.pagination import PageNumberPagination
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from account.mixins import ActivityLogMixin

from datetime import datetime, timedelta
from .tasks import add_task
# Create your views here.

class DailyNewsViewset(ActivityLogMixin, ModelViewSet):
    serializer_class = AlertNewsSerializer
    def get_queryset(self):
        queryset = AlertNews.objects.all()
        status = self.request.query_params.get('status', None)
        sort_time = self.request.query_params.get('sort_time', None)
        receiver_range = self.request.query_params.get('receiver_range', None)
        creator = self.request.query_params.get('creator', None)
        type = self.request.query_params.get('type', None)
        try:
            creator = creator.split('-')
        except:
            pass
        if type:
            queryset.filter(type=type)
        if status:
            queryset = queryset.filter(status=status)
        if receiver_range:
            queryset = queryset.filter(receiver_range = receiver_range)
        if creator:
            queryset = queryset.filter(creator__id__in=creator)
        
        if sort_time:
            if sort_time == 'DESC':
                queryset = queryset.order_by('-created_at')
            queryset = queryset.order_by('created_at')
        return queryset
    # def list(self, request, *args, **kwargs):
    #     return super().list(request, *args, **kwargs)
    def list(self, request, *args, **kwargs):
        if request.user.has_perm('alertnew.view_list_alertnews'):
            return super().list(request, *args, **kwargs)
        return Response({"detail":"You don't have permission to do this action"}, 
                        status= status.HTTP_403_FORBIDDEN)
    
    def create(self, request, *args, **kwargs):
        if request.user.has_perm('alertnew.create_alertnews'):
            if any(key in request.data.keys() for key in ['is_send','reason_not_approved','moderate_status']):
                return Response({"detail":"Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            request.data['creator']=request.user.id
            return super().create(request, *args, **kwargs)
        return Response({"detail":"You don't have permission to do this action"}, 
                        status= status.HTTP_403_FORBIDDEN)
    
    def retrieve(self, request, *args, **kwargs):
        if request.user.has_perm('alertnew.view_detail_alertnews'):
            return super().retrieve(request, *args, **kwargs)
        return Response({"detail":"You don't have permission to do this action"}, 
                        status= status.HTTP_403_FORBIDDEN)
    
    def check_datetime_format(self, data):
        try:
            return datetime.strptime(data, '%Y-%m-%d %H:%M'), True
        except ValueError:
            return None, False
    
    def process_moder(self, is_send, request, instance_id):
        if request.data['status']!='NOT_APPROVED':
            request.data['reason_not_approved']=None
            if is_send is None:
                request.data['status'] = "APPROVED"
                
            elif is_send == 'send':
                request.data['status'] = "SENT"
            else:
                date_time, check = self.check_datetime_format(is_send)
                date_time = date_time if date_time>datetime.now() else datetime.now()
                if check:
                    add_task.apply_async((instance_id,),eta=date_time)
                    request.data['status']='PENDING_SEND'
                    print('Hẹn giờ gửi', request.data['is_send'])
                else:
                    request.data.clear()
        return request
    
    def update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        instance = self.get_object()
        keys_in_request_data = set(request.data.keys())
        mod_accepted_fields = {'is_send','reason_not_approved','status'}
        if request.user.has_perm('alertnew.moderate_alertnews'):
            if keys_in_request_data.difference(mod_accepted_fields):
                return Response({'detail':"Bad request, you can not update any other fields beside: is_send, reason_not_approved, status"},
                                status=status.HTTP_400_BAD_REQUEST)
            is_send = request.data.get('is_send',None)
            request = self.process_moder(is_send, request, instance.id)
            if request.data =={}:
                return Response({"detail": "Bad request"}, status=status.HTTP_400_BAD_REQUEST)
            return super().update(request, *args, **kwargs)
        
        if request.user.has_perm('alertnew.update_alertnews') \
            and instance.creator.id==request.user.id and instance.status not in['APPROVED','SENT','PENDING_SEND']:
            if any(key in keys_in_request_data for key in mod_accepted_fields):
                return Response({'detail':"Bad request, you can not update: is_send, reason_not_approved, status"}, 
                                status=status.HTTP_400_BAD_REQUEST)
            return super().update(request, *args, **kwargs)
            
        return Response({"detail":"You don't have permission to do this action"}, 
                        status= status.HTTP_403_FORBIDDEN)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status not in ['APPROVED', 'PENDING_SEND','SENT']:
            if request.user.has_perm('alertnew.delete_no_approved_alertnews'):
                self.perform_destroy(instance)
                return Response({'message':"Delete daily news successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail":"You don't have permission to do this action"}, 
                        status= status.HTTP_403_FORBIDDEN)
    
class AlertNewsViewset(ActivityLogMixin, ModelViewSet):
    serializer_class = AlertNewsSerializer
    def get_queryset(self):
        queryset = AlertNews.objects.filter(type='ALERT')
        status = self.request.query_params.get('status', None)
        sort_time = self.request.query_params.get('sort_time', None)
        receiver_range = self.request.query_params.get('receiver_range', None)
        creator = self.request.query_params.get('creator', None)
        try:
            creator = creator.split('-')
        except:
            pass
        if status:
            queryset = queryset.filter(status=status)
        if receiver_range:
            queryset = queryset.filter(receiver_range = receiver_range)
        if creator:
            queryset = queryset.filter(creator__id__in=creator)
        if sort_time:
            if sort_time == 'DESC':
                queryset = queryset.order_by('-created_at')
            queryset = queryset.order_by('created_at')
        return queryset

class NewSourceList(APIView, PageNumberPagination, ActivityLogMixin):
    # @method_decorator(cache_page(60*60))
    def get(self, request, format=None, *args, **kwargs):
        queryset = NewSource.objects.all().order_by('-created_at')
        queryset = self.paginate_queryset(queryset, request, view=self)
        serializer = NewSourceSerializer(queryset, many=True)
        return self.get_paginated_response(serializer.data)
        
    def post(self, request, *args, **kwargs):
        gg_news = GNews()
        gg_news.language=request.data['language']
        gg_news.country =request.data['country']
        gg_news.start_date=(1,1,2023)
        response = gg_news.get_news(request.data['content'])
        for data in response:
            print({'url':data['url'],
                   'title':data['title']})
            NewSource.objects.create(
                source_new = data['title'],
                source_link = data['url'],  
            )
        return Response(response)