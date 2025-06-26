from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .models import Peer, Signal, Notification
from .serializers import PeerSerializer, SignalSerializer, NotificationSerializer
import uuid

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('call')
        else:
            return render(request, 'video_call/login.html', {'error': 'نام کاربری یا رمز عبور اشتباه است'})
    return render(request, 'video_call/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if User.objects.filter(username=username).exists():
            return render(request, 'video_call/signup.html', {'error': 'نام کاربری قبلاً استفاده شده'})
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('call')
    return render(request, 'video_call/signup.html')

def call_view(request):
    return render(request, 'video_call/call.html')

class RegisterPeerId(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        user = request.user if request.user.is_authenticated else User.objects.get_or_create(username='guest')[0]
        peer_id = request.data.get('peer_id')
        if peer_id:
            Peer.objects.update_or_create(user=user, defaults={'peer_id': peer_id})
            return Response({'status': 'success'}, status=status.HTTP_200_OK)
        return Response({'error': 'Peer ID required'}, status=status.HTTP_400_BAD_REQUEST)

class GetOnlineUsers(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        peers = Peer.objects.exclude(user=request.user if request.user.is_authenticated else None)
        serializer = PeerSerializer(peers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendSignal(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        sender = request.user if request.user.is_authenticated else User.objects.get_or_create(username='guest')[0]
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
    permission_classes = [AllowAny]
    def get(self, request):
        user = request.user if request.user.is_authenticated else User.objects.get_or_create(username='guest')[0]
        signals = Signal.objects.filter(receiver=user).order_by('-created_at')
        serializer = SignalSerializer(signals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SendNotification(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        sender = request.user if request.user.is_authenticated else User.objects.get_or_create(username='guest')[0]
        receiver_peer_id = request.data.get('receiver_peer_id')
        call_id = request.data.get('call_id')

        try:
            receiver = Peer.objects.get(peer_id=receiver_peer_id).user
        except Peer.DoesNotExist:
            return Response({'error': 'Receiver not found'}, status=status.HTTP_404_NOT_FOUND)

        Notification.objects.create(
            sender=sender,
            receiver=receiver,
            call_id=call_id,
            status='pending'
        )
        return Response({'status': 'notification sent'}, status=status.HTTP_201_CREATED)

class GetNotifications(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        user = request.user if request.user.is_authenticated else User.objects.get_or_create(username='guest')[0]
        notifications = Notification.objects.filter(receiver=user, status='pending').order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateNotification(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        notification_id = request.data.get('notification_id')
        status = request.data.get('status')  # accepted or rejected
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.status = status
            notification.save()
            return Response({'status': 'notification updated'}, status=status.HTTP_200_OK)
        except Notification.DoesNotExist:
            return Response({'error': 'Notification not found'}, status=status.HTTP_404_NOT_FOUND)