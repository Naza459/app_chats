import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from chats.models import Conversations


class ConversationsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Lógica al conectar un cliente WebSocket
        await self.accept()

    async def disconnect(self, close_code):
        # Lógica al desconectar un cliente WebSocket
        pass

    @database_sync_to_async
    def save_conversation(self, data):
        # Guardar la conversación en la base de datos
        conversation = Conversations.objects.create(
            messages=data['messages'],
            type_messages=data['type_messages'],
            file=data['file'],
            user=self.scope['user'].customer,
            client=self.scope['user'].client
        )
        # Puedes realizar más operaciones o lógica aquí si es necesario

    async def receive(self, text_data):
        # Lógica al recibir un mensaje WebSocket
        # Suponiendo que los datos se envían en formato JSON
        data = json.loads(text_data)

        # Guardar la conversación en la base de datos
        await self.save_conversation(data)

        # Enviar el mensaje a todos los clientes conectados en el grupo
        await self.send_group_message(data)

    async def send_group_message(self, data):
        # Lógica para enviar un mensaje a todos los clientes en el grupo
        await self.channel_layer.group_send(
            'send_messages',  # Reemplaza con el nombre del grupo WebSocket adecuado
            {
                'type': 'send_message',
                'message': {
                    'messages': data['messages'],
                    'type_messages': data['type_messages'],
                    'file': data['file'],
                }
            }
        )

    async def send_message(self, event):
        # Lógica para enviar un mensaje a través del WebSocket
        message = event['message']
        await self.send(text_data=json.dumps(message))
