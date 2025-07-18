import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import video_call.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'video_call_project.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            video_call.routing.websocket_urlpatterns
        )
    ),
})