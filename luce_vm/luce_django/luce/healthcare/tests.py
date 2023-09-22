from django.test import TestCase
from django.test.client import Client

from accounts.models import User

# Create your tests here.


# class UploadDataViewTests(TestCase):
#     def setUp(self):
#         self.username = 'likun6034@gmail.com'
#         self.password = '1'
#         self.user = User.objects.create_user(
#             username=self.username,
#             password=self.password
#         )

#         self.client = Client()
#         self.client.login(username=self.username, password=self.password)

class UserRegistrationTests(TestCase):
    def setUp(self):
        self.email = 'test@email.com'
        self.gender = 'male'
        self.age = 30
        self.first_name = 'first_name_test'
        self.last_name = 'last_name_test'
        self.password = 'password_test'
        self.user_type = 0

        self.user = User.objects.create_user(
            self.email,
            self.gender,
            self.age,
            self.first_name,
            self.last_name,
            password=self.password,
            user_type=self.user_type
        )

        self.client = Client()

    def test_registration(self):
        path = 'user/register/'

        # print(self.email)
        post_data = {
            'email': self.email
        }

        resp = self.client.post(
            path=path,
            data=post_data,
            content_type='application/json'
        )

        result = resp

        print(result)

