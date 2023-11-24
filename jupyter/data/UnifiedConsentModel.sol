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
        uint64 Area_Group_Code;
        uint8[] Area_Country_Code;
        uint64[] Area_Country_Group_Code;
        mapping(uint8 => bool) Area_Country_Code_Map;
        mapping(uint8 => uint128) Disease_Map_Hierarchy;
        mapping(uint16 => bool) Disease_Map;
        uint8[] Disease_Group_Code_Array;
        uint128[] Disease_Category_Code_Array;
        uint16[] Disease_Code_Array;
    }

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    address[] DataSubjectAcc;
    address[] DataRequesterAcc;

    uint8 role_provider = 1;
    uint8 role_requester = 2;

    //    role 1 provider,2 requester

    function TermsByRole(
        uint8 role,
        address _address
    ) internal view returns (Terms storage) {
        if (role == role_provider) {
            // require(msg.sender == dataProvider, "TermsByRole: Invalid sender");
            return providerMapping[_address];
        } else if (role == role_requester) {
            return requesterMapping[_address];
        } else {
            revert("TermsByRole: Invalid role specified");
        }
    }

    function UploadSimpleItems(
        uint8 role,
        address _address,
        uint16 Simple_Items
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Simple_Items = Simple_Items;
    }

    function DisplaySimpleItems(
        uint8 role,
        address _address
    ) public view returns (uint16) {
        Terms storage terms = TermsByRole(role, _address);
        return terms.Simple_Items;
    }

    function UploadDate(
        uint8 role,
        address _address,
        uint16 Start_Year,
        uint16 Start_Month,
        uint16 Start_Day,
        uint16 Months
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Start_Year = Start_Year;
        terms.Start_Month = Start_Month;
        terms.Start_Day = Start_Day;
        terms.Months = Months;
    }

    function DisplayDate(
        uint8 role,
        address _address
    ) public view returns (uint16, uint16, uint16, uint16) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Start_Year,
            terms.Start_Month,
            terms.Start_Day,
            terms.Months
        );
    }

    function UploadAreaCode(
        uint8 role,
        address _address,
        uint64 Group_Code,
        uint8[] memory Country_Code,
        uint64[] memory Country_Group_Code
    ) public {
        // if (Country_Code.length != Country_Group_Code.length) {
        //     revert(
        //         "UploadCountryCode: Country_Code and Country_Group_Code must have the same length"
        //     );
        // }

        Terms storage terms = TermsByRole(role, _address);

        if (role == role_provider) {
            // require(msg.sender == dataProvider);
            for (uint8 i = 0; i < Country_Code.length; i++) {
                terms.Area_Country_Code_Map[Country_Code[i]] = true;
            }
        }

        terms.Area_Country_Code = Country_Code;
        terms.Area_Country_Group_Code = Country_Group_Code;
        // terms.Country_Code = Country_Code;

        terms.Area_Group_Code = Group_Code;
    }

    function DisplayAreaCode(
        uint8 role,
        address _address
    ) public view returns (uint64, uint8[] memory, uint64[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Area_Group_Code,
            terms.Area_Country_Code,
            terms.Area_Country_Group_Code
        );
    }

    function UploadDiseaseCodeHierarchy(
        uint8 role,
        address _address,
        uint8[] memory Disease_Group_Code_Array,
        uint128[] memory Disease_Category_Code_Array
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        if (
            Disease_Group_Code_Array.length !=
            Disease_Category_Code_Array.length
        ) {
            revert(
                "UploadDiseaseCode: Disease_Group_Code_Array and Disease_Category_Code_Array must have the same length"
            );
        }
        if (role == role_provider) {
            for (uint8 i = 0; i < Disease_Group_Code_Array.length; i++) {
                uint8 Disease_Group_Code = Disease_Group_Code_Array[i];
                terms.Disease_Map_Hierarchy[
                    Disease_Group_Code
                ] = Disease_Category_Code_Array[i];
            }
        }
        terms.Disease_Group_Code_Array = Disease_Group_Code_Array;
        terms.Disease_Category_Code_Array = Disease_Category_Code_Array;
    }

    function UploadDiseaseCode(
        uint8 role,
        address _address,
        uint16[] memory Disease_Code_Array
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        if (role == role_provider) {
            for (uint8 i = 0; i < Disease_Code_Array.length; i++) {
                terms.Disease_Map[Disease_Code_Array[i]] = true;
            }
        }
        terms.Disease_Code_Array = Disease_Code_Array;
    }

    function DisplayDiseaseCode(
        uint8 role,
        address _address
    ) public view returns (uint16[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return terms.Disease_Code_Array;
    }

    function DisplayDiseaseCodeHierarchy(
        uint8 role,
        address _address
    ) public view returns (uint8[] memory, uint128[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Disease_Group_Code_Array,
            terms.Disease_Category_Code_Array
        );
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

    function CheckArea(
        address _provider,
        address _requester
    ) public view returns (bool) {
        //check countries, countries of requester must be a subset of countries of provider or the group of countries of requester must be a subset of countries of provider
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester].Area_Country_Code.length;
            index_requester++
        ) {
            uint8 requester_code = requesterMapping[_requester]
                .Area_Country_Code[index_requester];
            bool validCountry = providerMapping[_provider]
                .Area_Country_Code_Map[requester_code] ==
                true ||
                providerMapping[_provider].Area_Group_Code &
                    requesterMapping[_requester].Area_Country_Group_Code[
                        index_requester
                    ] >
                0;
            if (validCountry == false) {
                return false;
            }
        }

        // check groups, group of requester must be a subset of group of provider or the group of requester is 0
        if (
            requesterMapping[_requester].Area_Group_Code == 0 ||
            providerMapping[_provider].Area_Group_Code &
                requesterMapping[_requester].Area_Group_Code ==
            requesterMapping[_requester].Area_Group_Code
        ) {
            return true;
        }

        return false;
    }

    function CheckDisease(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester_address].Disease_Code_Array.length;
            index_requester++
        ) {
            uint16 requester_code = requesterMapping[_requester_address]
                .Disease_Code_Array[index_requester];
            if (
                providerMapping[_provider_address].Disease_Map[
                    requester_code
                ] == false
            ) {
                return false;
            }
        }
        return true;
    }

    // CheckDiseaseHierarchy
    function CheckDiseaseHierarchy(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester_address].Disease_Code_Array.length;
            index_requester++
        ) {
            uint8 requester_group_code = requesterMapping[_requester_address]
                .Disease_Group_Code_Array[index_requester];
            uint128 requester_category_code = requesterMapping[_requester_address]
                .Disease_Category_Code_Array[index_requester];
            uint128 provider_category_code = providerMapping[_provider_address]
                .Disease_Map_Hierarchy[requester_group_code];
            if (
               !(provider_category_code & requester_category_code == requester_category_code)
            ) {
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
        if (CheckArea(_provider_address, _requester_address) == false) {
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
