from django.test import TestCase
from unittest.mock import patch
import json
from privacy.snarkjs_service import SnarkjsService


class SnarkjsServiceTests(TestCase):
    def setUp(self):
        # print("setUp")
        # Here we need to  distinguish local and docker environment
        # docker
        # snarkjs_service_url = "http://zkp_service:8888/compute_commitment"
        # local
        snarkjs_service_url = "http://localhost:8888"
        self.snarkjs_service = SnarkjsService(snarkjs_service_url)

    def test_generate_proof_online(self):
        payload = {"secret": "secret"}

        response = self.snarkjs_service.generate_proof(payload)

        print(type(response))

        # print(response)

    # @patch('requests.post')
    # def test_generate_proof(self, mock_post):
    #     # print(mock_post)

    #     mock_response = {'proof': 'some-proof', 'status': 'success'}

    #     # mock_post.return_value = 200
    #     mock_post.return_value = mock_response
    #     # print(mock_post.return_value)

    #     # print(mock_post.return_value.status_code)

    #     payload = json.dumps({"secret": "secret"}).encode('utf-8')

    #     response = self.snarkjs_service.generate_proof(payload)
    # print("here")
    # print(response)

    # self.assertIsNotNone(response)
    # self.assertEqual(response, mock_response)
