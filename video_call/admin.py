from django.contrib import admin
from .models import Peer, Signal, Notification

admin.site.register(Peer)
admin.site.register(Signal)
admin.site.register(Notification)