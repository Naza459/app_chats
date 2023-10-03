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
from chats.models import Conversations, Catalogue
from chats.serializers import ConversationSerializer, ConversationListSerializer
from chats.consumers import ConversationsConsumer
from users.models import UserCustomer, Client, Roles
from django.shortcuts import render
from socketio import AsyncServer
from socketio import Namespace
from socketio.exceptions import ConnectionRefusedError

# Create your views here.


class ConversacionsNamespace(Namespace):
    async def on_connect(self, sid, environ):
        # Obtener el usuario y el cliente de los parámetros de la URL
        user_id = environ["QUERY_STRING"].split("=")[1]
        client_id = environ["QUERY_STRING"].split("=")[3]

        # Guardar los identificadores en los atributos del namespace
        self.user_id = user_id
        self.client_id = client_id

        # Agregar el namespace al grupo de comunicación del usuario y el cliente
        await self.enter_room(f'user_{user_id}')
        await self.enter_room(f'client_{client_id}')

    async def on_message(self, sid, data):
        # Procesar el mensaje recibido desde el cliente
        # ...

        # Enviar una respuesta al cliente
        await self.emit('message', 'Respuesta del servidor WebSocket')

    async def on_disconnect(self, sid):
        # Manejar la desconexión del cliente
        # ...

        # Eliminar el namespace del grupo de comunicación del usuario y el cliente
        await self.leave_room(f'user_{self.user_id}')
        await self.leave_room(f'client_{self.client_id}')


class ConversacionsViewSet(ModelViewSet):
    queryset = Conversations.objects.all()
    serializer_class = ConversationListSerializer
    #authentication_classes = [TokenAuthentication]
    #permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = ConversationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            # Obtener el usuario y el cliente de la conversación
            user_id = serializer.validated_data.get('user')
            client_id = serializer.validated_data.get('client')

            # Enviar mensaje al WebSocket con los identificadores del usuario y el cliente
            message = {
                'messages': serializer.validated_data.get('messages'),
                'type_messages': serializer.validated_data.get('type_messages'),
                'file': serializer.validated_data.get('file'),
                'user': user_id,
                'client': client_id,
            }

            try:
                async def send_message():
                    await server.emit('message', message, room=f'user_{user_id}')
                    await server.emit('message', message, room=f'client_{client_id}')

                server = request.app['socketio_server']
                request.app.loop.create_task(send_message())
            except (ConnectionRefusedError, AttributeError):
                # Manejar excepciones si el servidor Socket.IO no está disponible
                pass

            return Response(ConversationListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        modulo_instance = self.get_object()

        serializer = ConversationListSerializer(
            instance=modulo_instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(ConversationListSerializer(instance=serializer.instance).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


async def chat_socket(request):
    # Obtener el usuario y el cliente de los parámetros de la URL
    user_id = request.GET.get('user')
    client_id = request.GET.get('client')

    if user_id is None or client_id is None:
        return HttpResponse('Missing user_id or client_id parameter', status=400)

    # Crear una instancia del servidor Socket.IO
    server = AsyncServer()

    # Configurar el namespace para las conversaciones
    chat_namespace = ConversacionsNamespace('/chats')
    server.register_namespace(chat_namespace)

    # Obtener el entorno WSGI de la solicitud de Django
    environ = request.environ

    try:
        # Iniciar el servidor Socket.IO
        await server.trigger_event('connect', chat_namespace, sid=None, environ=environ)
    except ConnectionRefusedError:
        return HttpResponse('Failed to connect to the Socket.IO server', status=500)

    # Mantener la conexión WebSocket abierta
    await server.trigger_event('disconnect', chat_namespace, sid=None)

    # Devolver una respuesta vacía
    return HttpResponse()
