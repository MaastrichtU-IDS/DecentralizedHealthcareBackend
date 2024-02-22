// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

// Interface definition for a Zero-Knowledge Proof verifier.
interface IVerifier {
    function verifyProof(
        bytes memory _proof,
        uint256[] memory pubSignals
    ) external returns (bool);
}

// This contract allows a data provider to send and store cryptographic commitments of data sets.
// The stored commitments can then be used to verify the ownership of the provided data sets using Zero-Knowledge Proofs.
contract Commitment {
    uint256[] commitment;

    IVerifier public immutable verifier;

    constructor(IVerifier _verifier, uint256[] memory _commitment) {
        verifier = _verifier;
        commitment = _commitment;
    }

    function verify(bytes memory _proof) public returns (bool) {
        return verifier.verifyProof(_proof, commitment);
    }

    modifier onlyVerified(bytes memory _proof) {
        require(verify(_proof), "Proof verification failed");
        _;
    }
}
