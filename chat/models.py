from django.contrib.auth.models import User
from django.db import models


class Thread(models.Model):
    """Model used to manage a chat thread"""

    STATUS_CHOICES = (
        (0, 'Open'),
        (1, 'Take'),
        (2, 'Closed'),
    )

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='doctor')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS_CHOICES)

    def __str__(self):
        return f'status: {self.get_status_display} user: {self.user.get_full_name()} ' \
               f'doctor: {self.doctor.get_full_name()}'

    class Meta:
        ordering = ['last_update']


class Message(models.Model):
    """Model used to manage a chat"""
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateTimeField(auto_now_add=True)
    body = models.TextField()

    def __str__(self):
        return f'user: {self.user.get_full_name()} message: {self.body}'

    class Meta:
        ordering = ['creation_date']

