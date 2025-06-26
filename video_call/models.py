from django.db import models
from django.contrib.auth.models import User

class Peer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    peer_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.peer_id}"

class Signal(models.Model):
    sender = models.ForeignKey(User, related_name='sent_signals', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_signals', on_delete=models.CASCADE)
    type = models.CharField(max_length=20)  # offer, answer, candidate
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)