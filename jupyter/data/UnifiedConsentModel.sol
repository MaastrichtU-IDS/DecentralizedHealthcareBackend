// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentCode {
    event LogMessage(string message);

    address public dataProvider;

    constructor() {
        dataProvider = msg.sender;
    }

    // MARK: - Terms
    struct Terms {
        uint16 Simple_Items;
        uint16 Start_Year;
        uint16 Start_Month;
        uint16 Start_Day;
        uint16 Months;
        uint64 Area_Group_Code;
        uint64 Area_Country_Group_Code_32;
        uint8[] Area_Country_Code;
        uint32[] Area_Country_Group_Code;
        uint256 Area_Country_Code_256;
        mapping(uint8 => bool) Area_Country_Code_Map;
        mapping(uint8 => uint128) Disease_Map_Hierarchy;
        mapping(uint16 => bool) Disease_Map;
        uint8[] Disease_Group_Code_Array;
        uint128[] Disease_Category_Code_Array;
        uint16[] Disease_Code_Array;
        uint256[] Area_Country_Group_Code_Data;
        uint32[] Area_Country_Group_Code_Index;
    }

    struct Term_Requester {
        uint16 Simple_Items;
        uint16 Start_Year;
        uint16 Start_Month;
        uint16 Start_Day;
        uint16 Months;
        uint64 Area_Group_Code;
        uint64 Area_Country_Group_Code_64;
        uint8[] Area_Country_Code;
        uint64[] Area_Country_Group_Code;
        uint256 Area_Country_Code_256;
        mapping(uint8 => bool) Area_Country_Code_Map;
        mapping(uint8 => uint128) Disease_Map_Hierarchy;
        mapping(uint16 => bool) Disease_Map;
        uint8[] Disease_Group_Code_Array;
        uint128[] Disease_Category_Code_Array;
        uint16[] Disease_Code_Array;
        uint256[] Area_Country_Group_Code_Data;
        uint32[] Area_Country_Group_Code_Index;
    }

    // MARK: - provider_area
    struct provider_area {
        uint8 Area_Group_Code;
        // uint256 Area_Country_Code;
        mapping(uint8 => bool) Area_Country_Code_Map;
    }
    // MARK: - requester_area
    struct requester_area {
        uint64 Area_Group_Code;
        uint8[] Area_Country_Code;
        uint8[] Area_Country_Group_Code;
    }

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject
    mapping(address => provider_area) provider_areaMapping; // data subject
    mapping(address => requester_area) requester_areaMapping; // data subject
    address[] DataSubjectAcc;
    address[] DataRequesterAcc;

    uint8 role_provider = 1;
    uint8 role_requester = 2;

    //    role 1 provider,2 requester

    function TermsByRole(
        uint8 role,
        address _address
    ) private view returns (Terms storage) {
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

    // MARK: - UploadAreaSimple
    function UploadAreaSimple(
        uint8 role,
        address _address,
        uint16 Group_Code,
        uint256 Country_Code,
        uint256[] memory Country_Group_Code_Data,
        uint32[] memory Country_Group_Code_Index
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Area_Group_Code = Group_Code;
        terms.Area_Country_Code_256 = Country_Code;
        if (role == role_requester) {
            terms.Area_Country_Group_Code_Data = Country_Group_Code_Data;
            terms.Area_Country_Group_Code_Index = Country_Group_Code_Index;
        }
    }

    // MARK: - UploadAreaOnly
    function UploadAreaOnly(
        uint8 role,
        address _address,
        uint64 Group_Code,
        uint256 Country_Code,
        uint64 country_group_code
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Area_Group_Code = Group_Code;
        terms.Area_Country_Code_256 = Country_Code;
        if (role == role_requester) {
            terms.Area_Country_Group_Code_32 = country_group_code;
        }
    }

    // MARK: - UploadAreaCode
    function UploadAreaCode(
        uint8 role,
        address _address,
        uint8 Group_Code,
        uint8[] memory Country_Code,
        uint8[] memory Country_Group_Code
    ) public {
        if (Country_Code.length != Country_Group_Code.length) {
            revert(
                "UploadCountryCode: Country_Code and Country_Group_Code must have the same length"
            );
        }

        if (role == role_provider) {
            // require(msg.sender == dataProvider);
            // for (uint8 i = 0; i < Country_Code.length; i++) {
            //     provider_areaMapping[_address].Area_Country_Code_Map[
            //         Country_Code[i]
            //     ] = true;
            // }
            // provider_areaMapping[_address].Area_Country_Code = Country_Code;
            provider_areaMapping[_address].Area_Group_Code = Group_Code;
        }
        if (role == role_requester) {
            requester_areaMapping[_address].Area_Country_Code = Country_Code;
            requester_areaMapping[_address]
                .Area_Country_Group_Code = Country_Group_Code;
            requester_areaMapping[_address].Area_Group_Code = Group_Code;
        }
    }

    function DisplayAreaCode(
        uint8 role,
        address _address
    ) public view returns (uint64, uint8[] memory, uint32[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Area_Group_Code,
            terms.Area_Country_Code,
            terms.Area_Country_Group_Code
        );
    } 

    // MARK: - UploadDiseaseCodeHierarchy
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
        if (role == role_requester) {
            terms.Disease_Group_Code_Array = Disease_Group_Code_Array;
            terms.Disease_Category_Code_Array = Disease_Category_Code_Array;
        }
    }

    // MARK: - UploadDiseaseCode
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

        if (role == role_requester) {
            terms.Disease_Code_Array = Disease_Code_Array;
        }
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

    // MARK: - checkAreaSimple
    function checkAreaSimple(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        uint64 provider_group = providerMapping[_provider_address]
            .Area_Group_Code;
        uint64 requester_group = requesterMapping[_requester_address]
            .Area_Group_Code;

        uint256 provider_Area_Country_Code_256 = providerMapping[
            _provider_address
        ].Area_Country_Code_256;
        uint256 requester_Area_Country_Code_256 = requesterMapping[
            _requester_address
        ].Area_Country_Code_256;

        if (
            provider_Area_Country_Code_256 & requester_Area_Country_Code_256 !=
            requester_Area_Country_Code_256
        ) {
            uint256 rest_county = requester_Area_Country_Code_256 &
                ~provider_Area_Country_Code_256;
            uint256[] memory group_country_data = requesterMapping[
                _requester_address
            ].Area_Country_Group_Code_Data;
            uint32[] memory group_country_index = requesterMapping[
                _requester_address
            ].Area_Country_Group_Code_Index;

            uint32 rest_group = 0;
            for (uint8 i = 0; i < group_country_data.length; i++) {
                uint256 country_code_data = group_country_data[i];
                uint32 country_group_index = group_country_index[i];
                if (country_code_data & rest_county > 0) {
                    rest_group += country_group_index;
                }
            }
            if (rest_group & provider_group > 0) {
                return false;
            }
        }

        if ((requester_group & provider_group) == requester_group) {
            return true;
        }
        return false;
    }

    // MARK: - checkArea
    // tags checkArea
    //   === Initialization ===
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
            uint64 requester_group_code = requesterMapping[_requester]
                .Area_Country_Group_Code[index_requester];
            bool validCountry = providerMapping[_provider]
                .Area_Country_Code_Map[requester_code] ==
                true ||
                providerMapping[_provider].Area_Group_Code &
                    requester_group_code >
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
            uint128 requester_category_code = requesterMapping[
                _requester_address
            ].Disease_Category_Code_Array[index_requester];
            uint128 provider_category_code = providerMapping[_provider_address]
                .Disease_Map_Hierarchy[requester_group_code];
            if (
                !(provider_category_code & requester_category_code ==
                    requester_category_code)
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
