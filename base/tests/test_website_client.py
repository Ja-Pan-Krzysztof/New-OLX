from django.test import Client, SimpleTestCase
from requests import Session


class TestWebsiteClient(SimpleTestCase):
    def test_log_in_client(self):

        client = Client()
        response = client.post('/account/login/', {'username': 'test', 'password': '12test12'})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers.get('Content-Type'), 'application/json')

        #self.assertEqual(response.body, {'signup': 0})