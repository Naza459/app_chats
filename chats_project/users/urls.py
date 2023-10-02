from django.urls import re_path
from rest_framework.routers import DefaultRouter


from users.views import LoginViewSet,  LogoutView, ClientViewSet, UserCustomerViewSet, RolViewSet, ChangePasswordViewSet, LoginClientViewSet, LogoutClientView

router = DefaultRouter()

router.register(r'usuarios', UserCustomerViewSet)
router.register(r'clientes', ClientViewSet)
router.register(r'rol', RolViewSet)

urlpatterns = [
    re_path(r'^login/', LoginViewSet.as_view(), name='login'),
    re_path(r'^logout/(?P<id>[0-9]+)/', LogoutView.as_view(), name='logout'),
    
    re_path(r'^login_cliente/', LoginClientViewSet.as_view(), name='login_cliente'),
    re_path(r'^logout_cliente/(?P<id>[0-9]+)/', LogoutClientView.as_view(), name='logout_cliente'),
    #re_path(r'^login/$', LoginViewSet, name='login'),
    #re_path(r'^users/', UserViewSet.as_view(), name='users'),
    re_path(r'^change_password/(?P<pk>[0-9]+)/$', ChangePasswordViewSet.as_view(), name='change_password'),
    # re_path(r'^user_offline/$', UserOfflineViewSet.as_view(), name='user_offline'),
    # re_path(r'^blocked_user/(?P<pk>[0-9]+)/$', Blocked_UserViewSet.as_view(), name='blocked_user'),
]

urlpatterns += router.urls