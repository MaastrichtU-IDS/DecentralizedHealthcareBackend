
pragma solidity ^0.4.25;


 contract Donor {
   
    uint public balance;
    uint public id;
    address public _address;
    
    
    constructor(uint _id) public {
        balance = 0;
        _address = msg.sender;
        id = _id;
    }
    
    
    /*
        this function is called by the owner of the contract when it wants to make 
        a donation to a specific cause. The amount that is donated will be transfered from 
        the donor contract to the influencer contract.
    */
    function donate(uint _cause_id, uint amount, address influencer_contract_address) public {
        require(msg.sender == _address, "permission denied");
        require(amount<=address(this).balance, "not enough funds in contract");
        Influencer i = Influencer(influencer_contract_address);
        i.deposit.value(amount)(_cause_id);
   }
   
   
    /*
        this function is called by the owner of the contract when it wants to make 
        a donation to a agroup of causes created by the influencer. The amount that is donated 
        will be transfered from the donor contract to the influencer contract.
    */
   function donateToGroup(uint group_id, uint amount, address influencer_contract_address) public {
        require((amount / 10000) * 10000 == amount , 'too small');
        require(msg.sender == _address, "permission denied");
        require(amount<=address(this).balance, "not enough funds in contract");
        Influencer i = Influencer(influencer_contract_address);
        (, uint[] memory causes, uint[] memory splits) = i.getGroup(group_id);
        uint amount_sum = 0;
        for(uint j = 0; j<causes.length; j++){
            uint slice = (amount / 10000)*splits[j];
            amount_sum += slice;
            i.deposit.value(slice)(causes[j]);
        }
        require(amount_sum == amount, "the distribution doesn't add up");
   }
   
   
    // withdraw the amount specified from the donor contract to the donor address.
    function withdraw(uint amount) public {
        require(msg.sender == _address, "permission to withdraw denied");
        msg.sender.transfer(amount);
    }
    
    
    //deposit the value specified form the caller to the donor contract
    function deposit() payable public {}
    
    
    //fetch the value balance of the contract
     function getBalance() public view returns (uint256) {
        return address(this).balance;
    }
}


