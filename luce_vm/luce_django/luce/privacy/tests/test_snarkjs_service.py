from django.test import TestCase
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
