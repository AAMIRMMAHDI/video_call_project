from rest_framework import serializers
from .models import Peer, Signal, Notification
from django.contrib.auth.models import User

class PeerSerializer(serializers.ModelSerializer):
    user__username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Peer
        fields = ['user__username', 'peer_id']

class SignalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signal
        fields = ['type', 'data', 'created_at']

class NotificationSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Notification
        fields = ['id', 'sender_username', 'call_id', 'status', 'created_at']