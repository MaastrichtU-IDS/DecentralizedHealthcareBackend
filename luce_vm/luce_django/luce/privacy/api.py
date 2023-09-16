import urllib3
import json


def generate_proof(secret):
    http = urllib3.PoolManager()
    # Here we need to  distinguish local and docker environment
    # docker
    # snark_service_url = "http://zkp_service:8888/compute_commitment"

    # local
    snark_service_url = "http://localhost:8888/compute_commitment"
    data = {"secret": secret}
    encoded_data = json.dumps(data).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    response = http.request('POST',
                            snark_service_url,
                            body=encoded_data,
                            headers=headers)
    return json.loads(response.data.decode('utf-8'))["proof"]