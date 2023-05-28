from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from channels.db import database_sync_to_async

import json

from . import models


class AsyncChatConsumer(AsyncWebsocketConsumer):
    """ Simple async chat consumer with site supports """

    async def websocket_connect(self):
        """ create a group when websocket connected
            and accept the websocket requests
        """
        self.user = self.scope["user"]
        if self.user:
            self.room_name = f"{self.user}:support"
        self.user_cookie = self.scope["session"]["anonymous_user_id"]
        self.room_name = f"{self.user_cookie}:supports"
        self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )
        await self.accept()

    async def websocket_disconnect(self, code):
        """ disconnecting websocket connection
            by raising a StopConsumer Exception
        """
        await self.channel_layer.group_send(
            self.room_name,
            {
                "type": "websocket.sendmessage",
                "message": "Disconnected."
            }
        )

        raise StopConsumer("Websocket connection has been disconnected.")

    async def websocket_receive(self, message):
        """ Recieve websocket datas from frontend
            and storing them on db, then response
            them back to frontend
        """
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
        """ Simple chat sender helper function
            to send passed data to frontend using
            websocket.send method
        """
        await self.send(text_data=json.dumps(message))

    @database_sync_to_async
    def create_chat(self, text):
        """ Database async function
            for storing chat data
        """
        chat = models.Chat(text=text)
        if not self.user:
            chat.anonymous_sender = self.user_cookie
        else:
            chat.sender = self.user
        chat.save()
        return chat
