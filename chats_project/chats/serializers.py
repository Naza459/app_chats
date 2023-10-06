from django.conf import settings
from rest_framework import serializers
from chats.models import Conversations, RoomChats
from users.serializers import UserCustomerListSerializer, ClientListSerializer
class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomChats
        fields = ('__all__')

class RoomListSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoomChats
        fields = ('__all__')

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversations
        fields = ('id', 'user', 'client', 'messages', 'file')

class ConversationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Conversations
        fields = ('__all__')


class ConversationListSerializer(serializers.ModelSerializer):
    user = UserCustomerListSerializer(many=False, read_only=True)
    client = ClientListSerializer(many=False, read_only=True)
    room = RoomListSerializer(many=False, read_only=True)
    class Meta:
        model = Conversations
        fields = ('__all__')

