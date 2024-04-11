import urllib3
import json


def get_commitment(secret):
    http = urllib3.PoolManager()
    snark_service_url = "http://127.0.0.1:8888/compute_commitment"
    body_json = json.dumps({"secret": secret}).encode('utf-8')
    r = http.request('POST',
                     snark_service_url,
                     body=body_json,
                     headers={'Content-Type': 'application/json'})
    result = json.loads(r.data.decode('utf-8'))
    return result
