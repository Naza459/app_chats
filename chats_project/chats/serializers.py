from django.conf import settings
from rest_framework import serializers
from chats.models import Conversations
from users.serializers import UserCustomerListSerializer, ClientListSerializer

class ConversationSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()  # Usar SerializerMethodField para personalizar la representación del archivo

    class Meta:
        model = Conversations
        fields = '__all__'

    def get_file(self, obj):
        # Aquí puedes personalizar la representación del archivo como desees
        if obj.file:
            return obj.file.read().decode('utf-8')  # Leer el archivo y convertirlo a una cadena base64 u otro formato

        return None

class ConversationSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()  # Usar SerializerMethodField para personalizar la representación del archivo

    class Meta:
        model = Conversations
        fields = '__all__'

    def get_file(self, obj):
        # Aquí puedes personalizar la representación del archivo como desees
        if obj.file:
            return obj.file.read().decode('utf-8')  # Leer el archivo y convertirlo a una cadena base64 u otro formato

        return None

class ConversationListSerializer(serializers.ModelSerializer):
    user = UserCustomerListSerializer(many=False, read_only=True)
    client = ClientListSerializer(many=False, read_only=True)
    class Meta:
        model = Conversations
        fields = ('__all__')

