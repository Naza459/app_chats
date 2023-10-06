import urllib3
import ssl
import socketio
import time
from geventwebsocket.handler import WebSocketHandler
from gevent.pywsgi import WSGIServer
from socketio import Server
from django.http import HttpResponseServerError
import datetime
import threading
import requests
import gevent



from django.http import JsonResponse
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password, check_password
from rest_framework import generics
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
from chats.models import Conversations, Catalogue, RoomChats
from chats.serializers import ConversationSerializer, ConversationListSerializer, ConversationSerializer, RoomSerializer, RoomListSerializer
from chats.consumers import ConversationsConsumer
from users.models import UserCustomer, Client, Roles
from django.shortcuts import render
from socketio import Client
from socketio import AsyncServer, AsyncNamespace, ASGIApp
from socketio import Namespace
#from chats.socket import socketIO
from socketio.exceptions import ConnectionRefusedError
sio = socketio.Client()
socketIO = Client()
connected = False


def connect_to_socket():
    global connected
    if not connected:
        try:
            socketIO.connect('http://localhost:4000/')
            connected = True
        except ConnectionError:
            # Manejar cualquier excepción de conexión aquí
            pass

class ConversacionsUsuarioViewSet(ModelViewSet):
    queryset = Conversations.objects.all()
    serializer_class = ConversationListSerializer

    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user']
            identify = serializer.validated_data['identify']
            client_id = serializer.validated_data.get('client')

            message = {
                'messages': serializer.validated_data.get('messages'),
                'type_messages': serializer.validated_data.get('type_messages'),
                'file': serializer.validated_data.get('file'),
                'identify': identify,
                'user': user_id.to_json(),
                'client': client_id.to_json()
            }

            response_data = None
            response_received = threading.Event()
            
            def on_disconnect():
                print('Se ha perdido la conexión con el servidor Socket.IO. Intentando reconectar...')
                time.sleep(5)  # Espera 5 segundos antes de intentar la reconexión
                socketIO.connect()  # Intenta reconectar

            def on_response(data):
                nonlocal response_data
                response_data = data
                response_received.set()

            connect_to_socket()

            socketIO.on('mensajeCliente', on_response)
            socketIO.emit('mensajeUsuario', message)
            print('Emitió el mensaje')

            # Espera la respuesta del servidor Socket.IO durante 5 segundos
            response_received.wait(timeout=5)

            if serializer.validated_data.get('is_closed') == True:
                #socketIO.disconnect()
                serializer.save()
                Conversations.objects.all().delete()
                return Response(ConversationSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
                
            serializer.save()

            if response_data is not None:
                print('Respuesta del servidor Socket.IO:', response_data)
                return Response(ConversationSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Tiempo de espera agotado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# ...


class ConversacionsClienteViewSet(ModelViewSet):
    queryset = Conversations.objects.all()
    serializer_class = ConversationSerializer

    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():
            user_id = serializer.validated_data['user']
            identify = serializer.validated_data['identify']
            client_id = serializer.validated_data.get('client')

            message = {
                'messages': serializer.validated_data.get('messages'),
                'type_messages': serializer.validated_data.get('type_messages'),
                'file': serializer.validated_data.get('file'),
                'identify': identify,
                'user': user_id.to_json(),
                'client': client_id.to_json()
            }

            response_data = None
            response_received = threading.Event()

            def on_response(data):
                nonlocal response_data
                response_data = data
                response_received.set()

            connect_to_socket()

            socketIO.on('mensajeUsuario', on_response)
            socketIO.emit('mensajeCliente', message)
            print('Emitió el mensaje')

            # Espera la respuesta del servidor Socket.IO durante 5 segundos
            response_received.wait(timeout=5)

            # socketIO.disconnect()
            # print('Entro por desconectar')
                
            serializer.save()

            if response_data is not None:
                print('Respuesta del servidor Socket.IO:', response_data)
                return Response(ConversationSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Tiempo de espera agotado'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RoomChatsViewset(ModelViewSet):
    #permission_classes = (IsAppAuthenticated, IsAppStaff, IsAuthenticated, IsCompanyPermission)
    serializer_class = RoomListSerializer
    queryset = RoomChats.objects.all()
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    filter_fields = ('name',)
    
    def create(self, request, *args, **kwargs):
        serializer = RoomSerializer(RoomChats(), data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(RoomListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = RoomListSerializer(instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(RoomListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetChatsUsuario(generics.ListAPIView):
    
    serializer_class = ConversationSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        client_id = self.request.query_params.get('client_id')
        # Obtener la sala de chats correspondiente

        room = RoomChats.objects.get(id=room_id)
        queryset = Conversations.objects.filter(client_id=client_id, room=room, identify='cliente')
        return queryset

    def get(self, request, *args, **kwargs):
        connect_to_socket()
        room_id = self.request.query_params.get('room_id')
        # Obtener la sala de chats correspondiente
        room = RoomChats.objects.get(id=room_id)
        # Unirse a la sala correspondiente
        socketIO.emit('join_room', room.name)

        response_received = threading.Event()
        response_data = None

        def on_new_message(data):
            nonlocal response_data
            response_data = data
            response_received.set()

        socketIO.on('mensajeCliente', on_new_message)

        response_received.wait(timeout=5)

        if response_data:
            print('Mensaje en tiempo real recibido:', response_data)

        # Realizar cualquier otra lógica necesaria para el procesamiento de la respuesta

        socketIO.disconnect()

        queryset = self.get_queryset()  # Obtener el queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class GetChatsCliente(generics.ListAPIView):
    serializer_class = ConversationSerializer

    def get_queryset(self):
        room_id = self.request.query_params.get('room_id')
        user_id = self.request.query_params.get('user_id')
        # Obtener la sala de chats correspondiente
        
        room = RoomChats.objects.get(id=room_id)
        queryset = Conversations.objects.filter(user_id=user_id, room=room, identify = 'usuario')
        return queryset

    def get(self, request, *args, **kwargs):
        connect_to_socket()
        room_id = self.request.query_params.get('room_id')
        # Obtener la sala de chats correspondiente
        room = RoomChats.objects.get(id=room_id)
        # Unirse a la sala correspondiente
        socketIO.emit('join_room', room.name)

        response_received = threading.Event()
        response_data = None

        def on_new_message(data):
            nonlocal response_data
            response_data = data
            response_received.set()

        socketIO.on('mensajeUsuario', on_new_message)
        

        response_received.wait(timeout=5)

        if response_data:
            print('Mensaje en tiempo real recibido:', response_data)

        # Realizar cualquier otra lógica necesaria para el procesamiento de la respuesta

        socketIO.disconnect()

        queryset = self.get_queryset()  # Obtener el queryset
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
