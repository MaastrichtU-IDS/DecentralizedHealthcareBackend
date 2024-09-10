// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentCode {
 
    //  constructor() {
    //     dataProvider = msg.sender;
    // }

    // MARK: - BooleanItems
    // struct BooleanItems {
    //     bool ClinicalProfessionals;
    //     bool AcademicProfessionals;
    //     bool ReferenceOrControlMaterial;
    //     bool MethodsDevelopment;
    //     bool PopulationsResearch;
    //     bool AncestryResearch;
    //     bool FundamentalBioResearch;
    //     bool DrugDevelopmentResearch;
    //     bool AgeCategoriesResearch;
    //     bool GenderCategoriesResearch;
    //     bool ProfitPurpose;
    //     bool ProfitMakingProfessionals;
    //     bool FormalApprovalRequired;
    // }

    // MARK: - Terms
    struct Terms {
        uint32 Purpose;
        uint16 Start_Year;
        uint8 Start_Month;
        uint16 Start_Day;
        uint8 Months;
  
        // affordable
        uint16 Area_Group_Affordable;
        uint256 Area_Country_Affordable;
        bool Allow_all_area;
        uint32 Disease_Group_Affordable;
        uint128[26] Disease_Category_Affordable;
  
        // baseline
        uint8[] Area_Country_List_Baseline;
        uint8[] Area_Group_List_Baseline;
        mapping(uint8 => bool) Area_Country_Map_Baseline;
        mapping(uint8 => bool) Area_Group_Map_Baseline;
        
        mapping(uint16 => bool) Disease_Map_Baseline;
        bool allow_all_disease;
        uint16[] Disease_Array_Baseline;

    }



    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    uint8 constant role_provider = 1;
    uint8 constant role_requester = 2;
    uint256[] Group_Countries;
    uint16[] Group_Index;
    // uint8[][] Country_Group_baseline;

    uint16 Area_Simple_Version = 0;

    // uint8[] Country_Code_8;
    // uint32[] Country_Group_Code_32;
    mapping(uint8 => uint32) Country_Code_Mapping;
    mapping(uint8 => uint8[]) Country_Group_Code_Mapping_Baseline;
    mapping(uint8 => mapping(uint32 => bool)) Country_Group_Code_Mapping_Mapping;

    //MARK - UpdateAreaSimple
    function UpdateCountryGroupRelation(
        uint256[] memory _Group_Countries,
        uint16[] memory _Country_Group_Code_Index
    ) public {
        Group_Countries = _Group_Countries;
        Group_Index = _Country_Group_Code_Index;
        Area_Simple_Version += 1;
    }

    // MARK: - DisplayCountryGroupRelation
    function DisplayCountryGroupRelation()
        public
        view
        returns (uint256[] memory, uint16[] memory, uint16)
    {
        return (Group_Countries,
            Group_Index,
            Area_Simple_Version
        );
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

    // MARK: - UploadSimpleItems
    function UploadSimpleItems(
        uint8 role,
        address _address,
        uint32 Purpose
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Purpose = Purpose;
    }

    // MARK: - DisplaySimpleItems
    function DisplaySimpleItems(
        uint8 role,
        address _address
    ) public view returns (uint32) {
        Terms storage terms = TermsByRole(role, _address);
        return terms.Purpose;
    }

    // MARK: - UploadDate
    function UploadDate(
        uint8 role,
        address _address,
        uint16 Start_Year,
        uint8 Start_Month,
        uint16 Start_Day,
        uint8 Months
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        terms.Start_Year = Start_Year;
        terms.Start_Month = Start_Month;
        terms.Start_Day = Start_Day;
        terms.Months = Months;
    }

    // MARK: - DisplayDate
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
  
    // MARK: - DisplayAreaSmarter
    function DisplayAreaAffordable(
        uint8 role,
        address _address
    ) public view returns (uint16, uint256, bool) {
        Terms storage terms = TermsByRole(role, _address);
        return (
            terms.Area_Group_Affordable,
            terms.Area_Country_Affordable,
            // terms.Area_Simple_Version,
            terms.Allow_all_area
        );
    }

    // MARK: - UploadAreaAffordable
    function UploadAreaAffordable(
        uint8 role,
        address _address,
        bool allow_all,
        uint16 Group_Code,
        uint256 Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        if (allow_all && (role == role_provider)) {
            terms.Allow_all_area = true;
        } else {
            terms.Area_Group_Affordable = Group_Code;
            terms.Area_Country_Affordable = Country_Code;
            // terms.Area_Simple_Version = Area_Simple_Version;
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
            // provider_area_baseline_mapping[_address].Area_Group_Affordable = Group_Code;
        }

        if (role == role_requester) {
            terms.Area_Country_List_Baseline = Country_Code;
            terms.Area_Group_List_Baseline = Group_Code;
        }
    }

    // MARK: - DisplayAreaCode
    // function DisplayAreaCodeAffordable(
    //     uint8 role,
    //     address _address
    // ) public view returns (uint16, uint256) {
    //     Terms storage terms = TermsByRole(role, _address);
    //     return (terms.Area_Group_Affordable,
    //         terms.Area_Country_Affordable,
    //     );
    // }


    // MARK: - UploadDiseaseAffordable
    function UploadDiseaseAffordable(
        uint8 role,
        address _address,
        bool allow_all,
        uint32 Disease_Group_Affordable,
        uint128[] memory Disease_Category_Affordable
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        if (allow_all) {
            terms.allow_all_disease = true;
            return;
        }
        terms.Disease_Group_Affordable = Disease_Group_Affordable;
        //  terms.Disease_Category_Affordable; = Disease_Category_Affordable;;
        for (uint8 i = 0; i < Disease_Category_Affordable.length; i++) {
            terms.Disease_Category_Affordable[i] = Disease_Category_Affordable[i];
        }
    }

    function RefreshState(address _address){
        Terms storage terms = requesterMapping[_address];
        terms.Disease_Array_Baseline = uint16[];
        mapping(address => uint256) storage aMapping;
        terms.Disease_Map_Baseline = aMapping;
        mapping(address => uint256) storage aMapping;
        terms.Area_Country_Map_Baseline =aMapping;
        mapping(address => uint256) storage aMapping;
        terms.Area_Group_Map_Baseline = aMapping;

        terms.Area_Country_List_Baseline = uint8[];
        terms.Area_Group_List_Baseline = uint8[];

        terms.Area_Country_Affordable = 0;
        terms.Area_Group_Affordable = 0;
        terms.Disease_Category_Affordable = uint128[26];
        terms.Disease_Group_Affordable = 0;
    
        Terms storage terms = providerMapping[_address];
        terms.Disease_Array_Baseline = uint16[] ;
        mapping(address => uint256) storage aMapping;
        terms.Disease_Map_Baseline = aMapping;
        mapping(address => uint256) storage aMapping;
        terms.Area_Country_Map_Baseline = aMapping;
        mapping(address => uint256) storage aMapping;
        terms.Area_Group_Map_Baseline = aMapping;

        terms.Area_Country_List_Baseline = uint8[];
        terms.Area_Group_List_Baseline = uint8[];

        terms.Area_Country_Affordable = 0;
        terms.Area_Group_Affordable = 0;
        terms.Disease_Category_Affordable = uint128[26];
        terms.Disease_Group_Affordable = 0;


    }
    // MARK: UploadDiseaseBaseline
    function UploadDiseaseBaseline(
        uint8 role,
        address _address,
        uint16[] memory Disease_Array_Baseline
    ) public {
        Terms storage terms = TermsByRole(role, _address);
         
        if (role == role_provider) {
            for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
                terms.Disease_Map_Baseline[Disease_Array_Baseline[i]] = true;
            }
        }

        if (role == role_requester) {
            // for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
            //     terms.Disease_Array_Baseline.push(Disease_Array_Baseline[i]);
            // }
            terms.Disease_Array_Baseline = Disease_Array_Baseline;
        }
    }

    // MARK: - DisplayDiseaseCode
    function DisplayDiseaseCode(
        uint8 role,
        address _address
    ) public view returns (uint16[] memory) {
        Terms storage terms = TermsByRole(role, _address);
        return terms.Disease_Array_Baseline;
    }

    // function DisplayDiseaseCodeAffordable(
    //     uint8 role,
    //     address _address
    // ) public view returns (uint32, uint128[26] memory, bool) {
    //     Terms storage terms = TermsByRole(role, _address);

    //         return (terms.Disease_Group_Affordable;,terms.Disease_Category_Affordable;,terms.allow_all_disease );
        
    // }


    // MARK: - CheckPurpose
    function CheckPurpose(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        uint32 providerData = providerMapping[_provider_address].Purpose;
        uint32 requesterData = requesterMapping[_requester_address]
            .Purpose;
        if ((requesterData & providerData) == requesterData) {
            return true;
        }
        return false;
    }

    // MARK: - CheckAreaAffordable(_provider_address, _requester_address);
    function CheckAreaAffordable(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        if (Group_Countries.length == 0) {
            revert("CheckAreaAffordable: Group_Countries is empty");
        }
        if (Group_Countries.length != Group_Index.length) {
            revert(
                "CheckAreaAffordable: Group_Countries and Group_Index must have the same length"
            );
        }
        Terms storage requester_terms = requesterMapping[_requester_address];
        Terms storage provider_terms = providerMapping[_provider_address];
        if (provider_terms.Allow_all_area == true) {
            return true;
        }
        if (requester_terms.Allow_all_area == true) {
            return false;
        }

        uint64 provider_group = provider_terms.Area_Group_Affordable;
        uint64 requester_group = requester_terms.Area_Group_Affordable;

        uint256 provider_country = provider_terms.Area_Country_Affordable;
        uint256 requester_country = requester_terms.Area_Country_Affordable;

        if ((requester_group & provider_group) != requester_group) {
            // if the group of requester is not a subset of group of provider, return false
            return false;
        }
        for (uint8 i = 0; i < Group_Countries.length; i++) {
            uint256 countries = Group_Countries[i];
            uint16 index = Group_Index[i];
            // the index belongs to the group of provider
            if (index & provider_group != 0) {
                provider_country |= countries;
            }
        }
        // if the group of requester is a subset of group of provider, check the countries
       if ((requester_country & provider_country) == requester_country) {
            return true;
        }
        return false;
    }

    // MARK: - CheckAreaBaseline
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
            if (
                provider_terms.Area_Group_Map_Baseline[requester_code] == false
            ) {
                return false;
            }
        }

        return true;
    }

    // MARK: - CheckDisease
    function CheckDiseaseBaseline(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester_address].Disease_Array_Baseline.length;
            index_requester++
        ) {
            uint16 requester_code = requesterMapping[_requester_address]
                .Disease_Array_Baseline[index_requester];
            if (
                providerMapping[_provider_address].Disease_Map_Baseline[
                    requester_code
                ] == false
            ) {
                return false;
            }
        }
        return true;
    }

    // CheckDiseaseAffordable
    function CheckDiseaseAffordable(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        if (providerMapping[_provider_address].allow_all_disease == true) {
            return true;
        }

        if (requesterMapping[_requester_address].allow_all_disease == true) {
            return false;
        }

        uint32 requester_group_code = requesterMapping[_requester_address].Disease_Group_Affordable;
        uint32 provider_group_code = providerMapping[_provider_address].Disease_Group_Affordable;
        if ((requester_group_code & provider_group_code) != requester_group_code) {
            return false;
        }

        bool allowed = false;
        for (
            uint index_requester = 0;
            index_requester <
            requesterMapping[_requester_address].Disease_Category_Affordable.length;
            index_requester++
        ) {
            // uint8 requester_group_code = requesterMapping[_requester_address]
            //     .Disease_Group_Affordable;[index_requester];
            uint128 requester_category_code = requesterMapping[
                _requester_address].Disease_Category_Affordable[index_requester];
            allowed = false;
            for (
                uint index_provider = 0;
                index_provider <
                providerMapping[_provider_address].Disease_Category_Affordable.length;
                index_provider++
            ) {
                // uint8 provider_group_code = providerMapping[_provider_address].Disease_Group_Affordable;[index_requester];
                uint128 provider_category_code = providerMapping[_provider_address].Disease_Category_Affordable[index_provider];
                if (provider_category_code & requester_category_code == requester_category_code) {
                    allowed = true;
                    break;
                }
            }

            if (allowed == false) {
                return false;
            }
        }
        //     uint128 provider_category_code = providerMapping[_provider_address]
        //         .Disease_Map_Affordable[requester_group_code];
                
        //     if (
        //         !(provider_category_code & requester_category_code ==
        //             requester_category_code)
        //     ) {
        //         return false;
        //     }
        // }
        return true;
    }

    // MARK: - CheckDate
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

        //  year, month, day now equal
        return true;
    }

    // MARK: - AccessData
    function AccessData(
        address _provider_address,
        address _requester_address
    ) public view returns (uint8) {
        uint8 result = 0;
        if (CheckAreaAffordable(_provider_address, _requester_address) == false) {
            result += 1;
        }

        if (
            CheckDiseaseAffordable(_provider_address, _requester_address) ==
            false
        ) {
            result += 2;
        }

        if (CheckDate(_provider_address, _requester_address) == false) {
            result += 4;
        }

        if (CheckPurpose(_provider_address, _requester_address) == false) {
            result += 8;
        }
        return result;
    }
}
