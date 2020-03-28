""" Module """
from django.test import TestCase
from django.conf import settings

from django.contrib.auth import get_user_model

from rest_framework import status

User = get_user_model()


class TestMessageViewSets(TestCase):
    """ Test Case for testing message viewsets """
    def setUp(self) -> None:
        self.main_uri = f'/api/{settings.CURRENT_API_VERSION}/chat/message/'
        self.cred = {
            'username': 'test_user',
            'password': '12345'
        }
        self.user = User.objects.create_user(**self.cred)

    def test_permission_on_message_creation(self):
        """ Test for proof auth validation and method validations """
        dummy_body = {
            'thread': '',
            'body': '',
        }
        response = self.client.post(self.main_uri, data=dummy_body)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        logged = self.client.login(**self.cred)
        self.assertTrue(logged)

        response = self.client.get(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_message_creation(self):
        """ Test message creation EndPoint """
        logged = self.client.login(**self.cred)
        self.assertEqual(logged, True)

        request_body = {
            'thread': '',
            'body': '',
        }
        response = self.client.post(self.main_uri, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)

        response = self.client.post(self.main_uri, data=request_body, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        request_body['body'] = 'Hi!'
        response = self.client.post(self.main_uri, data=request_body, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertTrue('thread' in data)
        self.assertIsInstance(data['thread'], int)

        request_body['thread'] = data['thread']
        response = self.client.post(self.main_uri, data=request_body, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        thread_id = data['thread']
        self.assertEqual(thread_id, request_body['thread'])

