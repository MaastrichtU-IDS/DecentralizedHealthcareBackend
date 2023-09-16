from django.db import models

# Create your models here.
import requests
import json


class SnarkjsService:
    def __init__(self, base_url="http://localhost:8888"):
        self.base_url = base_url

    def generate_proof(self, secret):
        payload = {"secret": secret}
        """
        Function to generate ZKP proof using snarkjs.
        """
        try:
            response = requests.post(f"{self.base_url}/compute_commitment",
                                     json=payload)

            # print(response.json())
            response_json = response.json()
            # print(response_json['public_signals'])
            # json.loads(response.data.decode('utf-8'))

            # print(response)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return None
        except Exception as e:
            print(f"Error generating proof: {e}")
            return None
