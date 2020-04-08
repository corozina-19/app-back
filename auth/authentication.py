from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from auth.models import SocialNetwork


class CustomAuth(ModelBackend):

    def authenticate(self, request, **kwargs):
        """
        This backend authenticates through social network token or normal authentication

        :param request: django request
        :type: HttpRequest objects
        :param kwargs: data by which the user will authenticate
        :type: Dict objects
        :return: User or None object
        """
        username = kwargs.get('username')
        password = kwargs.get('password')
        user_name_social_network = kwargs.get('user_name_social_network')
        social_network = kwargs.get('social_network')
        HTTP_SOCIAL_LOGIN_TOKEN = kwargs.get('HTTP_SOCIAL_LOGIN_TOKEN')
        if all([user_name_social_network, social_network, HTTP_SOCIAL_LOGIN_TOKEN]):
            # TODO: validate if social token is valid in network social
            try:
                user = SocialNetwork.objects.get(token=HTTP_SOCIAL_LOGIN_TOKEN).user
            except SocialNetwork.DoesNotExist:
                user, is_create = User.objects.get_or_create(username=user_name_social_network)
                if is_create:
                    user.is_active = True
                    user.set_password(User.objects.make_random_password())
                    user.save()
                SocialNetwork.objects.create(user=user, token=HTTP_SOCIAL_LOGIN_TOKEN, social_network=social_network)
            return user
        elif all([username, password]):
            return super(CustomAuth, self).authenticate(request, username, password)