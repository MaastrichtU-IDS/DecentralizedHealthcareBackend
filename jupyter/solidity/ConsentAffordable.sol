// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;
import "./ConsentBase.sol";

contract ConsentCode is ConsentBase {
 
    //  constructor() {
    //     dataProvider = msg.sender;
    // }
    // MARK: - Terms
    struct Terms {
        // affordable
        uint16 Area_Group_Affordable;
        uint256 Area_Country_Affordable;

        uint32 Disease_Group_Affordable;
        uint128[26] Disease_Category_Affordable;
    }

    

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    // uint8[] Country_Code_8;
    // uint32[] Country_Group_Code_32;
    // mapping(uint8 => uint32) Country_Code_Mapping;
    // mapping(uint8 => uint8[]) Country_Group_Code_Mapping_Baseline;
    // mapping(uint8 => mapping(uint32 => bool)) Country_Group_Code_Mapping_Mapping;


  
    // //MARK - UpdateAreaSimple
    // function UpdateCountryGroupRelation(
    //     uint256[] memory _Group_Countries,
    //     uint16[] memory _Country_Group_Code_Index
    // ) public {
    //     Group_Countries = _Group_Countries;
    //     Group_Index = _Country_Group_Code_Index;
    //     Area_Simple_Version += 1;
    // }

    // // MARK: - DisplayCountryGroupRelation
    // function DisplayCountryGroupRelation()
    //     public
    //     view
    //     returns (uint256[] memory, uint16[] memory, uint16)
    // {
    //     return (Group_Countries,
    //         Group_Index,
    //         Area_Simple_Version
    //     );
    // }


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

 
    // MARK: - DisplayAreaSmarter
    function DisplayArea(
        uint8 role,
        address _address
    ) public view returns (uint16, uint256) {
        Terms storage terms = TermsByRole(role, _address);
        return (terms.Area_Group_Affordable,
            terms.Area_Country_Affordable
            // terms.Area_Simple_Version,    
            // terms.Allow_all_area     
        );
    }

    // MARK: - UploadAreaAffordable
    function UploadArea(
        uint8 role,
        address _address,
        // bool allow_all,
        uint16 Group_Code,
        uint256 Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        // if (allow_all) {
        //     terms.Allow_all_area = true;
        // } else {
            terms.Area_Group_Affordable = Group_Code;
            terms.Area_Country_Affordable = Country_Code;
            // terms.Area_Simple_Version = Area_Simple_Version;
        // }
    }


    function delete_area(
        uint8 role,
        address _address,
        uint8[] memory Group_Code,
        uint8[] memory Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == role_provider) {
            // require(msg.sender == dataProvider, "Invalid sender");
       
            delete terms.Area_Group_Affordable;
            delete terms.Area_Country_Affordable;
            // provider_areaMapping[_address].Area_Country_List_Baseline = Country_Code;
            // provider_area_baseline_mapping[_address].Area_Group_Affordable = Group_Code;
        }

        if (role == role_requester) {
            // require(msg.sender == dataProvider, "Invalid sender");
            delete terms.Area_Group_Affordable;
            delete terms.Area_Country_Affordable;
            // requester_areaMapping[_address].Area_Country_List_Baseline = Country_Code;
            // requester_area_baseline_mapping[_address].Area_Group_Affordable = Group_Code;
        }
    }



    // MARK: - UploadDiseaseAffordable
    function UploadDisease(
        uint8 role,
        address _address,
        // bool allow_all,
        uint32 Disease_Group_Affordable,
        uint128[] memory Disease_Category_Affordable
    ) public {
        Terms storage terms = TermsByRole(role, _address);
        // if (allow_all) {
        //     terms.allow_all_disease = true;
        //     return;
        // }
        // terms.Disease_Group_Affordable = Disease_Group_Affordable;
        //  terms.Disease_Category_Affordable; = Disease_Category_Affordable;;
        for (uint8 i = 0; i < Disease_Category_Affordable.length; i++) {
            terms.Disease_Category_Affordable[i] = Disease_Category_Affordable[i];
        }
    }


    // MARK: UploadDiseaseBaseline
    function delete_disease(
        uint8 role,
        address _address,
        uint16[] memory Disease_Array_Baseline
    ) public {
        Terms storage terms = TermsByRole(role, _address);
         
        if (role == role_provider) {
        
            delete terms.Disease_Category_Affordable;
            delete terms.Disease_Group_Affordable;
        }

        if (role == role_requester) {
            // for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
            //     terms.Disease_Array_Baseline.push(Disease_Array_Baseline[i]);
            // }
   
            delete terms.Disease_Category_Affordable;
            delete terms.Disease_Group_Affordable;
        }
    }


    
    // MARK: - DisplayDiseaseCode
    function DisplayDiseaseCode(
        uint8 role,
        address _address
    ) public view returns (Terms memory) {
        Terms memory terms = TermsByRole(role, _address);
        return terms;
    }

    // function DisplayDiseaseCodeAffordable(
    //     uint8 role,
    //     address _address
    // ) public view returns (uint32, uint128[26] memory, bool) {
    //     Terms storage terms = TermsByRole(role, _address);

    //         return (terms.Disease_Group_Affordable;,terms.Disease_Category_Affordable;,terms.allow_all_disease );
        
    // }


    // MARK: - CheckAreaAffordable(_provider_address, _requester_address);
    function CheckArea(
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
        // if (provider_terms.Allow_all_area == true) {
        //     return true;
        // }
        // if (requester_terms.Allow_all_area == true) {
        //     return false;
        // }

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

    //    if ((requester_group & provider_group) != requester_group) {
    //         // if the group of requester is not a subset of group of provider, return false
    //         return false;
    //     }
        return false;
    }

    // CheckDiseaseAffordable
    function CheckDisease(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        // uint32 requester_group_code = requesterMapping[_requester_address].Disease_Group_Affordable;
        // uint32 provider_group_code = providerMapping[_provider_address].Disease_Group_Affordable;
        // if ((requester_group_code & provider_group_code) != requester_group_code) {
        //     return false;
        // }

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
        return true;
    }


    function access_data(address provider_address, address requester_address) view public returns (uint32) {

        PurposeProvider memory provider = purpose_providers_mapping[provider_address];
        PurposeRequester memory requester = purpose_requesters_mapping[requester_address];
        
        if (provider.Allow_All == true) {
            return 0;
        }
       
        uint32 result = super.AccessData(provider_address, requester_address);
        if (result != 0) {
            return result;
        }
        uint32 u1=1;

        if (provider.GeographicSpecificRestriction) {
            if (!requester.UseBySpecifiedCountries || !CheckArea(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.GeographicSpecificRestriction);
            }
        }

        if (provider.OpenToGeneralResearchAndClinicalCare && provider.OpenToHMBResearch && provider.OpenToDiseaseSpecific) {
            if (!requester.UseForSpecificDiseaseResearch || !CheckDisease(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.OpenToDiseaseSpecific);
            }
        }
        return result;
    }
     

}
