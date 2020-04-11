from django.contrib.auth.models import User
from django.db import models
from chat.choices import STATUS_CHOICES


class Thread(models.Model):
    """Model used to manage a chat thread"""

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient')
    doctor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='doctor')
    creation_date = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=STATUS_CHOICES, default='open', max_length=25)

    def __str__(self):
        return f'status: {self.get_status_display()} ' \
               f'- patient: {self.patient.get_full_name() if self.patient.get_full_name() else self.patient.username} '\
               f'- doctor: {(self.doctor.get_full_name() if self.doctor.get_full_name() else self.doctor.username) if self.doctor else None}'

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
