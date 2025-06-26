from rest_framework import serializers
from .models import Peer, Signal
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