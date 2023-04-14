// SPDX-License-Identifier: MIT
// Tells the Solidity compiler to compile only from v0.8.13 to v0.9.0
pragma solidity >=0.7.0 <0.9.0;

interface IVerifier {
    function verifyProof(
        bytes memory _proof,
        uint256[] memory pubSignals
    ) external returns (bool);
}

contract Commitment {
    uint256[] commitment;

    IVerifier public immutable verifier;

    constructor(IVerifier _verifier, uint256[] memory _commitment) {
        verifier = _verifier;
        commitment = _commitment;
    }

    function Verify(
        bytes memory _proof,
        uint256[] memory _commitment
    ) public returns (bool) {
        return verifier.verifyProof(_proof, _commitment);
    }
}
