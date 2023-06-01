import os

from django.core.asgi import get_asgi_application

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

import forum.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'helloYouProj.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            forum.routing.websocket_urlpatterns
        )
    )
})