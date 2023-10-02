"""
WSGI config for chats_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.urls import path
from channels.middleware import WebsocketMiddlewareStack
from chats.consumers import ConversationsConsumer

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chats_project.settings')

# application = get_wsgi_application()

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(
                [
                    # Aquí agregas tus rutas de WebSocket
                    path("ws/conversations/", ConversationsConsumer.as_asgi()),
                ]
            )
        ),
    }
)
