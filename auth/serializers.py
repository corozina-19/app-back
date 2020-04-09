from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import PasswordField
from rest_framework_simplejwt.tokens import RefreshToken


class CustomTokenObtainSerializer(serializers.Serializer):
    SOCIAL_NETWORK_CHOICES = (
        ('facebook', 'Facebook'),
        ('google', 'Google'),
    )

    user_name_social_network = serializers.CharField(required=False)
    social_network = serializers.ChoiceField(required=False, choices=SOCIAL_NETWORK_CHOICES)
    HTTP_SOCIAL_LOGIN_TOKEN = serializers.CharField(required=False)

    username_field = User \
        .USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_data.update(self.context['request'].META)
        self.fields[self.username_field] = serializers.CharField(required=False)
        self.fields['password'] = PasswordField(required=False)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    def validate(self, attrs):
        if (attrs.get(self.username_field) and attrs.get('password')) or \
                (attrs.get('user_name_social_network') and attrs.get('social_network') and
                 attrs.get('HTTP_SOCIAL_LOGIN_TOKEN')):
            attrs['request'] = self.context['request']
        self.user = authenticate(**attrs)
        # Prior to Django 1.10, inactive users could be authenticated with the
        # default `ModelBackend`.  As of Django 1.10, the `ModelBackend`
        # prevents inactive users from authenticating.  App designers can still
        # allow inactive users to authenticate by opting for the new
        # `AllowAllUsersModelBackend`.  However, we explicitly prevent inactive
        # users from authenticating to enforce a reasonable policy and provide
        # sensible backwards compatibility with older Django versions.
        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')


class CustomTokenObtainPairSerializer(CustomTokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data
