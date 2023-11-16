// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentCode {
    event LogMessage(string message);

    address public dataProvider;

    constructor() {
        dataProvider = msg.sender;
    }

    struct Terms {
        uint16 Simple_Items;
        uint16 Start_Year;
        uint16 Start_Month;
        uint16 Start_Day;
        uint16 Months;
        uint16[] Disease_Code_Array;
        uint64 Group_Code;
        uint8[] Country_Code;
        uint64[] Country_Group_Code;
    }

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    address[] DataSubjectAcc;
    address[] DataRequesterAcc;

    //    role 1 provider,2 requester

    function TermsByRole(
        address _address,
        uint8 role
    ) internal view returns (Terms storage) {
        if (role == 1) {
            require(msg.sender == dataProvider);
            return providerMapping[_address];
        } else if (role == 2) {
            return requesterMapping[_address];
        } else {
            revert("Invalid role");
        }
    }

    function UploadSimpleItems(
        uint8 role,
        address _address,
        uint16 Simple_Items
    ) public {
        Terms storage terms = TermsByRole(_address, role);
        terms.Simple_Items = Simple_Items;
    }

    function Display(
        uint8 role,
        address _address
    ) public view returns (uint16) {
        Terms storage terms = TermsByRole(_address, role);
        return terms.Simple_Items;
    }

    function UploadSimpleItemsProvider(
        address _address,
        uint16 Simple_Items
    ) public {
        require(msg.sender == dataProvider);
        providerMapping[_address].Simple_Items = Simple_Items;
    }

    function UploadDateProvider(
        address _address,
        uint16 Start_Year,
        uint16 Start_Month,
        uint16 Start_Day,
        uint16 Months
    ) public {
        require(msg.sender == dataProvider);
        providerMapping[_address].Start_Year = Start_Year;
        providerMapping[_address].Start_Month = Start_Month;
        providerMapping[_address].Start_Day = Start_Day;
        providerMapping[_address].Months = Months;
    }

    function UploadDateRequester(
        address _address,
        uint16 Start_Year,
        uint16 Start_Month,
        uint16 Start_Day,
        uint16 Months
    ) public {
        requesterMapping[_address].Start_Year = Start_Year;
        requesterMapping[_address].Start_Month = Start_Month;
        requesterMapping[_address].Start_Day = Start_Day;
        requesterMapping[_address].Months = Months;
    }

    function UploadCountryCodeRequester(
        address _address,
        uint32 Group_Code,
        uint256 Country_Code,
        uint32 Country_Group_Code
    ) public {
        requesterMapping[_address].Country_Code = Country_Code;
        requesterMapping[_address].Country_Group_Code = Country_Group_Code;
        requesterMapping[_address].Group_Code = Group_Code;
    }

    function UploadCountryCodeProvider(
        address _address,
        uint32 Group_Code,
        uint256 Country_Code,
        uint32 Country_Group_Code
    ) public {
        require(msg.sender == dataProvider);
        providerMapping[_address].Country_Code = Country_Code;
        providerMapping[_address].Country_Group_Code = Country_Group_Code;
        providerMapping[_address].Group_Code = Group_Code;
    }

    function UploadDiseaseCodeRequester(
        address _address,
        uint16[] memory Disease_Code_Array
    ) public {
        requesterMapping[_address].Disease_Code_Array = Disease_Code_Array;
    }

    function UploadDiseaseCodeProvider(
        address _address,
        uint16[] memory Disease_Code_Array
    ) public {
        require(msg.sender == dataProvider);
        providerMapping[_address].Disease_Code_Array = Disease_Code_Array;
    }

    function CheckBooleanItems(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        uint16 providerData = providerMapping[_provider_address].Simple_Items;
        uint16 requesterData = requesterMapping[_requester_address]
            .Simple_Items;
        if ((requesterData & providerData) == requesterData) {
            return true;
        }
        return false;
    }

    function CheckCountry(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        bool hasValidCountries = (requesterMapping[_requester_address]
            .Country_Code &
            providerMapping[_provider_address].Country_Code ==
            requesterMapping[_requester_address].Country_Code) ||
            (requesterMapping[_requester_address].Country_Group_Code &
                providerMapping[_provider_address].Group_Code ==
                requesterMapping[_requester_address].Country_Group_Code);

        bool hasValidGroupCode = requesterMapping[_requester_address]
            .Group_Code !=
            0 &&
            requesterMapping[_requester_address].Group_Code &
                providerMapping[_provider_address].Group_Code ==
            requesterMapping[_requester_address].Group_Code;

        if (hasValidCountries || hasValidGroupCode) {
            return true;
        } else {
            return false;
        }
    }

    function CheckDisease(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        bool disease_flag = false;
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester_address].Disease_Code_Array.length;
            index_requester++
        ) {
            uint16 requester_code = requesterMapping[_requester_address]
                .Disease_Code_Array[index_requester];
            disease_flag = false;
            for (
                uint index_provider = 0;
                index_provider <
                providerMapping[_provider_address].Disease_Code_Array.length;
                index_provider++
            ) {
                uint16 provider_code = providerMapping[_provider_address]
                    .Disease_Code_Array[index_provider];
                if (
                    requester_code & provider_code == provider_code &&
                    requester_code >= provider_code
                ) {
                    // ensure the provider code is a subset of the requester code
                    // given provider 1100,  requester  1110 is granted but 1011 is not
                    disease_flag = true;
                    break;
                }
            }
            if (disease_flag == false) {
                return false;
            }
        }
        return true;
    }

    function CheckDate(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        if (
            requesterMapping[_requester_address].Start_Year >
            providerMapping[_provider_address].Start_Year
        ) {
            return true;
        }
        if (
            requesterMapping[_requester_address].Start_Year <
            providerMapping[_provider_address].Start_Year
        ) {
            return false;
        }
        // year now equal
        if (
            requesterMapping[_requester_address].Start_Month >
            providerMapping[_provider_address].Start_Month
        ) {
            return true;
        }
        if (
            requesterMapping[_requester_address].Start_Month <
            providerMapping[_provider_address].Start_Month
        ) {
            return false;
        }
        // month now equal
        if (
            requesterMapping[_requester_address].Start_Day >=
            providerMapping[_provider_address].Start_Day
        ) {
            return true;
        }
        if (
            requesterMapping[_requester_address].Start_Day <
            providerMapping[_provider_address].Start_Day
        ) {
            return false;
        }

        return true;
    }

    function AccessData(
        address _provider_address,
        address _requester_address
    ) public view returns (uint8) {
        if (CheckCountry(_provider_address, _requester_address) == false) {
            return 1;
        }

        if (CheckDisease(_provider_address, _requester_address) == false) {
            return 2;
        }

        if (CheckDate(_provider_address, _requester_address) == false) {
            return 3;
        }

        if (CheckBooleanItems(_provider_address, _requester_address) == false) {
            return 4;
        }
        return 0;
    }
}
