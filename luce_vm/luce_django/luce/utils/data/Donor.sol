// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.4.25;

/** 
 * @title Ballot
 * @dev Implements voting process along with vote delegation
 */
contract Donor {
   
    uint public balance;
    uint public id;
    address public _address;
    
    constructor(uint _id) {
        balance = 0;
        _address = msg.sender;
        id = _id;
                
    }
    
   
}
