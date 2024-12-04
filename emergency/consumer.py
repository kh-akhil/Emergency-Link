from urllib.parse import parse_qs
from channels.generic.websocket import AsyncWebsocketConsumer
import json
import re

def sanitize_group_name(name):
    # Replace invalid characters with an underscore
    return re.sub(r'[^\w\.-]', '_', name)[:100]

class AlertConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        query_params = parse_qs(self.scope["query_string"].decode())
        self.vehicle_id = query_params.get("vehicle_id", [None])[0]
        self.group_name = sanitize_group_name(f"vehicle_{self.vehicle_id}")
        
        print(f"Extracted vehicle_id: {self.vehicle_id}")
        print(f"Sanitized group name: {self.group_name}")
        
        if not self.vehicle_id:
            print("No id provided")
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        message = {
            'status' : 'success',
            'message' : 'Hello world'
        }
        await self.accept()
        await self.send(text_data=json.dumps(message))
    
    async def disconnect(self, close_code):
        if self.vehicle_id:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
            
    async def send_alert(self, event):
        await self.send(text_data=json.dumps(event["message"]))