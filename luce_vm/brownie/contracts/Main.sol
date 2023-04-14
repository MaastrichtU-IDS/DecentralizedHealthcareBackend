// SPDX-License-Identifier: AFL-3.0
pragma solidity >=0.7.0 <0.9.0;

import "./DataSet.sol";

//import "./generateToken.sol";
contract LuceMain is Dataset {
    constructor(
        IVerifier _verifier,
        uint256[] memory _commitment
    ) Dataset(_verifier, _commitment) {}

    bool private burnPermission = false;

    // This event signals a requester that their token was burned.
    event tokenBurned(
        address userOfToken,
        uint256 tokenId,
        address contractAddress,
        uint256 remainingAccessTime
    );

    function getOwner() public view returns (address) {
        return owner;
    }

    /**
     * @dev This function allows the dataProvider to change the license required for access to the dataset.
     * @param newlicense sets a new license that should be checked whenever a User requests access to the dataset.
     */
    function setlicense(uint256 newlicense) public onlyOwner providerGasCost {
        license = newlicense;
        burnPermission = true;
        uint256 arrayLength = tokens.length;
        // if(arrayLength == 1 && tokens[0].license != newlicense) {
        //     burn(i.add(1)); // Burn requester 1's token.
        // }
        if (arrayLength > 0) {
            for (uint256 i = 0; i < arrayLength; i++) {
                if (tokens[i].license != newlicense) {
                    burn(i + 1); // Burn all previously added tokens that now have the wrong license.
                }
            }
        }
        burnPermission = false;
    }

    /**
     * @dev This function returns the license required for access to the dataset.
     */
    function getlicense() public view returns (uint256) {
        return license;
    }

    function getCompliance(address _requester) public view returns (bool) {
        require(mappedUsers[_requester] > 0 || msg.sender == dataProvider);
        return requesterCompliance[_requester];
    }

    function getTokenId(address _user) public view returns (uint256) {
        require(mappedUsers[_user] > 0 || msg.sender == dataProvider);
        if (msg.sender == dataProvider) {
            return mappedUsers[_user];
        } else {
            uint256 tokenId = mappedUsers[_user];
            require(userOf(tokenId) == msg.sender);
            return tokenId;
        }
    }

    /**
     * @dev This function allows the dataProvider or the user (requester) of a token to delete it, thus relinquishing access to
     *  getLink, or any other token-related function via this token. The token struct will persist, however there is currently no
     * possibility to access it. This would need to be implemented for the supervisory authority.
     * @param tokenId is the token to be burned. A requester can look up their tokenId by calling mappedUsers with their own address.
     */
    function burn(uint256 tokenId) public {
        require(
            userOf(tokenId) == msg.sender ||
                dataProvider == msg.sender ||
                burnPermission
        );
        address user = userOf(tokenId);
        uint256 accessTime = tokens[tokenId - 1].accessTime;
        uint256 remainingAccessTime = 0;
        if (accessTime > block.timestamp) {
            // access has expired
            remainingAccessTime = remainingAccessTime =
                accessTime -
                block.timestamp; // access not yet expired
        }
        // tokens[tokenId].burned = true;
        _burn(tokenId);
        emit tokenBurned(user, tokenId, address(this), remainingAccessTime);
        mappedUsers[user] = 0; // indicate the user no longer has a token
        if (msg.sender == user) {
            // If the data requester issues deletion of their token, they also intrinsicly agree to delete their copy of the dataset
            requesterCompliance[user] = true;
        } else {
            requesterCompliance[user] = false; // Since the user doesn't have access anymore, they inherently comply (soft compliance).
            // Hard compliance must be verified by the supervisory authority, if it is in question.
        }
    }

    /**
     * @dev This function first adds a new data Requester to the relevant mapping, then creates a token to access the link
     * to the data, and then transfers User-rights to the data Requester. Before this function is called, it is advisable
     * that the requester calls the expectedCosts function to make sure they submit the correct msg.value in their
     * transaction.
     * @param purposeCode represents the purpose the requester wants to use the requested data for. The provider will be
     * able to control this via the consent contract (unfinished)
     * @param accessTime is the amount of time in seconds the data should be available to the data requester. If 0 is passed
     * to this value, the function will set a standard 2 weeks accessTime. This parameter is mainly for testing purposes.
     */
    function addDataRequester(
        uint256 purposeCode,
        uint256 accessTime
    ) public payable returns (uint256) {
        require(unpublished == false, "1");
        LUCERegistry c = LUCERegistry(registry);

        uint256 userLicense = c.checkUser(msg.sender);

        // Make sure the requester's license matches with the provider's requirements
        require(license == userLicense, "2");
        // Make sure the requester's purpose matches the 'requirements' (this is where the consent contract will interface)
        require(purposeCode <= 20, "3");
        // Make sure the requester doesn't have a token yet.
        require(mappedUsers[msg.sender] == 0, "already have token");

        ConsentCode cc = ConsentCode(consent);
        bool accessGranted = cc.AccessData(dataProvider, msg.sender);
        require(accessGranted, "5");

        addressIndices.push(msg.sender); //adding the data requester to an array so that I can loop the mapping of dataRequesters later!

        // Calculate the amount an individual requester must pay in order to receive access and make sure their transferred value matches.
        if (scenario > 1) {
            uint256 individualCost = (currentCost * (costMult)) / (costDiv);
            require(msg.value == individualCost, "6");

            // Adjust the true contract cost by subtracting the value this requester transferred.
            if (currentCost < individualCost) {
                // Values smaller than 0 are not allowed in solidity.
                currentCost = 0;
            } else {
                currentCost = currentCost - (individualCost);
            }
        }

        // Token generation
        if (accessTime == 0) {
            accessTime = 2 weeks;
        }
        _createRequestedToken(license, purposeCode, accessTime); // Creates a token.
        uint256 tokenId = tokens.length; // ID of the token that was just created. Note that solidity is 0-indexed.
        _safeMint(dataProvider, tokenId); // Mints the token to the dataProvider and gives them complete control over it.
        _safeTransfer(dataProvider, msg.sender, tokenId, ""); // Allows access of the created token to the requester.
        emit Sent(dataProvider, msg.sender, tokenId);
        // A requester can look up their token by calling the mappedUsers mapping with their own address.
        mappedUsers[msg.sender] = tokenId; // This proves the requester has received a token and cannot receive another one
        // Compliance initialization for the data requester:
        requesterCompliance[msg.sender] = true;
        return tokenId;
    }

    function getAccessTime(uint256 tokenId) public view returns (uint256) {
        require(userOf(tokenId) == msg.sender || dataProvider == msg.sender);
        return (tokens[tokenId - 1].accessTime);
    }

    function confirmCompliance() public {
        require(mappedUsers[msg.sender] > 0);
        requesterCompliance[msg.sender] = true;
    }

    // function resetCompliance(uint tokenId) public {
    //     require (tokens.length<tokenId, "Querying for nonexistent token.");
    //     require (tokens[tokenId].burned == true, "The token in question was not burned");
    //     require (tokens[tokenId].requester == msg.sender, "Operation not authorized.");
    //     LUCERegistry c = LUCERegistry(registry);
    //     uint requesterLicense = c.checkUser(msg.sender);
    //     require (tokens[tokenId].license != requesterLicense, "License of requester did not change.");
    //     requesterCompliance[msg.sender] = true;
    // }

    /**
     * @dev This function allows a data requester to renew or add to their access time to the dataset. It is advisable to
     * call the expectedCosts function to make sure the correct value is transferred with the transaction.
     * @param newAccessTime is the amount of time to be added to the requester's current access time.
     */
    function renewToken(uint256 newAccessTime) public payable {
        uint256 tokenId = mappedUsers[msg.sender]; // This defaults to 0 in case the requester doesn't own a token. TokenId 0 is invalid.
        require(userOf(tokenId) == msg.sender);
        require(requesterCompliance[msg.sender]);
        // Calculates the value the requester must pay to call this function and checks whether the amount transferred matches.
        if (scenario > 1) {
            uint256 individualCost = (currentCost * (costMult)) / (costDiv);
            require(msg.value == individualCost);

            // Adjust the true contract cost by subtracting the value this requester transferred.
            if (currentCost < individualCost) {
                // Values smaller than 0 are not allowed in solidity.
                currentCost = 0;
            } else {
                currentCost = currentCost - (individualCost);
            }
        }
        if (newAccessTime == 0) {
            newAccessTime = 2 weeks;
        }
        if (tokens[tokenId - 1].accessTime > block.timestamp) {
            tokens[tokenId - 1].accessTime =
                tokens[tokenId - 1].accessTime +
                (newAccessTime);
        } else {
            tokens[tokenId - 1].accessTime = block.timestamp + (newAccessTime);
        }
    }

    /**
     * @dev This function returns the amount the next requester in line needs to pay in return for access.
     */
    function expectedCosts() public view returns (uint256) {
        if (scenario == 1) {
            return 0;
        }
        //returns the expected costs for the next data Requester
        uint256 individualCost = (currentCost * (costMult)) / (costDiv);
        return (individualCost);
    }

    /**
     * @dev Returns the contract balance. Only callable by the dataProvider.
     */
    function contractBalance() public view returns (uint256) {
        require(
            msg.sender == dataProvider,
            "Only the data provider can extract funds from the contract."
        );
        return uint256(address(this).balance);
    }

    /**
     * @dev Transfers all funds from the contract to the dataProvider. Only callable by the dataProvider.
     */
    function receiveFunds() public onlyOwner providerGasCost {
        payable(msg.sender).transfer(address(this).balance); //this could just be the balance of the contract
    }
}
