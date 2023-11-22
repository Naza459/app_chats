from django.urls import re_path, path
from rest_framework.routers import DefaultRouter


from chats.views import ConversacionsUsuarioViewSet, ConversacionsClienteViewSet, GetChatsUsuario, GetChatsCliente, CatalogueViewSet, ReportCatalogueViewSet

router = DefaultRouter()

router.register(r'chats_usuario', ConversacionsUsuarioViewSet)
router.register(r'chats_Cliente', ConversacionsClienteViewSet)
router.register(r'catalogue', CatalogueViewSet)
router.register(r'report_catalogue', ReportCatalogueViewSet)


urlpatterns = [
    #path('chat_socket/', chat_socket, name='chat_socket'),
    re_path(r'^get_chat_usuario/$', GetChatsUsuario.as_view(), name='get_chat_usuario'),
    re_path(r'^get_chat_cliente/$', GetChatsCliente.as_view(), name='get_chat_cliente'),
    #re_path('catalogue/', ReportCatalogueViewSet.as_view(), name='catalogue-list'),
]

urlpatterns += router.urls