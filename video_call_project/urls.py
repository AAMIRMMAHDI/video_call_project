from django.contrib import admin
from django.urls import path, include
from video_call import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),  # مسیر اصلی به صفحه ورود
    path('', include('video_call.urls')),
]