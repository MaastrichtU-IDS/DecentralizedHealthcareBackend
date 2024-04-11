import pytest

from brownie import accounts
from brownie import PrivacyShieldDataset
from brownie import PlonkVerifier
from brownie import Commitment
from utils import get_commitment

TEST_STRING = "test1"


@pytest.fixture
def verifier():
    return PlonkVerifier.deploy({"from": accounts[0]})


@pytest.fixture
def privacy_shield_dataset(verifier):
    public_signals = get_commitment(TEST_STRING)["solidity_public_signals"]
    return PrivacyShieldDataset.deploy(verifier.address, public_signals, {"from": accounts[0]})


def test_privacy_shield_dataset(privacy_shield_dataset):

    c = get_commitment(TEST_STRING)
    call_data = c["call_data"]
    parms = call_data.split(',')

    commitment = privacy_shield_dataset.getCommitment(parms[0])

    print("commitment", commitment)
