pragma solidity ^0.4.25;

contract Dataset{
    
    address public dataProvider;
    uint public licence;
    string private link;
    string public dataDescription="default"; //this needs to become a struct!

    // The keyword "public" makes those variables
    // easily readable from outside.
    mapping (address => uint) userTokens;
    mapping (address => address) public mappedUsers;
    address[] public addressIndices;
    
    // Events allow light clients to react to changes efficiently.
    event Sent(address from, address to, uint token);
    event publishedDataset(address publisher, string description, string link, uint licence); // Event
    event updateDataset(address to, string uspdateDescr, string link);

    constructor () public{
                dataProvider=msg.sender;
    }
    
    function publishData(string memory _newdescription, string memory _link, uint _licence) public {
        require(msg.sender == dataProvider);
        dataDescription=_newdescription;
        link=_link;
        licence=_licence;
        emit publishedDataset(msg.sender, _newdescription, link, licence); // Triggering event
    }

    function setLicence(uint newLicence) public{
       dataProvider=msg.sender;
       licence=newLicence;
    //TODO we need to update all of the changes!! 
    //Not focusing here as I am not sure we need to change licences once the data is published.
    }
    
    
    function getLicence() public view returns(uint) {
       return licence;
    }

    //DataRequesters get the link to the data only if the token is right!
    function getLink(uint token) public view returns(string memory){
        require(token==1);
        return link;
    }

    //This is a function to notify the dataRequesters to update the data records
    function updateData(string memory updateDescr, string memory _newlink) public{
        require(dataProvider==msg.sender);
        dataDescription=updateDescr;
        link=_newlink;
        uint arrayLength = addressIndices.length;
        for (uint i=0; i<arrayLength; i++) {
            address to=mappedUsers[addressIndices[i]];
            emit updateDataset(to, updateDescr, link); // Triggering event for all dataRequesters
        }//for
   }

    function addDataRequester(uint purposeCode, uint licenceType) public returns(uint){
       //for now the purpose is a code as the string comparison it's expensive in solidity
       //in the future the purpose should be compared to a field of the overall contract description
        require(purposeCode<=20);
        require(licence==licenceType);
        addressIndices.push(msg.sender); //adding the data requester to an array so that I can loop the mapping of dataRequesters later!
        mappedUsers[msg.sender] = msg.sender;//adding a new data requester (key and value are the same!)!
        userTokens[msg.sender] = 1; //TODO this should become a token generation function!
        uint token=1; //TODO this is a shortcut. tokens should be derived from some verifiable function that cannot be faked
        return token;
    }

    function renewToken(uint compliance) public returns(uint token){
        require(userTokens[msg.sender] > 0, "need to agree on licence first");
        if(licence==compliance){
            emit Sent(msg.sender, dataProvider, userTokens[msg.sender]++);
           token=userTokens[msg.sender]++;
           //TODO add compliance in respect to dataUpdates
           //the compliance that is given in input will need to show that updates were performed
        }
        else{
            userTokens[msg.sender] = 0;
            emit Sent(msg.sender, dataProvider, 0);
            token=0;
        }
        return token;
    }
}