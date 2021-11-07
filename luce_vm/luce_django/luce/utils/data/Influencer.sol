// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.4.25;

/** 
 * @title Ballot
 * @dev Implements voting process along with vote delegation
 */
contract Influencer {
   
    uint public balance;
    uint public id;
    address public _address;
    
    mapping (uint => Cause) public causes;
    struct Cause {
        uint goal;
        uint balance;
        address cause_address;
    }
    
    constructor(uint _id) public {
        balance = 0;
        _address = msg.sender;
        id = _id;
                
    }   
    
   function addCause(uint _cause_id, uint _goal) public {
       Cause storage c = causes[_cause_id];
       c.goal = _goal;
       c.balance = 0;
       c.cause_address = msg.sender;
   }
   
   function donate(uint _amount, uint _cause_id) public {
        Cause storage c = causes[_cause_id];
        c.balance += _amount;
   }
   
}
