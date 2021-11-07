from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status



class UserTests(APITestCase):

    def test_user_register(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('user-register')
        data =  {
        "email":"influecner@email.com",
        "password":"password123",
        "user_type":0
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)