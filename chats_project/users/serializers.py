from django.conf import settings
from rest_framework import serializers
from users.models import UserCustomer, Client, Roles

class RolSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Roles
        fields = ('__all__')

class RolListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Roles
        fields = ('__all__')
        
class UserCustomerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = UserCustomer
        fields = ('__all__')

class UserCustomerListSerializer(serializers.ModelSerializer):
    rol = RolListSerializer(many=False, read_only=True)
    class Meta:
        model = UserCustomer
        fields = ('__all__')
        

class ClientSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Client
        fields = ('__all__')

class ClientListSerializer(serializers.ModelSerializer):
    rol = RolListSerializer(many=False, read_only=True)

    class Meta:
        model = Client
        fields = ('__all__')
        
class UserPasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=16, required=True)