from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json

from . import models


class AsyncChatConsumer(AsyncWebsocketConsumer):
    """ Simple async chat consumer with site supports """

    async def connect(self):
        """ create a group when websocket connected
            and accept the websocket requests
        """
        self.user = self.scope.get("user")
        if self.user:
            self.room_name = f"{self.user}-support"
        self.user_cookie = self.scope.get("session")
        if self.user_cookie:
            self.user_cookie = self.user_cookie.get('anonymous_user_id')
            self.room_name = f"{self.user_cookie}-supports"
        else:
            self.test_name = "test"
            self.room_name = f"{self.test_name}-support"
        self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, code):
        """ disconnecting websocket connection
            by raising a StopConsumer Exception
        """
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send_message",
                "message": "Disconnected."
            }
        )

        raise StopConsumer(f"Websocket connection has been disconnected.\ncode: {code}")

    async def receive(self, text_data=None, bytes_data=None):
        """ Recieve websocket datas from frontend
            and storing them on db, then response
            them back to frontend
        """
        message = json.loads(text_data)
        text = message["text"]
        await self.create_chat(text)
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "send_message",
                "message": {
                    "text": message
                }
            }
        )

    async def send_message(self, message):
        """ Simple chat sender helper function
            to send passed data to frontend using
            websocket.send method
        """
        print("Sending", message)
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_chat(self, text):
        """ Database async function
            for storing chat data
        """
        chat = models.Chat(text=text)
        if not self.user:
            chat.anonymous_sender = self.user_cookie or self.test_name
        else:
            chat.sender = self.user
        chat.save()
        return chat
