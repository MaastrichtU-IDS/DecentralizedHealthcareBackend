import pytest
import urllib3
import json

from brownie import accounts
from brownie import Commitment
from brownie import PlonkVerifier

TEST_STRING = "test1"


def get_commitment(secret):
    http = urllib3.PoolManager()
    snark_service_url = "http://127.0.0.1:8888/compute_commitment"
    body_json = json.dumps({"secret": secret}).encode('utf-8')
    r = http.request('POST',
                     snark_service_url,
                     body=body_json,
                     headers={'Content-Type': 'application/json'})
    result = json.loads(r.data.decode('utf-8'))
    # print(result)
    return result


@pytest.fixture
def verifier():
    return PlonkVerifier.deploy({"from": accounts[0]})


@pytest.fixture
def commitment(verifier):
    c = get_commitment(TEST_STRING)
    # print(c["public_signals"])
    # print(c)
    return Commitment.deploy(verifier.address, c["solidity_public_signals"], {"from": accounts[0]})


# def test_verifier(verifier):
#     # deploy verifier contract
#     assert verifier.tx.status == 1


# def test_commitment(commitment):
#     # deploy commitment contract
#     assert commitment.tx.status == 1


def test_verify_commitment(commitment):
    # verify commitment
    # assert commitment.verify_commitment() == True
    c = get_commitment(TEST_STRING)
    # proof = c["solidity_proof"]
    call_data = c["call_data"]
    parms = call_data.split(',')
    # print(parms)
    # print(c)
    # print(call_data)
    # decoded_input = commitment.decode_input(call_data)

    # sender = accounts[0]
    # sender.transfer(commitment, data=call_data)
    # print(decoded_input)
    # print(proof)
    verifying_result = commitment.verify(parms[0])
    # print(verifying_result.return_value)
    assert verifying_result.return_value is True
