from django.conf import settings
from django.db import models


class ProfileTypes(models.TextChoices):
    DOCTOR = ('doc', 'Doctor',)
    PATIENT = ('pat', 'Patient',)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos', blank=True, null=True)
    type = models.CharField(
        max_length=3,
        choices=ProfileTypes.choices,
        default=ProfileTypes.PATIENT,
    )
