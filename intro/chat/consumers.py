from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json

from . import models


class AsyncChatConsumer(AsyncWebsocketConsumer):
    async def websocket_connect(self):
        self.user_cookie = self.scope["session"]["anonymous_user_id"]
        self.room_name = f"{self.user_cookie}:supports"
        self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def websocket_disconnect(self, code):
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket.sendmessage",
                "message": "Disconnected."
            }
        )
        raise StopConsumer("Websocket connection has been disconnected.")

    async def websocket_receive(self, message):
        data = json.loads(message)
        text = data["text"]
        await self.create_chat(text)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket.sendmessage",
                "message": message
            }
        )

    async def websocket_sendmessage(self, message):
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_chat(self, text):
        chat = models.Chat.objects.create(
            sender=self.user_cookie,
            text=text,
            support=...
        )
        return chat
