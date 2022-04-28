// SPDX-License-Identifier: AFL-3.0

pragma solidity ^0.6.2;

contract LUCERegistry {
    // This may be used for administrator control later. Not totally necessary. Can also remain unused.
    address public admin;

    // -------------------------------------- Provider section ---------------------------------------

    // Mapping for provider registration
    mapping(address => bool) public providerRegistry;

    /**
     * @dev Allows any person to register themselves as data provider.
     * @param _provider is the address of the new data provider to be registered. The function fails if
     * the _provider is already registered.
     */
    function newDataProvider(address _provider) external {
        require(
            providerRegistry[_provider] == false,
            "This address is already registered as Provider."
        );
        providerRegistry[_provider] = true;
    }

    /**
     * @dev Allows any person to check whether a certain address belongs to a data provider.
     * @param _provider is the address of data provider in question.
     */
    function checkProvider(address _provider) external view returns (bool) {
        return (providerRegistry[_provider]);
    }

    // -----------------------------------------User section -----------------------------------------

    event newUserRegistered(address indexed user, uint256 license);

    // Maps the license of a data requester to their address. License 0 is default for all addresses, i.e. not registered.
    mapping(address => uint256) public userRegistry;

    /**
     * @dev Allows (currently any) person to register themselves with (currently any) license. This function should
     * introduce more stringent requirements etc. to make sure only authorized usage is allowed.
     * @param newUser is the address of the new user to be registered.
     * @param license is the license of the new user to be registered.
     */
    function registerNewUser(address newUser, uint256 license) external {
        require(userRegistry[newUser] == 0, "User is already registered.");
        userRegistry[newUser] = license;
    }

    /**
     * @dev Returns the license of a user. Not completely necessary, since the mapping is public.
     * @param user is the address of the user whose license is in question.
     */
    function checkUser(address user) external view returns (uint256) {
        return (userRegistry[user]);
    }

    /**
     * @dev Allows any registered user to change their license. This should be controlled by the supervising authority
     * but such control is not yet implemented and not necessarily a good idea because centralized control defeats the
     * purpose of a decentralized ledger.
     * @param newLicense is the new license to be associated with the address of the msg.sender.
     */
    function updateUserLicense(uint256 newLicense) external {
        require(userRegistry[msg.sender] != 0, "User is not yet registered.");
        userRegistry[msg.sender] = newLicense;
    }

    /**
     * @dev Allows a user to deregister themselves.
     */
    function deregister() external {
        userRegistry[msg.sender] = 0;
        providerRegistry[msg.sender] = false;
    }

    constructor() public {
        admin = msg.sender;
    }
}
