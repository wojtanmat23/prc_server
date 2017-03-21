import mock
from django.conf import settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from request_handler.models import AllowedRequest


class TestAPI(APITestCase):
    fixtures = ['test_api']

    def setUp(self):
        settings.REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'] = [
            'rest_framework.authentication.SessionAuthentication'
        ]
        self.client.login(username='test', password='test123')
        self.allowed_request = AllowedRequest.objects.get(id=1)

    def test_get_platform_information_success(self):
        response = self.client.get(reverse('identify_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response.json()['system'], ('Windows', 'Linux'))

    def test_get_allowed_request_info_success(self):
        response = self.client.get(reverse('allowed_view'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['id'], self.allowed_request.id)

        for attr in response.json():
            if attr != 'id':
                self.assertEqual(hasattr(self.allowed_request, attr), True)

    @mock.patch('subprocess.call')
    def test_post_signal_success(self, mock):
        response = self.client.post(reverse('allowed_view'), {'value': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['command'], 1)
        self.assertEqual(response.json()['result'], 'success')

    @mock.patch('sys.stdout')
    def test_post_python_simple_code_success(self, mock):
        command = "print('3')"
        response = self.client.post(reverse('external_view'), {'external': command})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['result'][0], "3")

    @mock.patch('sys.stdout')
    def test_post_python_function_success(self, mock):
        command = "print([i**2 for i in range(6)])"
        response = self.client.post(reverse('external_view'), {'external': command})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['result'][0], "[0, 1, 4, 9, 16, 25]")

    @mock.patch('subprocess.call')
    def test_post_wrong_signal_failure(self, mock):
        response = self.client.post(reverse('allowed_view'), {'value': 99})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'value': ['"99" is not a valid choice.']})

    @mock.patch('sys.stdout')
    def test_post_python_bad_code_failure(self, mock):
        command = "print(z"  # badly formatted code
        response = self.client.post(reverse('external_view'), {'external': command})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'non_field_errors': ['Cannot process request.']})

    def test_unauthenticated_user_access_to_api_failure(self):
        self.client.logout()
        response = self.client.get(reverse('allowed_view'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
