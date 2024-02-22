// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract MimicMixingService {
    uint256 public deposits;

    function deposit() public payable {
        require(msg.value > 0, "Deposit amount must be greater than zero");
        deposits += msg.value;
    }

    function withdrawToDisposable(
        address payable disposableAddress,
        uint256 amount
    ) public {
        disposableAddress.transfer(amount);
        deposits -= amount;
    }
}
