// SPDX-License-Identifier: AFL-3.0
pragma solidity >=0.7.0 <0.9.0;

import "./LuceRegistry.sol";
import "./Token.sol";
import "./Commitment.sol";

contract Dataset is ERC721, Commitment {
    // Contract testing variables
    uint256 public scenario;

    // About the data provider and dataset
    address public dataProvider;
    uint256 public license;
    string private link;
    string public dataDescription = "default"; //this needs to become a struct when the consent contract is integrated.
    bool internal unpublished;

    // Registry
    address internal registry;
    address internal consent;
    address payable owner;

    // Cost variables
    uint256 public currentCost;
    uint256 internal costMult;
    uint256 internal costDiv;
    uint256 public profitMargin;

    // The keyword "public" makes those variables easily readable from outside.
    // mapping from user address to token id
    mapping(address => uint256) internal mappedUsers;
    mapping(address => bool) internal requesterCompliance;
    address[] internal addressIndices;

    // Events allow light clients to react to changes efficiently.
    event Sent(address from, address to, uint256 token); // currently unused.
    event publishedDataset(
        address publisher,
        string description,
        uint256 license
    );
    event updateDataset(address to, string uspdateDescr);

    /**
     * @dev This modifier calculates the gas cost of any function that is called with it and adds the result to the contract's
     * currentCost.
     */
    modifier providerGasCost() {
        uint256 remainingGasStart = gasleft();

        _;

        uint256 remainingGasEnd = gasleft();
        uint256 usedGas = remainingGasStart - remainingGasEnd;
        // Add intrinsic gas and transfer gas. Need to account for gas stipend as well.
        // usedGas.add(30700);
        usedGas = usedGas + 30700;
        // Possibly need to check max gasprice and usedGas here to limit possibility for abuse.
        // uint256 gasCost = usedGas.mul(tx.gasprice).mul(profitMargin).div(100); // in wei
        uint256 gasCost = (usedGas * tx.gasprice * profitMargin) / 100;
        // Add gas cost to total
        // currentCost = currentCost.add(gasCost);
        currentCost = currentCost + gasCost;
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function.");
        _;
    }

    // function claimOwnership(
    //     int256 dataset_id,
    //     bytes memory _proof
    // ) public onlyVerified(_proof) {}

    function setScenario(
        uint256 _scenario,
        uint256 _profitMargin
    ) public onlyOwner {
        scenario = _scenario;
        setProfitMargin(_profitMargin);
    }

    function destroy() public onlyOwner {
        selfdestruct(owner);
    }

    /**
     * @dev This function lets the dataProvider save the address of the general registry contract to make sure requesters are
     * registered and possess the correct license.
     * @param userRegistry is the address of the general registry contract this contract should call on whenever validating
     * data requesters.
     */
    function setRegistryAddress(address userRegistry) public {
        registry = userRegistry;
    }

    /**
     * @dev This function lets the dataProvider save the address of the consent contract to make sure requesters are
     * registered and possess the correct license.
     * @param userConsent is the address of the general consent contract this contract.
     */
    function setConsentAddress(address userConsent) public providerGasCost {
        consent = userConsent;
    }

    /**
     * @dev Initializes the dataset.
     * @param _description sets the description of the dataset.
     * @param _link sets the link to the dataset, which may be shared to Users through tokens.
     * @param _license sets the license which is needed to get access to the dataset.
     */
    function publishData(
        string memory _description,
        string memory _link,
        uint256 _license
    ) public {
        require(unpublished == true, "1");

        // LUCERegistry c = LUCERegistry(registry);
        // ConsentCode cc = ConsentCode(consent);

        // address[] memory dataSubjects = cc.displayDataSubjectAcc();
        // require(dataSubjects.length != 0, "2");

        // bool registered = c.checkProvider(msg.sender);
        // require(registered, "3");

        dataDescription = _description;
        license = _license;
        link = _link;
        emit publishedDataset(msg.sender, _description, license); // Triggering event
        unpublished = false;
    }

    /**
     * @dev Public function to return the link of the dataset, callable only by the dataProvider or authorized data requesters.
     * This function should become more or less obsolete once we implement the checksum for data access.
     */
    function getLink() public view returns (string memory) {
        return link;

        // if (msg.sender == dataProvider) {
        //     return link;
        // }
        // require(requesterCompliance[msg.sender], "1");
        // uint256 tokenId = mappedUsers[msg.sender];
        // require(userOf(tokenId) == msg.sender, "2");
        // require(tokens[tokenId - 1].accessTime > block.timestamp, "3");
        // return link;
    }

    function getAllDataRequesters()
        public
        view
        onlyOwner
        returns (address[] memory)
    {
        require(addressIndices.length > 0);
        return addressIndices;
    }

    /**
     * @dev This function allows the dataProvider to update the description of and link to their dataset.
     * @param updateDescr is the new description of the dataset.
     * @param newlink is the new link to the dataset.
     */
    function updateData(
        string memory updateDescr,
        string memory newlink
    ) public onlyOwner providerGasCost {
        require(unpublished == false);
        dataDescription = updateDescr;
        link = newlink;

        uint256 arrayLength = tokens.length;
        if (arrayLength > 0) {
            for (uint256 i = 0; i < arrayLength; i++) {
                if (_exists(i + 1)) {
                    address to = userOf(i + 1);
                    if (tokens[i].accessTime >= block.timestamp) {
                        requesterCompliance[to] = false; // This is false until the requester reconfirms their compliance.
                        emit updateDataset(to, updateDescr); // Triggering event for all dataRequesters.
                    }
                    if (requesterCompliance[to] == true) {
                        requesterCompliance[to] = false; // This is false until the requester reconfirms their compliance.
                        emit updateDataset(to, updateDescr); // Triggering event for all dataRequesters.
                    }
                }
            }
        }
    }

    /**
     * @dev This is a workaround to set the correct initial cost of deploying the contract. It may also be used to control
     * the contract cost (artificial cost). This function should be called right after the contract is deployed. Possibly, it
     * should be callable only once, but this is not implemented.
     * @param price is the total cost requesters will have to pay whenever requesting access to the data.
     */
    function setPrice(uint256 price) public onlyOwner providerGasCost {
        currentCost = price;
    }

    /**
     * @dev This function lets the data provider set the fixed profitMargin they want to achieve by sharing this dataset.
     * @param _profitMargin is the percentage profit margin the provider strives for. Standard is 100, i.e. no-profit.
     */
    function setProfitMargin(
        uint256 _profitMargin
    ) public onlyOwner providerGasCost {
        profitMargin = _profitMargin;
    }

    /**
     * @dev This function allows the dataProvider to control what percentage of the current contract cost (currentCost)
     * any requester should pay.
     * @param mult is the numerator in the calculation.
     * @param div is the denominator in the calculation.
     */
    function setMultis(
        uint256 mult,
        uint256 div
    ) public onlyOwner providerGasCost {
        require(mult <= div);
        costMult = mult;
        costDiv = div;
    }

    constructor(
        IVerifier _verifier,
        uint256[] memory _commitment
    ) ERC721("Test", "TST") Commitment(_verifier, _commitment) {
        owner = payable(msg.sender);
        dataProvider = msg.sender;
        currentCost = 1e9; // hopefully this is 1 shannon (giga wei)
        costMult = 1;
        costDiv = 3;
        unpublished = true;
        profitMargin = 100; // Cover costs exactly => scenario 2
        scenario = 2; // Initialize contract as scenario 2
    }
}
