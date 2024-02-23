"""
This module provides the SnarkjsService class, which interfaces with a snarkjs-based service to generate Zero-Knowledge Proofs (ZKPs).

The SnarkjsService class allows for sending a secret to a specified server endpoint and receiving a ZKP in return. It handles HTTP requests, response parsing, and error logging.

Dependencies:
    - requests: For making HTTP requests to the snarkjs service.
    - json: For parsing the JSON response from the service.
    - logging: For logging error messages.

Example:
    service = SnarkjsService()
    proof = service.generate_proof(secret='my_secret')
"""

import logging
import json
import requests


class SnarkjsService:
    """
    SnarkjsService provides an interface to a snarkjs-based server for generating Zero-Knowledge Proofs (ZKPs).

    It sends a secret to the server and retrieves a ZKP. The class handles the details of making the HTTP request,
    processing the response, and error handling. It is designed to work with a server running snarkjs that exposes
    a `/compute_commitment` endpoint.

    Attributes:
        base_url (str): The base URL of the snarkjs server. Defaults to 'http://localhost:8888'.
        endpoint (str): The endpoint for computing the commitment. Defaults to '/compute_commitment'.

    Methods:
        generate_proof(secret): Takes a secret, sends it to the snarkjs server, and returns the generated ZKP.
            Returns None if the server response is not successful or if an error occurs.

    Example:
        service = SnarkjsService()
        proof = service.generate_proof(secret='my_secret')
    """

    def __init__(self, base_url="http://zkp_service:8888", endpoint="/compute_commitment"):
        self.base_url = base_url
        self.endpoint = endpoint

    def generate_proof(self, secret):
        """
        Function to generate ZKP proof using snarkjs.
        """
        payload = {"secret": secret}
        url = f"{self.base_url}{self.endpoint}"

        try:
            response = requests.post(
                url,
                json=payload,
                timeout=1000
            )

            if response.status_code == 200:
                return response.json()
            else:
                logging.error(
                    "Received non-200 status code: %s",
                    response.status_code
                )
                return None

        except requests.exceptions.RequestException as req_err:
            logging.error("Request error: %s", req_err)
        except json.JSONDecodeError as json_err:
            logging.error("JSON decode error: %s", json_err)
