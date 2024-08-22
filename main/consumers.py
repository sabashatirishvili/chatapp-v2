import json
import logging
from django.shortcuts import get_object_or_404
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from .models import User, Chat, Message


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        logging.debug("WebSocket connect method called.")
        if self.scope["user"].is_authenticated:
            self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
            self.group_name = f"chat_{self.chat_id}"

            self.channel_layer.group_add(self.group_name, self.channel_name)

            self.accept()
        else:
            self.close()

    def disconnect(self, close_code):
        self.channel_layer.group_discard(self.group_name, self.channel_name)

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json.get("message", "")
        user = self.scope["user"]

        if not message_content:
            return

        chat = get_object_or_404(Chat, id=self.chat_id)

        # Create the message
        message = Message.objects.create(
            content=message_content, sender=user, chat=chat
        )

        self.channel_layer.group_send(
            self.group_name, {"type": "chat_message", "message": message_content}
        )

    def chat_message(self, event):
        message = event["message"]

        # Send message to WebSocket
        self.send(text_data=json.dumps({"message": message}))