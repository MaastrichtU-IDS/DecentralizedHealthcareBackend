// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentCode {

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
        // bool Allow_all_area;
        uint32 Disease_Group_Affordable;
        uint128[26] Disease_Category_Affordable;
  
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
    }


    

    mapping(address => Terms) providerMapping; // data subject
    mapping(address => Terms) requesterMapping; // data subject

    uint8 constant role_provider = 1;
    uint8 constant role_requester = 2;

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
            if (!requester.UseBySpecifiedCountries || !CheckAreaAffordable(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.GeographicSpecificRestriction);
            }
        }

        if (provider.OpenToDiseaseSpecific) {
            if (!requester.UseForSpecificDiseaseResearch || !CheckDiseaseAffordable(provider_address, requester_address)) {
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
        return result;
    }

}
