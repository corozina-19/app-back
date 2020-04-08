from django.db import models

from django.contrib.auth.models import User


class SocialNetwork(models.Model):
    """
    model used to save the social networks through which users connect
    """
    SOCIAL_NETWORK_CHOICES = (
        ('facebook', 'Facebook'),
        ('google', 'Google'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    social_network = models.CharField(choices=SOCIAL_NETWORK_CHOICES, max_length=20)
    token = models.TextField(unique=True)

    def __str__(self):
        return f'{self.social_network}'
