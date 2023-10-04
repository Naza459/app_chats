from django.urls import re_path, path
from rest_framework.routers import DefaultRouter


from chats.views import ConversacionsUsuarioViewSet, ConversacionsClienteViewSet

router = DefaultRouter()

router.register(r'chats_usuario', ConversacionsUsuarioViewSet)
router.register(r'chats_Cliente', ConversacionsClienteViewSet)


urlpatterns = [
    #path('chat_socket/', chat_socket, name='chat_socket'),
    # re_path(r'^blocked_user/(?P<pk>[0-9]+)/$', Blocked_UserViewSet.as_view(), name='blocked_user'),
]

urlpatterns += router.urls