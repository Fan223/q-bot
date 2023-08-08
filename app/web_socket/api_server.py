import json

from asgiref.sync import async_to_sync
from channels.exceptions import StopConsumer
from channels.generic.websocket import WebsocketConsumer


class ChatConsumer(WebsocketConsumer):
    def websocket_connect(self, message):
        self.accept()
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_add)(group, self.channel_name)

    def websocket_receive(self, message):
        print('API 接收到的消息: ', message)

    def send_msg(self, event):
        text = event['message']
        self.send(json.dumps(text, ensure_ascii=False))

    def websocket_disconnect(self, message):
        group = self.scope['url_route']['kwargs'].get('group')
        async_to_sync(self.channel_layer.group_discard)(group, self.channel_name)
        raise StopConsumer
