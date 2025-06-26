
from django.urls import re_path
from video_call import consumers

websocket_urlpatterns = [
    re_path(r'ws/call/(?P<room_name>\w+)/$', consumers.CallConsumer.as_asgi()),
]