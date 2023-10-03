from django.urls import re_path
from chats.consumers import ConversationsConsumer

websocket_urlpatterns = [
    re_path(r'ws/conversations/$', ConversationsConsumer.as_wsgi()),
]
