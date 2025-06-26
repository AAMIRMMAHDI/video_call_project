from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Peer, Signal
from .serializers import PeerSerializer, SignalSerializer
from django.contrib.auth.models import User

def call_view(request):
    return render(request, 'video_call/call.html')

class RegisterPeerId(APIView):
    permission_classes = [AllowAny]  # برای تست لوکال
    def post(self, request):
        peer_id = request.data.get('peer_id')
        if peer_id:
            # برای تست بدون لاگین، کاربر پیش‌فرض انتخاب می‌شه
            user = request.user if request.user.is_authenticated else User.objects.first()
            if not user:
                return Response({'error': 'No user available'}, status=status.HTTP_400_BAD_REQUEST)
            Peer.objects.update_or_create(user=user, defaults={'peer_id': peer_id})
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Peer ID required'}, status=status.HTTP_400_BAD_REQUEST)

class GetOnlineUsers(APIView):
    permission_classes = [AllowAny]  # برای تست لوکال
    def get(self, request):
        peers = Peer.objects.all()
        serializer = PeerSerializer(peers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendSignal(APIView):
    permission_classes = [AllowAny]  # برای تست لوکال
    def post(self, request):
        sender = request.user if request.user.is_authenticated else User.objects.first()
        if not sender:
            return Response({'error': 'No sender available'}, status=status.HTTP_400_BAD_REQUEST)
        
        receiver_peer_id = request.data.get('receiver_peer_id')
        signal_type = request.data.get('type')
        signal_data = request.data.get('data')

        try:
            receiver = Peer.objects.get(peer_id=receiver_peer_id).user
        except Peer.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

        Signal.objects.create(
            sender=sender,
            receiver=receiver,
            type=signal_type,
            data=signal_data
        )
        return Response({'status': 'signal sent'}, status=status.HTTP_201_CREATED)

class GetSignals(APIView):
    permission_classes = [AllowAny]  # برای تست لوکال
    def get(self, request):
        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            return Response({'error': 'No user available'}, status=status.HTTP_400_BAD_REQUEST)
        signals = Signal.objects.filter(receiver=user).order_by('-created_at')
        serializer = SignalSerializer(signals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)