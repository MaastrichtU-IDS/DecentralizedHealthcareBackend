from django.test import TestCase

# Create your tests here.


class UploadDataViewTests(TestCase):
    def setUp(self):
        self.username = 'likun6034@gmail.com'
        self.password = '1'
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password
        )

        self.client = Client()
        self.client.login(username=self.username, password=self.password)
