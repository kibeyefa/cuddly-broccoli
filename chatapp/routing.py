from django.conf.urls import url
from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator, OriginValidator
from django.utils.regex_helper import Group

from chat.consumers import *

application = ProtocolTypeRouter({
    'websocket': AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter([
                path("chat/", ChatConsumer.as_asgi()),
                url(r"^chat/groups/(?P<id>[\w.@+-]+)", PrivateChatConsumer.as_asgi()),
                url(r"^chat/(?P<username>[\w.@+-]+)", PrivateChatConsumer.as_asgi()),
                # path('chat/<str:username>/', ChatConsumer()),
                # path('group-chat/<str:id>/', GroupChatConsumer.as_asgi(), name='group-chat'),
            ])
        )
    )
})  