from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('call/', views.call_view, name='call'),
    path('api/register-peer/', views.RegisterPeerId.as_view(), name='register_peer'),
    path('api/online-users/', views.GetOnlineUsers.as_view(), name='online_users'),
    path('api/send-signal/', views.SendSignal.as_view(), name='send_signal'),
    path('api/get-signals/', views.GetSignals.as_view(), name='get_signals'),
    path('api/send-notification/', views.SendNotification.as_view(), name='send_notification'),
    path('api/get-notifications/', views.GetNotifications.as_view(), name='get_notifications'),
    path('api/update-notification/', views.UpdateNotification.as_view(), name='update_notification'),
]