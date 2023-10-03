from django.urls import re_path
from rest_framework.routers import DefaultRouter


from chats.views import ConversacionsViewSet

router = DefaultRouter()

router.register(r'chats', ConversacionsViewSet)


urlpatterns = [
    # re_path(r'^user_offline/$', UserOfflineViewSet.as_view(), name='user_offline'),
    # re_path(r'^blocked_user/(?P<pk>[0-9]+)/$', Blocked_UserViewSet.as_view(), name='blocked_user'),
]

urlpatterns += router.urls