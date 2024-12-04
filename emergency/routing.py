from django.urls import path
from . import consumer 

websocket_urlpatterns = [
    path("ws/alert/", consumer.AlertConsumer.as_asgi()),  
]
