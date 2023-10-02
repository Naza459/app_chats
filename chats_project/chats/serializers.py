from django.conf import settings
from rest_framework import serializers
from chats.models import Conversations
from users.serializers import UserCustomerListSerializer, ClientListSerializer

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversations
        fields = ('__all__')


class ConversationListSerializer(serializers.ModelSerializer):
    user = UserCustomerListSerializer(many=False, read_only=True)
    client = ClientListSerializer(many=False, read_only=True)

    class Meta:
        model = Conversations
        fields = ('__all__')
