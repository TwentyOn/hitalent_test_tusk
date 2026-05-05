from django.urls import path

from .consumers import ProxyConnection

websocket_urlpatterns = [
    path('ws/connection-status/<int:user_id>/', ProxyConnection.as_asgi())
]