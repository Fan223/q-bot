from django.urls import re_path

from app.web_socket import api_server, event_server

websocket_urlpatterns = [
    # urls 路径
    re_path(r'api/(?P<group>\w+)/$', api_server.ChatConsumer.as_asgi()),
    re_path(r'event/(?P<group>\w+)/$', event_server.ChatConsumer.as_asgi())
]
