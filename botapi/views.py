from django.shortcuts import render
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
import json

import openai
from .ultis import *

from question.models import Question
from django.contrib.postgres.search import TrigramSimilarity
from .models import UserInteraction
from datetime import datetime
from django.db.models import F
from .serializers import UserInteractionTrackingSerializer
# Create your views here.

openai.api_key = get_token_openai()

class Botview(APIView):
    permission_classes = [AllowAny,]
    def post(self, request):
        viber = Api(BotConfiguration(
                  name='PythonSampleBot',
                  avatar='',
                  auth_token='50a7f3efada7e7b8-ad6839d85746bac8-1274d79a9557e0b1'
                ))
        # xử lý yêu cầu từ Viber bot
        
        if request.data:
            viber_request = viber.parse_request(json.dumps(request.data))
            today = datetime.today().date()
            if isinstance(viber_request, ViberSubscribedRequest) or isinstance(viber_request, ViberConversationStartedRequest):  
                user_tracking, __ = UserInteraction.objects.get_or_create(date=today)
                user_tracking.sub_count = F('sub_count')+1
                user_tracking.save()
                print("VIBER SUBCRIBED")
                message = TextMessage(text="Xin chào, chatbot ATTT có thể giúp gì cho bạn?")
                viber.send_messages(viber_request.user.id, [message])
            if isinstance(viber_request, ViberUnsubscribedRequest):
                user_tracking,__ = UserInteraction.objects.get_or_create(date=today)
                user_tracking.unsub_count = F('unsub_count')+1
                user_tracking.save()
                print("VIBER UNSUBCRIBED", viber_request)
            if isinstance(viber_request, ViberMessageRequest):
                input = request.data['message']['text']
                messages = self.__query_question(input)
                for item in messages:
                    message = TextMessage(text=item)
                    viber.send_messages(viber_request.sender.id, [message])

        return Response(status=status.HTTP_200_OK)
    
    def __query_question(self, input):
        question = Question.objects.annotate(
                similarity = TrigramSimilarity('question', input),
            ).filter(similarity__gt=0.3).order_by('-similarity').first()
        messages = []
        if question and question.answers.exists():
            for answer in question.answers.all():
                messages.append(answer.content)
        else:
            messages.append(Botview.get_chatGPT_response(input+'trả lời tiếng việt',
                                                         model='gpt-3.5-turbo',max_tokens=500, temperature=0.7))
        return messages
        
    
    @staticmethod
    def get_chatGPT_response(prompt, model='gpt-3.5-turbo',max_tokens=500, temperature=0.5):
        response = openai.ChatCompletion.create(
            model=model, 
            messages=[
                        {"role": "user", "content": prompt}
                    ],
            max_tokens=max_tokens,
            temperature = temperature,
            stop=['.']
        )
        return response.get("choices")[0]['message']['content']

class UserInteractionView(APIView):
    permission_classes = [IsAdminUser,]
    def get(self, request, *ags,**kwargs):
        queryset = UserInteraction.objects.all()
        start_date = request.query_params.get('started_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lt=start_date)
        serializer = UserInteractionTrackingSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)   