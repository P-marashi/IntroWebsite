from django.urls import path
from . import consumers

urlpatterns = [
    path('chat/', consumers.AsyncChatConsumer.as_asgi())
]
