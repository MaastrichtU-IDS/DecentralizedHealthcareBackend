
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
    

     
    constructor(uint _id) public {
        balance = 0;
        _address = msg.sender;
        id = _id;
    }
    
    function reduce_balance(uint _amount) returns(bool) {
        if (balance<_amount){
            return false;
        }
        else{
            balance -= _amount;
            return true;
        }
    }
        
    function add_balance(uint _amount){
        if(msg.sender != _address){
            revert("sender is not the owner of the address");
        }
        balance += _amount;
    }
    
    
   
}


contract Influencer {
   
    uint public balance;
    uint public id;
    address public _address;
    
    event Donate(address donor_address, address cause_address, uint amount);
    event CauseAdded(address cause_address, uint goal);

    mapping (uint => Cause) public causes;
    struct Cause {
        bool valid;
        uint goal;
        uint balance;
        address cause_address;
    }
    
    constructor(uint _id) public {
        balance = 0;
        _address = msg.sender;
        id = _id;
                
    }   
    
   function addCause(uint _cause_id, uint _goal, address cause_address) public {
       Cause storage c = causes[_cause_id];
       c.goal = _goal;
       c.balance = 0;
       c.valid = true;
       c.cause_address = cause_address;
       emit CauseAdded(cause_address,_goal);
   }
   
   function donate(uint _amount, uint _cause_id, address donor_contract_address) public {
        Cause storage c = causes[_cause_id];
        if(c.valid != true){
            revert("this cause is not registered");
        }
        Donor donor_contract = Donor(donor_contract_address);
        bool hasbalance = donor_contract.reduce_balance(_amount);
        if (hasbalance != true){
            revert("the donor has insufficient balance");
        }
        c.balance += _amount;
        emit Donate(donor_contract_address, c.cause_address, _amount);

   }

    function add_balance(uint _amount){
        if(msg.sender != _address){
            revert("sender is not the owner of the address");
        }
        balance += _amount;
    }

    function reduce_balance(uint _amount) {
        if (balance<_amount){
            revert("not enough funds");
        }
        else{
            balance -= _amount;
        }
    }
    
   
   
   
}