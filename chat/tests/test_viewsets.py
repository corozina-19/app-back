""" Module """
import json

from django.db.models import Q
from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status

from chat.api.serializers import ThreadSerializer
from chat.choices import open_, closed
from chat.models import Thread
import pdb

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


class TestThreadViewSet(TestCase):

    def setUp(self) -> None:
        self.main_uri = f'/api/{settings.CURRENT_API_VERSION}/chat/thread/'
        self.cred_superuser = {
            'username': 'admin',
            'password': 'admin'
        }
        self.cred1 = {
            'username': 'user1',
            'password': 'user1'
        }
        self.cred2 = {
            'username': 'user2',
            'password': 'user2'
        }
        self.cred3 = {
            'username': 'user3',
            'password': 'user3'
        }
        self.user_superuser = User.objects.create_superuser(**self.cred_superuser)
        self.user1 = User.objects.create_user(**self.cred1)
        self.user2 = User.objects.create_user(**self.cred2)
        self.user3 = User.objects.create_user(**self.cred3)

        # Thread Creation
        Thread.objects.create(patient=self.user1, doctor=self.user2, status=open_)
        Thread.objects.create(patient=self.user1, doctor=self.user2, status=closed)
        Thread.objects.create(patient=self.user2, status=open_)

    def test_permission_in_the_threads_list(self):
        """ Test for proof auth validation and method validations """

        response = self.client.post(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        logged = self.client.login(**self.cred_superuser)
        self.assertTrue(logged)

        response = self.client.post(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.put(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

        response = self.client.get(self.main_uri)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete(f'{self.main_uri}1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_threads_listing_depending_rol_or_user(self):
        """ Thread listing test depending on the role or authenticated user and status Threads """

        logged = self.client.login(**self.cred_superuser)
        self.assertTrue(logged)
        response = self.client.get(self.main_uri)
        thread_serializer_data = object_thread(None)
        self.assertEqual(response.json(), thread_serializer_data)

        logged = self.client.login(**self.cred1)
        self.assertTrue(logged)
        response = self.client.get(self.main_uri)
        thread_serializer_data = object_thread(self.user1)
        self.assertEqual(response.json(), thread_serializer_data)

        logged = self.client.login(**self.cred2)
        self.assertTrue(logged)
        response = self.client.get(self.main_uri)
        thread_serializer_data = object_thread(self.user2)
        self.assertEqual(response.json(), thread_serializer_data)

        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.get(self.main_uri)
        thread_serializer_data = object_thread(self.user3)
        self.assertEqual(response.json(), thread_serializer_data)

    def test_thread_deletion_and_retrieve(self):
        """ Test the detail or deletion of an element """
        logged = self.client.login(**self.cred_superuser)
        self.assertTrue(logged)
        response = self.client.delete(f'{self.main_uri}10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.get(f'{self.main_uri}10/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.delete(f'{self.main_uri}1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get(f'{self.main_uri}1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_thread_action_report_thread(self):
        """ Test to simulate the action of reporting a thread """
        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/report-thread/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        logged = self.client.login(**self.cred2)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/report-thread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_thread_action_close_thread(self):
        """ test to simulate the action of close a thread """
        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/close-thread/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        logged = self.client.login(**self.cred1)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/close-thread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        logged = self.client.login(**self.cred2)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/close-thread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_thread_action_take_thread(self):
        """ Test to simulate the action of take a thread """
        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}1/take-thread/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        logged = self.client.login(**self.cred3)
        self.assertTrue(logged)
        response = self.client.get(f'{self.main_uri}3/take-thread/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


def object_thread(user: User) -> [list]:
    thread = Thread.objects.filter(status=open_)
    if user:
        thread = thread.filter(Q(patient=user) | Q(doctor=user))
    thread_serializer_data = json.dumps(ThreadSerializer(thread, many=True).data)
    thread_serializer_data = json.loads(thread_serializer_data)
    return thread_serializer_data
