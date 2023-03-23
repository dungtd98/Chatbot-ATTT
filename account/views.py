from django.shortcuts import render
from .serializers import UserSerializer, PermissionSerializer, UserLogSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from .models import UserActivityLog
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (ListAPIView, 
                                     RetrieveUpdateDestroyAPIView, 
                                     ListCreateAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework import permissions
from rest_framework import views
from django.http import Http404
UserModel = get_user_model()
# Create your views here.
class Permisisonlist(ListAPIView):
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser,]
    def get_queryset(self):
        permissions = Permission.objects.all()
        if self.request.user.is_superuser is not True:
            user = UserModel.objects.get(id=self.request.user.id)
            user_permissions = user.user_permissions.all()
            group_permissions = Permission.objects.filter(group__user = user)
            permission = user_permissions.union(group_permissions)
            return permission.order_by('pk')
        return permissions.order_by('pk')
    
class PermissionCreate(RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAdminUser,]
# class UserViewset(ModelViewSet):

class UserLogViewset(ModelViewSet):
    queryset = UserActivityLog.objects.all().order_by('-id')
    serializer_class = UserLogSerializer
    permission_classes = [IsAdminUser,] 

class UserListCreateView(ListCreateAPIView,UserActivityLog):
    # queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser,]
    def get_queryset(self):
        queryset = UserModel.objects.all()
        user_name = self.request.query_params.get("name", None)
        user_email = self.request.query_params.get("email", None)
        if user_name is not None:
            queryset.filter(fulname__icontains = user_name)
        if user_email is not None:
            queryset.filter(email__icontains = user_email)
        return queryset

class UserDetailView(views.APIView, UserActivityLog):
    def _get_object(self, pk):
        try:
            return UserModel.objects.get(pk=pk)
        except UserModel.DoesNotExist:
            raise Http404
    def get(self, request, pk):
        object = self._get_object(pk)
        serializer = UserSerializer(object)
        if pk == request.user.id or request.user.is_superuser:
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"detail":"You do not have permission to do this action"}, status=status.HTTP_403_FORBIDDEN)
    
    def patch(self, request, pk):
        object = self._get_object(pk)
        fields_updated = []
        updated_check_fields = ['is_superuser','is_staff']
        for key, value in request.data.items():
            if getattr(object, key) != value:
                fields_updated.append(key)
        if any(item in updated_check_fields for item in fields_updated) and request.user.is_superuser!=True:
            return Response({"detail":"You do not have permission to do this action"}, status= status.HTTP_403_FORBIDDEN)
        serializer = UserSerializer(object, data = request.data, partial=True)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        object = self._get_object(pk)
        if request.user.is_superuser:
            object.delete()
            return Response({"detail":"Delete account successfully"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"detail":"You do not have permission to do this action"}, status=status.HTTP_403_FORBIDDEN)
        