import json

from django.contrib.auth.models import User
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Forum, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.forum_name = self.scope['url_route']['kwargs']['forum_name']
        self.forum_group_name = 'chat_%s' % self.forum_name

        await self.channel_layer.group_add(
            self.forum_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self):
        await self.channel_layer.group_discard(
            self.forum_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        username = data['username']
        forum = data['forum']

        await self.save_message(username, forum, message)

        # Send message to forum group
        await self.channel_layer.group_send(
            self.forum_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username
            }
        )

    # Receive message from forum group
    async def chat_message(self, event):
        message = event['message']
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'username': username
        }))

    @sync_to_async
    def save_message(self, username, forum, message):
        user = User.objects.get(username=username)
        forum = Forum.objects.get(slug=forum)

        Message.objects.create(user=user, forum=forum, content=message)