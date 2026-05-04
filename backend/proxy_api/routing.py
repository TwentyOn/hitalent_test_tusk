from django.urls import path

from .consumers import JoinLeave

websocket_urlpatterns = [
    path('', JoinLeave.as_asgi())
]