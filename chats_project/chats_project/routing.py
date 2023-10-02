from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from django.urls import path
from chats.consumers import ConversationsConsumer

application = ProtocolTypeRouter(
    {
        'http': get_asgi_application(),
        'websocket': AuthMiddlewareStack(
            URLRouter(
                [
                    path('ws/conversations/', ConversationsConsumer.as_asgi()),
                ]
            )
        ),
    }
)
