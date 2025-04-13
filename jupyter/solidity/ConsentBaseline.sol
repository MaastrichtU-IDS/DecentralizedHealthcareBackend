// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentCode {
 
    //  constructor() {
    //     dataProvider = msg.sender;
    // }

   
    // MARK: - Terms
    struct Terms {
        uint32 Purpose;
        uint16 Start_Year;
        uint8 Start_Month;
        uint16 Start_Day;
        uint8 Months;
  
  
        // baseline
        uint8[] Area_Country_List_Baseline;
        uint8[] Area_Group_List_Baseline;
        mapping(uint8 => bool) Area_Country_Map_Baseline;
        mapping(uint8 => bool) Area_Group_Map_Baseline;
        
        mapping(uint16 => bool) Disease_Map_Baseline;
        // bool allow_all_disease;
        uint16[] Disease_Array_Baseline;

    }

    enum RESULT_CODE {
        // Success,
        FirstCategory,
        OpenToGeneralResearchAndClinicalCare,
        OpenToHMBResearch,
        OpenToPopulationAndAncestryResearch,
        OpenToDiseaseSpecific,
        OpenToGeneticStudiesOnly,
        ResearchSpecificRestrictions,
        OpenToResearchUseOnly,
        GeneralMethodResearch,
        GeographicSpecificRestriction,
        OpenToNonProfitUseOnly,
        PublicationRequired,
        CollaborationRequired,
        EthicsApprovalrequired,
        TimeLimitOnUse,
        CostOnUse,
        DataSecurityMeasuresRequired
        // DiseaseSpecificResearch
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



    struct PurposeProvider {
        bool Allow_All;
        bool OpenToGeneralResearchAndClinicalCare;
        bool OpenToHMBResearch;
        bool OpenToPopulationAndAncestryResearch;
        bool OpenToDiseaseSpecific;
        bool OpenToGeneticStudiesOnly;
        bool ResearchSpecificRestrictions;
        bool OpenToResearchUseOnly;
        bool GeneralMethodResearch;
        bool GeographicSpecificRestriction;
        bool OpenToNonProfitUseOnly;
        bool PublicationRequired;
        bool CollaborationRequired;
        bool EthicsApprovalrequired;
        bool TimeLimitOnUse;
        bool CostOnUse;
        bool DataSecurityMeasuresRequired;
        // bool DiseaseSpecificResearch;
    }

    struct PurposeRequester {
        bool UseForMethodsDevelopment;
        bool UseForReferenceOrControlMaterial;
        bool UseForPopulationsResearch;
        bool UseForAncestryResearch;
        bool UseForHMBResearch;
        bool UseForFundamentalBioResearch;
        bool UseForGeneticsResearch;
        bool UseForDrugDevelopmentResearch;
        bool UseForSpecificDiseaseResearch;
        bool UseForAgeCategoriesResearch;
        bool UseForGenderCategoriesResearch;
        bool UseForDecisionSupport;
        bool UseForDiseaseSupport;
        bool UseByAcademicProfessionals;
        bool UseByClinicalProfessionals;
        bool UseByProfitMakingProfessionals;
        bool UseByNonProfessionals;
        bool UseBySpecifiedCountries;
        bool UseForProfitPurpose;
        bool UseForNonProfitPurpose;
        bool TimelineRestrictions;
        bool FormalApprovalRequired;
        bool CollaborationRequired;
        bool PublicationRequired;
        bool DataSecurityMeasures;
        bool DataDestructionRequired;
        bool LinkingOfAccessedRecords;
        bool RecontactingDataSubjects;
        bool IntellectualPropertyClaims;
        bool UseOfAccessedResources;
        bool FeesForAccess;
    }

    mapping(address => PurposeProvider) purpose_providers_mapping;
    mapping(address => PurposeRequester) purpose_requesters_mapping;

     function uploadPurposeProvider(
        address _address1,
        PurposeProvider memory purpose
    ) public {
        purpose_providers_mapping[_address1] = purpose;
        // DataSubjectAcc.push(_address1);
    }

    function uploadPurposeRequester(
        address _address2,
        PurposeRequester memory purpose
    ) public {
        purpose_requesters_mapping[_address2] = purpose;
        // DataRequesterAcc.push(_address2);
    }

    function GetPurposeItemsProvider(address _address) view public returns (PurposeProvider memory) {
              return purpose_providers_mapping[_address];
    }

    function GetPurposeItemsRequester(address _address) view public returns (PurposeRequester memory) {
        return purpose_requesters_mapping[_address];
    }
  
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
    function UpdateArea(
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
  

    // MARK: - UploadAreaBaseline
    function UploadArea(
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

    function delete_area(
        uint8 role,
        address _address,
        uint8[] memory Group_Code,
        uint8[] memory Country_Code
    ) public {
        Terms storage terms = TermsByRole(role, _address);

        if (role == role_provider) {
            // require(msg.sender == dataProvider, "Invalid sender");
            for (uint8 i = 0; i < Country_Code.length; i++) {
                delete terms.Area_Country_Map_Baseline[Country_Code[i]];
            }
            for (uint8 i = 0; i < Group_Code.length; i++) {
                delete terms.Area_Group_Map_Baseline[Group_Code[i]];
            }
            delete terms.Area_Group_Affordable;
            delete terms.Area_Country_Affordable;
            // provider_areaMapping[_address].Area_Country_List_Baseline = Country_Code;
            // provider_area_baseline_mapping[_address].Area_Group_Affordable = Group_Code;
        }

        if (role == role_requester) {
            delete terms.Area_Country_List_Baseline ;
            delete terms.Area_Group_List_Baseline ;
            
            delete terms.Area_Group_Affordable;
            delete terms.Area_Country_Affordable;
        }
    }

    // MARK: UploadDiseaseBaseline
    function UploadDisease(
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

    
    // MARK: UploadDiseaseBaseline
    function delete_disease(
        uint8 role,
        address _address,
        uint16[] memory Disease_Array_Baseline
    ) public {
        Terms storage terms = TermsByRole(role, _address);
         
        if (role == role_provider) {
            for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
               delete terms.Disease_Map_Baseline[Disease_Array_Baseline[i]];
            }
            delete terms.Disease_Category_Affordable;
            delete terms.Disease_Group_Affordable;
        }

        if (role == role_requester) {
            // for (uint16 i = 0; i < Disease_Array_Baseline.length; i++) {
            //     terms.Disease_Array_Baseline.push(Disease_Array_Baseline[i]);
            // }
            delete terms.Disease_Array_Baseline;
            delete terms.Disease_Category_Affordable;
            delete terms.Disease_Group_Affordable;
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

    // MARK: - CheckAreaBaseline
    function CheckArea(
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
    function CheckDisease(
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

    function AccessData(address provider_address, address requester_address) view public returns (uint32) {

        PurposeProvider memory provider = purpose_providers_mapping[provider_address];
        PurposeRequester memory requester = purpose_requesters_mapping[requester_address];
        
        if (provider.Allow_All == true) {
            return 0;
        }
       
        uint32 result = 0;
        uint32 u1=1;

        bool generalResearchAndClinicalCare = (provider.OpenToGeneralResearchAndClinicalCare == true && 
            (requester.UseForMethodsDevelopment== true || 
            requester.UseForReferenceOrControlMaterial == true || 
            requester.UseForHMBResearch == false ||
            requester.UseForPopulationsResearch == true ||
            requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);

        bool hmbResearch =  (provider.OpenToHMBResearch == true && 
            (requester.UseForFundamentalBioResearch == true || 
            requester.UseForGeneticsResearch == true || 
            requester.UseForDrugDevelopmentResearch == true || 
            requester.UseForSpecificDiseaseResearch == true || 
            requester.UseForAgeCategoriesResearch == true || 
           requester.UseForGenderCategoriesResearch == true) ||requester.UseByClinicalProfessionals==true);

        bool populationAndAncestryResearch = (provider.OpenToPopulationAndAncestryResearch == true &&
            (requester.UseForPopulationsResearch == true || 
            requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);

        if (!(generalResearchAndClinicalCare || hmbResearch || populationAndAncestryResearch)) {
            return  result += u1 << uint32(RESULT_CODE.FirstCategory);
        }

        if (provider.GeographicSpecificRestriction) {
            if (!requester.UseBySpecifiedCountries || !CheckArea(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.GeographicSpecificRestriction);
            }
        }

        if (provider.OpenToDiseaseSpecific) {
            if (!requester.UseForSpecificDiseaseResearch || !CheckDisease(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.OpenToDiseaseSpecific);
            }
        }

        if (provider.TimeLimitOnUse) {
            if (!requester.TimelineRestrictions || !CheckDate(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.TimeLimitOnUse);
            }
        }

        bool researchSpecificRestrictions =((provider.ResearchSpecificRestrictions == true && requester.UseForReferenceOrControlMaterial== false) || provider.ResearchSpecificRestrictions == false);
        if (!researchSpecificRestrictions) {
            result += u1 << uint32(RESULT_CODE.ResearchSpecificRestrictions);
        }

        bool openToResearchUseOnly = (provider.OpenToResearchUseOnly == true && requester.UseForHMBResearch == false) ||
            provider.OpenToResearchUseOnly == false;

        if (!openToResearchUseOnly) {
            result += u1 << uint32(RESULT_CODE.OpenToResearchUseOnly);
        }

        bool openToGeneticStudiesOnly = ((provider.OpenToGeneticStudiesOnly==true && requester.UseForGeneticsResearch == true) || provider.OpenToGeneticStudiesOnly==false);
        if (openToGeneticStudiesOnly == false) {
            result += u1 << uint32(RESULT_CODE.OpenToGeneticStudiesOnly);
        }

        // bool generalMethodResearch = provider.GeneralMethodResearch ? true : requester.UseForMethodsDevelopment == false;

        bool generalMethodResearch =  (provider.GeneralMethodResearch==false && requester.UseForMethodsDevelopment == false) || provider.GeneralMethodResearch==true;

        if (!generalMethodResearch) {
            result += u1 << uint32(RESULT_CODE.GeneralMethodResearch);
        }

        bool openToNonProfitUseOnly = (provider.OpenToNonProfitUseOnly == true && (requester.UseForNonProfitPurpose == true && requester.UseForProfitPurpose == false &&
           requester.UseByProfitMakingProfessionals == false)) || 
            provider.OpenToNonProfitUseOnly == false;


        if (!openToNonProfitUseOnly) {
            result += u1 << uint32(RESULT_CODE.OpenToNonProfitUseOnly);
        }

        // bool publicationRequired = provider.PublicationRequired ? requester.PublicationRequired : true;

        bool publicationRequired =  (provider.PublicationRequired == true && requester.PublicationRequired == true) ||
            provider.PublicationRequired == false;


        if (!publicationRequired) {
            result += u1 << uint32(RESULT_CODE.PublicationRequired);
        }

        bool collaborationRequired = provider.CollaborationRequired ? requester.CollaborationRequired : true;
        if (!collaborationRequired) {
            result += u1 << uint32(RESULT_CODE.CollaborationRequired);
        }

        // bool ethicsApprovalrequired = 
        if (!(provider.EthicsApprovalrequired ? requester.FormalApprovalRequired : true)) {
            result += u1 << uint32(RESULT_CODE.EthicsApprovalrequired);
        }

       bool dataSecurityMeasuresRequired =   (provider.DataSecurityMeasuresRequired == true && requester.DataSecurityMeasures == true  && requester.DataDestructionRequired == true && requester.LinkingOfAccessedRecords == true && requester.RecontactingDataSubjects == true && requester.IntellectualPropertyClaims == true && requester.UseOfAccessedResources == true) ||provider.DataSecurityMeasuresRequired == false;
        if (!dataSecurityMeasuresRequired) {
            result += u1 << uint8(RESULT_CODE.DataSecurityMeasuresRequired);
        }

        // bool costOnUse = 
        if (!((provider.CostOnUse == true && requester.FeesForAccess ==  true) ||provider.CostOnUse == false) ) {
            result += u1 << uint8(RESULT_CODE.CostOnUse);
        }

        // if (result == 0) {
        //     result |= 1 << uint32(RESULT_CODE.Success);
        // }

        return result;
    }
       
}
