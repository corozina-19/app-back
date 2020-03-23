from collections import namedtuple
import requests
from django.conf import settings
from django.contrib.auth.models import User

from firebase.models import TokenFirebase


class PushNotificationsFirebaseManager(object):
    """
    Standard basic class for Notifications Firebase (send Data messages)
    """
    fcm = namedtuple('FcmRequest', ['to', 'collapse_key', 'notification', 'data'])

    def __init__(self, url_fcm=None, key=None, *args, **kwargs):
        self.url_fmc = url_fcm if url_fcm else settings.URL_FCM
        self.key = key if key else settings.NOTIFICATIONS_ZINA_FIREBASE_TOKEN

    def __str__(self):
        return f'server_url: {self.url_fcm} server_key:{self.key}'

    def __repr__(self):
        return f"{self.__class__.__name__}('{settings.URL_FCM}', '{settings.NOTIFICATIONS_ZINA_FIREBASE_TOKEN}')"

    def send(self, to: str, title: str, body: str, collapse_key: str = 'type_a', *args, **data: dict) -> requests:
        """
            Method to send messages from firebase
            :param to: Token firebase.
            :type: str
            :param title: Message title.
            :type: str
            :param body: Message body.
            :type: str
            :param collapse_key: Message duration. you can read more at -->
                                 https://firebase.google.com/docs/cloud-messaging/concept-options.
            :type: str
            :param data: Message data.
            :type: dict
            :return: Response of the message sent.
            :type: requests or None
        """
        header = {'Authorization': 'key={0}'.format(self.key), 'Content-Type': 'application/json'}
        requests_fcm = self.fcm(to, collapse_key, {'title': title, 'body': body}, data)._asdict()
        return requests.post(self.url_fmc, headers=header, json=dict(requests_fcm))

    def add_token(self, user: User, token: str) -> TokenFirebase:
        """
            Method to save Firebase token for the user.
            :param user: Token owner.
            :type: User
            :param token: firebase token.
            :type: str
            :return: Instance TokenFirebase or Exception if user has the token.
            :type: TokenFirebase or Exception
        """
        if not isinstance(user, User):
            raise ValueError('A user instance is needed to save the token')
        if not hasattr(self, '__token'):
            self.__token = TokenFirebase(user=user, token=token).save()
        return self.__token

    @staticmethod
    def all_token(user: User):
        """
            Method to get all Firebase token for the user.
            :param user: Token owner.
            :type: User.
            :return: List tokens to user.
            :type: list.
        """
        if not isinstance(user, User):
            raise ValueError('A user instance is needed to save the token')
        tokens = TokenFirebase.objects.filter(
            user=user
        ).values_list('token', flat=True)
        return tokens


class PushNotificationsFirebaseBroadcast(PushNotificationsFirebaseManager):
    """
        Class to send notifications from a user to all their registered devices.
    """

    def __init__(self, user: User, *args, **kwargs):
        self.user = user
        super(PushNotificationsFirebaseBroadcast, self).__init__(*args, **kwargs)

    def __str__(self):
        return f'{self.__repr__()} all token: {self.tokens_firebase}'

    @property
    def tokens_firebase(self):
        """
        Get all the tokens related to the requested user

        :return: all token associated with set user
        """
        return PushNotificationsFirebaseManager.all_token(self.user)

    def send_all_devices(self, title: str, body: str, *args: str, **data: dict) -> requests:
        """
          Method to send messages for all user devices.
          :param title: Message title.
          :type: str
          :param body: Message body.
          :type: str
          :param data: Message data.
          :type: dict
          :return: Http response of the all messages sent.
          :type: Http response
        """
        sent_token = {}
        for item in self.tokens_firebase:
            sent_token[item] = super(PushNotificationsFirebaseBroadcast, self).send(item, title, body, *args, **data)
        return sent_token
