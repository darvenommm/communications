from django.urls import path

from .consumers import SubscriberConsumer


websocket_urlpatterns = [
    path("subscribers/", SubscriberConsumer.as_asgi()),
]
