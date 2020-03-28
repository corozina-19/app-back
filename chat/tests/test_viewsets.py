""" Module """
from django.test import TestCase
from django.conf import settings

from rest_framework import status


class TestMessageViewSets(TestCase):
    """ Test Case for testing message viewsets """
    def setUp(self) -> None:
        self.main_uri = f'/api/{settings.CURRENT_API_VERSION}/chat/message/'

    def test_permission_on_message_creation(self):
        self.client.logout()
        dummy_body = {
            'thread_id': '',
            'message_body': '',
        }
        response = self.client.post(self.main_uri, data=dummy_body)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.client.get(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_message_creation(self):
        """ Test message creation EndPoint """
        logged = self.client.force_login('test_user')
        self.assertEqual(logged, True)

        request_body = {
            'thread_id': '',
            'message_body': '',
        }
        response = self.client.post(self.main_uri, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

        request_body['message_body'] = 'Hi!'
        response = self.client.post(self.main_uri, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data = response.json()
        self.assertIn(data, 'thread_id')
        self.assertIsInstance(data['thread_id'], int)

        request_body['thread_id'] = data['thread_id']
        response = self.client.post(self.main_uri, data=request_body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = response.json()
        thread_id = data['thread_id']
        self.assertEqual(thread_id, request_body['thread_id'])

