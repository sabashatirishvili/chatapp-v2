import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        await self.accept()

        await self.send(
            text_data=json.dumps(
                {
                    "type": "connection_established",
                    "message": "You have connected successfully!",
                }
            )
        )

    async def receive(self, text_data):
        if not text_data:
            print("Empty message received")
            return  # or handle it as needed

        try:
            data = json.loads(text_data)
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {text_data}")
            return  # handle the error appropriately
          
        data = json.loads(text_data)
        message = data.get("message", "No message")

        # Echo the message back to the client
        await self.send(
            text_data=json.dumps({"type": "chat_message", "message": message})
        )
