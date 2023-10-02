import datetime

import requests

from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, Http404
from django.utils.timezone import localtime
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm, AuthenticationForm
from django.utils import timezone
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status, serializers
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.csrf import csrf_protect
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action, api_view
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import JSONParser, FormParser
from rest_framework.response import Response
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from users.models import UserCustomer, Client, Roles
from users.serializers import UserCustomerListSerializer, UserCustomerSerializer, ClientSerializer, ClientListSerializer, RolSerializer, RolListSerializer, \
    UserPasswordChangeSerializer
from django.shortcuts import render

# Create your views here.

class LoginViewSet(APIView):
    authentication_classes = ()
    
    def post(self, request, *args, **kwargs):
        # Verificar si el usuario ya está autenticado
        #if request.user.is_authenticated:
        #    return Response({'message': 'El usuario ya está autenticado'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            username = UserCustomer.objects.get(username=request.data.get("username"))
        except UserCustomer.DoesNotExist:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

        password = username.password
        print(username)
        print(password)
        print(username.last_login)
        
        if username.last_login is not None:
            return Response({'message': 'El usuario ya está autenticado'}, status=status.HTTP_400_BAD_REQUEST)
            

        if username and password and check_password(request.data["password"], password):
            username.last_login = timezone.now()
            username.save()
            return Response({'access': True, 'data': UserCustomerListSerializer(instance=username).data}, status=status.HTTP_200_OK)
        # Si no, devolver un mensaje de error
        else:
            return Response({'message': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request, id, *args, **kwargs): # Añadir el argumento id
        try:
            user = UserCustomer.objects.get(id=id)
        except UserCustomer.DoesNotExist:
            return Response({'message': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

        # Actualizar el campo is_online del usuario
        user.last_login = None
        user.save()

        return Response({'message': 'Cierre de sesión exitoso'}, status=status.HTTP_200_OK)



class UserCustomerViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsSuperUser)
    queryset = UserCustomer.objects.all()
    serializer_class = UserCustomerListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'rol', 'is_active',)


    def create(self, request, *args, **kwargs):
        serializer = UserCustomerSerializer(data=request.data)

        if serializer.is_valid():
            if serializer.validated_data['email'].startswith('sotomotors'):
                email = serializer.validated_data['email']
            serializer.validated_data['password'] = make_password(serializer.validated_data.get('password'))
            serializer.save()
            return Response(UserCustomerListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserCustomerSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if a new password is provided
            new_password = serializer.validated_data.get('password')
            if new_password:
                # Only encrypt the password if it is different from the current one
                if check_password(new_password, user.password):
                    serializer.validated_data['password'] = user.password
                else:
                    serializer.validated_data['password'] = make_password(
                        new_password)

            serializer.save()

            return Response(UserCustomerListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username  # Obtener el nombre de usuario
        self.perform_destroy(instance)
        message = f"Usuario {username} eliminado"  # Mensaje con la concatenación del nombre de usuario
        return Response({"message": message}, status=status.HTTP_200_OK)


class ClientViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsSuperUser)
    queryset = Client.objects.all()
    serializer_class = ClientListSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name', 'rol', 'is_active',)


    def create(self, request, *args, **kwargs):
        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data.get('password'))
            serializer.save()
            return Response(ClientListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = ClientSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Check if a new password is provided
            new_password = serializer.validated_data.get('password')
            if new_password:
                # Only encrypt the password if it is different from the current one
                if check_password(new_password, user.password):
                    serializer.validated_data['password'] = user.password
                else:
                    serializer.validated_data['password'] = make_password(
                        new_password)

            serializer.save()

            return Response(ClientListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        username = instance.username  # Obtener el nombre de usuario
        self.perform_destroy(instance)
        message = f"Usuario {username} eliminado"  # Mensaje con la concatenación del nombre de usuario
        return Response({"message": message}, status=status.HTTP_200_OK)
    
class ChangePasswordViewSet(APIView):
    def put(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserPasswordChangeSerializer(data=request.data)

        if serializer.is_valid():
            user.password = make_password(serializer.validated_data.get('password'))
            user.save(update_fields=['password'])
            return Response({'message': 'Password changed', "User": user}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RolViewSet(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = RolListSerializer
    queryset = Roles.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filter_fields = ('name',)
    
    def create(self, request, *args, **kwargs):
        serializer = RolSerializer(Roles(), data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(RolListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = RolListSerializer(instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(RolListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)