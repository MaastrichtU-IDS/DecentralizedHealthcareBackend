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
        // start area
        // start binary
        uint64 Area_Group_Simple;
        uint256 Area_Country_Simple;
        uint16 Area_Simple_Version;
        // end binary
        // uint64 Area_Country_Group_Code_32;

        uint32[] Area_Country_Group_Code;
        // uint256[] Area_Country_Group_Code_Data;
        // uint32[] Area_Country_Group_Code_Index;
        // start baseline
        uint8[] Area_Country_List_Baseline;
        uint8[] Area_Group_List_Baseline;
        mapping(uint8 => bool) Area_Country_Map_Baseline;
        mapping(uint8 => bool) Area_Group_Map_Baseline;
        // start desease
        mapping(uint8 => uint128) Disease_Map_Hierarchy;
        mapping(uint16 => bool) Disease_Map;
        uint8[] Disease_Group_Code_Array;
        uint128[] Disease_Category_Code_Array;
        uint16[] Disease_Code_Array;
    }

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    uint8 role_provider = 1;
    uint8 role_requester = 2;
    uint256[] Country_Group_Code_Data;
    uint32[] Country_Group_Code_Index;
    uint8[][] Country_Group_baseline;

    uint16 Area_Simple_Version = 0;

    // uint8[] Country_Code_8;
    // uint32[] Country_Group_Code_32;
    mapping(uint8 => uint32) Country_Code_Mapping;
    mapping(uint8 => uint8[]) Country_Group_Code_Mapping_Baseline;
    mapping(uint8 => mapping(uint32 => bool)) Country_Group_Code_Mapping_Mapping;

    //MARK: - UpdateAreaSimple
    function UpdateAreaSimple(
        uint256[] memory _Country_Group_Code_Data,
        uint32[] memory _Country_Group_Code_Index
    ) public {
        Country_Group_Code_Data = _Country_Group_Code_Data;
        Country_Group_Code_Index = _Country_Group_Code_Index;
        Area_Simple_Version += 1;
    }

    // MARK: - UpdateAreaBaseline
    function UpdateAreaBaseline(
        uint8[] memory _Country_Code_8,
        uint8[][] memory _Country_Group_Code_8
    ) public {
        // Country_Group_baseline = _Country_Group_Code_8;
        for (uint8 i = 0; i < _Country_Code_8.length; i++) {
            // uint8 country = _Country_Code_8[i];
            Country_Group_Code_Mapping_Baseline[
                _Country_Code_8[i]
            ] = _Country_Group_Code_8[i];
            // for (uint8 j = 0; j < _Country_Group_Code_32[i].length; j++) {
            //     uint32 group = _Country_Group_Code_32[i][j];
            //     Country_Group_Code_Mapping_Mapping[country][group] = true;
            // }
        }
    }

    // MARK: - UploadTerms
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
        uint256 Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Area_Group_Simple = Group_Code;
        terms.Area_Country_Simple = Country_Code;
        terms.Area_Simple_Version = Area_Simple_Version;
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
        terms.Area_Group_Simple = Group_Code;
        terms.Area_Country_Simple = Country_Code;
        if (role == role_requester) {
            terms.Area_Country_Simple = country_group_code;
        }
    }

    // MARK: - UploadAreaBaseline
    function UploadAreaBaseline(
        uint8 role,
        address _address,
        uint8[] memory Group_Code,
        uint8[] memory Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == role_provider) {
            // require(msg.sender == dataProvider, "Invalid sender");
            for (uint8 i = 0; i < Country_Code.length; i++) {
                terms.Area_Country_Map_Baseline[Country_Code[i]] = true;
            }
            for (uint8 i = 0; i < Group_Code.length; i++) {
                terms.Area_Group_Map_Baseline[Group_Code[i]] = true;
            }
            // provider_areaMapping[_address].Area_Country_List_Baseline = Country_Code;
            // provider_area_baseline_mapping[_address].Area_Group_Simple = Group_Code;
        }

        if (role == role_requester) {
            terms.Area_Country_List_Baseline = Country_Code;
            terms.Area_Group_List_Baseline = Group_Code;
        }
    }

    function DisplayAreaCode(
        uint8 role,
        address _address
    ) public view returns (uint64, uint8[] memory, uint32[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Area_Group_Simple,
            terms.Area_Country_List_Baseline,
            terms.Area_Country_Group_Code
        );
    }

    // MARK: - UploadDiseaseBinary
    function UploadDiseaseBinary(
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

    // MARK: - UploadDisease
    function UploadDisease(
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

    // MARK: - CheckAreaSimple
    function CheckAreaSimple(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        if (Country_Group_Code_Data.length == 0) {
            revert("checkAreaSimple: Country_Group_Code_Data is empty");
        }
        if (Country_Group_Code_Data.length != Country_Group_Code_Index.length) {
            revert(
                "checkAreaSimple: Country_Group_Code_Data and Country_Group_Code_Index must have the same length"
            );
        }
        Terms storage requester_terms = requesterMapping[_requester_address];
        Terms storage provider_terms = providerMapping[_provider_address];

        uint64 provider_group = provider_terms.Area_Group_Simple;
        uint64 requester_group = requester_terms.Area_Group_Simple;

        uint256 provider_Country = provider_terms.Area_Country_Simple;
        uint256 requester_Country = requester_terms.Area_Country_Simple;

        if (provider_Country & requester_Country != requester_Country) {
            uint256 rest_countries = ~provider_Country & requester_Country;
            uint256 provider_countries_from_group = 0;
            // to obtain the countries from group of provider
            for (uint8 i = 0; i < Country_Group_Code_Data.length; i++) {
                uint256 group = Country_Group_Code_Data[i];
                uint32 index = Country_Group_Code_Index[i];
                // the index belongs to the group of provider
                if (index & provider_group != 0) {
                    provider_countries_from_group |= group;
                }
            }
            uint256 rest_countries_from_group = rest_countries &
                provider_countries_from_group;
            if (rest_countries_from_group != 0) {
                return false;
            }
        }

        if ((requester_group & provider_group) == requester_group) {
            return true;
        }
        return false;
    }

    // MARK: - CheckAreaBaseline
    // tags checkArea
    //   === Initialization ===
    function CheckAreaBaseline(
        address _provider,
        address _requester
    ) public view returns (bool) {
        //check countries, countries of requester must be a subset of countries of provider or the group of countries of requester must be a subset of countries of provider
        Terms storage requester_terms = requesterMapping[_requester];
        Terms storage provider_terms = providerMapping[_provider];
        mapping(uint8 => bool) storage provider_country_code = provider_terms
            .Area_Country_Map_Baseline;
        for (
            uint index_requester = 0;
            index_requester < requester_terms.Area_Country_List_Baseline.length;
            index_requester++
        ) {
            uint8 requester_code = requester_terms.Area_Country_List_Baseline[
                index_requester
            ];

            if (provider_country_code[requester_code] == false) {
                uint8[]
                    memory group_country_code = Country_Group_Code_Mapping_Baseline[
                        requester_code
                    ];
                bool flag = false;
                for (uint8 i = 0; i < group_country_code.length; i++) {
                    uint8 group = group_country_code[i];
                    if (provider_terms.Area_Group_Map_Baseline[group] == true) {
                        // any group of countries of requester is a subset of countries of providder
                        // then permit of this country is permitted
                        flag = true;
                        break;
                    }
                }
                //both countries and its group is denied
                if (flag == false) {
                    return false;
                }
            }
        }

        // check groups, group of requester must be a subset of group of provider or the group of requester is 0
        for (
            uint index_requester = 0;
            index_requester < requester_terms.Area_Group_List_Baseline.length;
            index_requester++
        ) {
            uint8 requester_code = requester_terms.Area_Group_List_Baseline[
                index_requester
            ];
            if (provider_terms.Area_Group_Map_Baseline[requester_code] == false) {
                return false;
            }
        }

        return true;
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
        if (CheckAreaBaseline(_provider_address, _requester_address) == false) {
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
