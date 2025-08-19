// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;
import "./DUOConsentBase.sol";

contract ConsentCode is ConsentBase {
    //  constructor() {
    //     dataProvider = msg.sender;
    // }

    // MARK: - Terms
    struct Terms {
        // baseline
        uint8[] Area_Country_List_Baseline;
        uint8[] Area_Group_List_Baseline;
        mapping(uint8 => bool) Area_Country_Map_Baseline;
        mapping(uint8 => bool) Area_Group_Map_Baseline;
        mapping(uint16 => bool) Disease_Map_Baseline;
        // bool allow_all_disease;
        uint16[] Disease_Array_Baseline;
    }

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    mapping(uint8 => uint8[]) Country_Group_Code_Mapping_Baseline;

    // MARK: - UploadTerms
    function TermsByRole(
        uint8 role,
        address _address
    ) private view returns (Terms storage) {
        if (role == ROLE_PROVIDER) {
            // require(msg.sender == dataProvider, "TermsByRole: Invalid sender");
            return providerMapping[_address];
        } else if (role == ROLE_REQUESTER) {
            return requesterMapping[_address];
        } else {
            revert("TermsByRole: Invalid role specified");
        }
    }

    function UpdateCountryGroupRelation(
        uint8[] memory Group_Code,
        uint8[][] memory Country_Code
    ) public {
        // Country_Group_baseline = _Country_Group_Code_8;
        for (uint8 i = 0; i < Group_Code.length; i++) {
            // uint8 country = _Country_Code_8[i];
            Country_Group_Code_Mapping_Baseline[Group_Code[i]] = Country_Code[
                i
            ];
            // for (uint8 j = 0; j < _Country_Group_Code_32[i].length; j++) {
            //     uint32 group = _Country_Group_Code_32[i][j];
            //     Country_Group_Code_Mapping_Mapping[country][group] = true;
            // }
        }
    }

    // MARK: - UploadAreaBaseline
    function UploadArea(
        uint8 role,
        address _address,
        uint8[] memory Group_Code,
        uint8[] memory Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == ROLE_PROVIDER) {
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

        if (role == ROLE_REQUESTER) {
            terms.Area_Country_List_Baseline = Country_Code;
            terms.Area_Group_List_Baseline = Group_Code;
        }
    }

    function delete_area(
        uint8 role,
        address _address,
        uint8[] memory Group_Code,
        uint8[] memory Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == ROLE_PROVIDER) {
            // require(msg.sender == dataProvider, "Invalid sender");
            for (uint8 i = 0; i < Country_Code.length; i++) {
                delete terms.Area_Country_Map_Baseline[Country_Code[i]];
            }
            for (uint8 i = 0; i < Group_Code.length; i++) {
                delete terms.Area_Group_Map_Baseline[Group_Code[i]];
            }

            // provider_areaMapping[_address].Area_Country_List_Baseline = Country_Code;
            // provider_area_baseline_mapping[_address].Area_Group_Affordable = Group_Code;
        }

        if (role == ROLE_REQUESTER) {
            delete terms.Area_Country_List_Baseline;
            delete terms.Area_Group_List_Baseline;
        }
    }

    // MARK: UploadDiseaseBaseline
    function UploadDisease(
        uint8 role,
        address _address,
        uint16[] memory Disease_Array_Baseline
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == ROLE_PROVIDER) {
            for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
                terms.Disease_Map_Baseline[Disease_Array_Baseline[i]] = true;
            }
        }

        if (role == ROLE_REQUESTER) {
            // for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
            //     terms.Disease_Array_Baseline.push(Disease_Array_Baseline[i]);
            // }
            terms.Disease_Array_Baseline = Disease_Array_Baseline;
        }
    }

    // MARK: UploadDiseaseBaseline
    function delete_disease(
        uint8 role,
        address _address,
        uint16[] memory Disease_Array_Baseline
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == ROLE_PROVIDER) {
            for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
                delete terms.Disease_Map_Baseline[Disease_Array_Baseline[i]];
            }
        }

        if (role == ROLE_REQUESTER) {
            // for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
            //     terms.Disease_Array_Baseline.push(Disease_Array_Baseline[i]);
            // }
            delete terms.Disease_Array_Baseline;
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

    // MARK: - CheckAreaBaseline
    function CheckArea(
        address _provider,
        address _requester
    ) public view override returns (bool) {
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
    function CheckDisease(
        address _provider_address,
        address _requester_address
    ) public view override returns (bool) {
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

    // function access_data1(address provider_address, address requester_address) view public returns (uint32) {

    //     PurposeProvider memory provider = purpose_providers_mapping[provider_address];
    //     PurposeRequester memory requester = purpose_requesters_mapping[requester_address];

    //      if (provider.Allow_All == true) {
    //         return 0;
    //     }

    //     uint32 result = super.AccessData(provider_address, requester_address);
    //     if (result != 0) {
    //         return result;
    //     }
    //     uint32 u1=1;

    //     if (provider.GeographicSpecificRestriction) {
    //         if (!requester.UseBySpecifiedCountries || !CheckArea(provider_address, requester_address)) {
    //             result += u1 << uint32(RESULT_CODE.GeographicSpecificRestriction);
    //         }
    //     }

    //     if (provider.OpenToGeneralResearchAndClinicalCare && provider.OpenToHMBResearch && provider.OpenToDiseaseSpecific) {
    //         if (!requester.UseForSpecificDiseaseResearch || !CheckDisease(provider_address, requester_address)) {
    //             result += u1 << uint32(RESULT_CODE.OpenToDiseaseSpecific);
    //         }
    //     }
    //     return result;
    // }
}
