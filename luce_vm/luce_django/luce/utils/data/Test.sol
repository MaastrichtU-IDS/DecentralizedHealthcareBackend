// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.6.2;

contract Test{
    int private number;

    function setNumber(int a) public {
        require(a!=1, "number not valid");
        number = a;
    }

    function getNumber() public view returns(int) {
        return number;
    }


}