contract Influencer {
    
    uint public balance; //part of the contract balance that the influencer is entitled to withdraw.
    uint public id;
    address public _address;
    
    mapping (uint => Cause) public causes;
    mapping (uint => CauseGroup) public groups;
    
    struct Cause {
        bool valid;
        uint goal; 
        uint balance;   //part of the contract balance that this cause is entitled to withdraw.
        uint percentBPS; 
        address cause_address;
    }
    struct CauseGroup{
        bool valid;
        uint[]  causes;
        uint[]  splits;
    }
   
     //EVENTS 
     
    event CauseCreated(address indexed cause_address, uint goal, uint percentBPS);
    event CauseReachedGoal(address indexed cause_address, uint goal, uint balance, uint percentBPS);
    event CauseWithdraw(address indexed cause_address, uint goal , uint percentBPS, uint amount);
    
                        //0: cause added, 1:cause removed
    event GroupChanged(uint indexed changeType, uint indexed group_id, uint indexed cause_id, uint[] split);
    event GroupCreated(uint indexed group_id, uint[] causes, uint[] splits);
    event GroupDeleted(uint indexed group_id);
    
    event InfluencerWithdraw(address indexed influencer_address, uint balance, uint amount);
    
    event Donate(address indexed donor_address, address indexed cause_address, uint amount);

    
    
    constructor(uint _id) public  {
        balance = 0;
        _address = msg.sender;
        id = _id;
    }   

    /*
    add a cause to the causes mapping. Specify an id, goal, address, and a percent expressed in basis points
    that represents how much of each donation will go to the cause, the rest will go to the influencer balance.
    */
   function addCause(uint _cause_id, uint _goal, address cause_address, uint percentBPS) public {
       require(percentBPS >= 0 && percentBPS <= 10000, "invalid percentage basis point");
       require(msg.sender == _address, "permission denied");
       Cause storage c = causes[_cause_id];
       require(c.valid == false, "cause already exist");
       c.goal = _goal;
       c.balance = 0;
       c.valid = true;
       c.cause_address = cause_address;
       c.percentBPS = percentBPS;
       emit CauseCreated(cause_address,_goal,percentBPS);
   }
   

    /*
    withdraw funds from the contract to the influencer address.
    the influencer can only withraw what he is entitled to (i.e. the amount stored in the balance variable).
    */
    function withdrawInfluencer(uint amount) public {
        require(msg.sender == _address, "permission to withdraw denied");
        require(amount <= balance, 'cannot withdraw more than balance');
         msg.sender.transfer(amount);
         balance -= amount;
         emit InfluencerWithdraw(_address, balance, amount);
    }
    
    
    /*
    withdraw funds from the contract to the cause address.
    the cause can only withraw what he is entitled to (i.e. the amount stored in the Cause.balance variable).
    */
    function withdrawCause(uint amount, uint _cause_id) public {
        Cause storage c = causes[_cause_id];
        require(c.valid == true, "this cause is not registered");
        require(msg.sender == c.cause_address, "permission to withdraw denied");
        require(amount <= c.balance, 'cannot withdraw more than balance');
        msg.sender.transfer(amount);
        c.balance -= amount;
        emit CauseWithdraw(c.cause_address, c.goal, c.percentBPS, amount);
    }
    
    
    /*
    deposit value specified into the contract. The value will be authomatically 
    split between what the Influencer is entitled to and what the cause is 
    entitled to.
    Note: any eth address can call this function not only a donor contract. (should this change?)
    */
    function deposit(uint cause_id) payable external {
        uint _amount = msg.value;
        address donor_contract_address = msg.sender;
        Cause storage c = causes[cause_id];
        require(c.valid == true, "this cause is not registered");
        require((_amount / 10000) * 10000 == _amount , 'amount too small');
        require(msg.sender == donor_contract_address, "" );
        uint to_cause = (_amount / 10000)*c.percentBPS;
        uint to_influencer = _amount - to_cause;
        c.balance += to_cause;
        balance += to_influencer;
        require(to_cause + to_influencer == _amount , 'invalid split');
        emit Donate(donor_contract_address, c.cause_address, _amount);
        if(c.balance >= c.goal){
            emit CauseReachedGoal(c.cause_address, c.goal, c.balance, c.percentBPS);
        }
    }
    
    
    /*
    create a group of causes. a splits array and a causes ids array must be specified. They 
    represent the percentage of every donation that each cause in the group is entitled to.
    */
    function createGroup(uint[] _causes_ids, uint[] _splits, uint group_id) public {
        require(msg.sender == _address, "permission to create group denied");
        require(_causes_ids.length == _splits.length, "incompatible length"); //every percentage must correspond to a cause and vice versa
        uint sum_splits = 0;
        for(uint i = 0; i<_splits.length; i++){
            sum_splits += _splits[i];
            Cause storage c = causes[_causes_ids[i]];
            require(c.valid == true, "cause does not exist"); 

        }
        require(sum_splits == 10000, "the split must sum up to 100%");
        CauseGroup storage cg = groups[group_id];
        require(cg.valid == false, "group id already exist");
        cg.causes = _causes_ids;
        cg.splits = _splits;
        cg.valid = true;
        emit GroupCreated(group_id, cg.causes, cg.splits);
    }
    
    
    //delete group
    function deleteGroup(uint groupid) public {
        require(msg.sender == _address, "permission to delete group denied");
        CauseGroup storage cg = groups[groupid];
        require(cg.valid == true, "group does not exist");
        cg.valid = false;
        emit GroupDeleted(groupid);
        
    }
    
    
    //add a singular cause to an existing group. a new split must be specified.
    function addCauseToGroup(uint groupid, uint causeid, uint[] newsplit) public {
        require(msg.sender == _address);
        CauseGroup storage cg = groups[groupid];
        require(cg.valid == true, "group id is not registered");
        for(uint i=0; i<cg.causes.length; i++){
            require(cg.causes[i] != causeid, "cause already exist");
        }
        cg.causes.push(causeid);
        changeGroupSplit(groupid, newsplit);
        emit GroupChanged(0, groupid, causeid, newsplit);
    }
    
    
    //remove a singular cause to an existing group. a new split must be specified.
    function removeCauseFromGrouop(uint groupid, uint causeid, uint[] newsplit) public {
        require(msg.sender == _address);
        CauseGroup storage cg = groups[groupid];
        require(cg.valid == true, "group id is not registered");
        for(uint i = 1; i<cg.causes.length; i++){
            if(cg.causes[i] == causeid){
                remove(i, cg.causes);
            }
        }
        changeGroupSplit(groupid, newsplit);
        emit GroupChanged(1, groupid, causeid, newsplit);

    }
    
    //utility function
    function remove(uint ind, uint[] storage array) private returns(uint[]) {
        delete array[ind];
        for (uint j = ind; j<array.length;j++) {
            if (j==array.length-1) {
                break;
            }else {
                array[j] = array[j+1];
            }
        }
        array.length--;
        return array;
    }
    
    //set the split of a group
    function changeGroupSplit(uint groupid, uint[] newsplit) public {
        require(msg.sender == _address);
        uint split_sum = 0;
        for(uint i=0; i<newsplit.length; i++){
            require(newsplit[i]>=0 && newsplit[i]<= 10000, "incorrect split sum");
            split_sum += newsplit[i];
        }
        require(split_sum == 10000, "incorrect split sum");
        CauseGroup storage cg = groups[groupid];
        require(cg.causes.length == newsplit.length, "worong split length");
        cg.splits = newsplit;
    }
    
    //fetch the balance of the contract
    function getContractBalance() public view returns (uint256) {
        return address(this).balance;
        
    }
    
    
    //fetch info of a group with group_id
    function getGroup(uint _group_id)public view returns (bool, uint[], uint[]){
        CauseGroup storage cg = groups[_group_id];
        require(cg.valid == true, "group does not exist");
        return (cg.valid, cg.causes, cg.splits);
    }
    
}

