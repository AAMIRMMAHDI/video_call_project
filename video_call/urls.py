from django.urls import path
from . import views

urlpatterns = [
    path('call/', views.call_view, name='call'),
    path('api/register-peer/', views.RegisterPeerId.as_view(), name='register_peer'),
    path('api/online-users/', views.GetOnlineUsers.as_view(), name='online_users'),
    path('api/send-signal/', views.SendSignal.as_view(), name='send_signal'),
    path('api/get-signals/', views.GetSignals.as_view(), name='get_signals'),
]