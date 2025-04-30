// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8;

contract ConsentBase {
 
    //  constructor() {
    //     dataProvider = msg.sender;
    // }
    // MARK: - Terms
    struct Date {
     
        uint16 Start_Year;
        uint8 Start_Month;
        uint16 Start_Day;
        uint8 Months;

    }

    enum RESULT_CODE {
        // Success,
        FirstCategory,
        GeneralResearch,
        ClinicalCare,
        HMBResearch,
        PopulationAndAncestryResearchOnly,
        PopulationAndAncestryResearchNon,
        DiseaseSpecific,
        GeneticStudiesOnly,
        ResearchSpecificRestriction,
        ResearchUseOnly,
        GeneralMethodResearchNon,
        GeographicSpecific,
        NonProfitUseOnly,
        NonCommercialUseOnly,
        PublicationRequired,
        PublicationMoratorium,
        CollaborationRequired,
        EthicsApprovalrequired,
        TimeLimitOnUse,
        // CostOnUse,
        DataSecurityMeasuresRequired
        // DiseaseSpecificResearch
    }


    

    mapping(address => Date) providerDateMapping; // data subject
    mapping(address => Date) requesterDateMapping; // data subject

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
        bool NoRestriction;
        bool GeneralResearch;
        bool ClinicalCare;
        bool HMBResearch;
        bool PopulationAndAncestryResearchOnly;
        bool PopulationAndAncestryResearchNon;
        bool DiseaseSpecific;
        bool GeneticStudiesOnly;
     
        // bool ResearchUseOnly;
        bool GeneralMethodResearchNon;
        bool GeographicSpecific;
        bool NonProfitUseOnly;
        bool NonCommercialUseOnly;
        bool PublicationRequired;
        bool PublicationMoratorium;
        bool CollaborationRequired;
        bool EthicsApprovalrequired;
        bool TimeLimitOnUse;
        bool ProfitOrganisationNon;
        // bool CostOnUse;
        bool DataSecurityMeasuresRequired;
        bool ReturnToResource;

        bool UserSpecificRestriction;
        bool ProjectSpecificRestriction;
        bool InstitutionSpecificRestriction;
        bool ResearchSpecificRestriction;
        bool DataUsePermission;
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
        bool SpecificDiseaseResearch;
        bool UseForAgeCategoriesResearch;
        bool UseForGenderCategoriesResearch;
        bool UseForDecisionSupport;
        bool UseForDiseaseSupport;
        bool UseByAcademicProfessionals;
        bool UseByClinicalProfessionals;
        bool UseByProfitMakingProfessionals;
        bool UseByNonProfessionals;
        bool SpecifiedCountries;
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


    // MARK: - UploadTerms
    function DateByRole(
        uint8 role,
        address _address
    ) private view returns (Date storage) {
        if (role == role_provider) {
            // require(msg.sender == dataProvider, "TermsByRole: Invalid sender");
            return providerDateMapping[_address];
        } else if (role == role_requester) {
            return requesterDateMapping[_address];
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
        Date storage terms = DateByRole(role, _address);
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
        Date storage terms = DateByRole(role, _address);
        return (
            terms.Start_Year,
            terms.Start_Month,
            terms.Start_Day,
            terms.Months
        );
    }
  
    // MARK: - CheckDate
    function CheckDate(
        address _provider_address,
        address _requester_address
    ) public view returns (bool) {
        if (
            requesterDateMapping[_requester_address].Start_Year >
            providerDateMapping[_provider_address].Start_Year
        ) {
            return true;
        }
        if (
            requesterDateMapping[_requester_address].Start_Year <
            providerDateMapping[_provider_address].Start_Year
        ) {
            return false;
        }

        // year now equal
        if (
            requesterDateMapping[_requester_address].Start_Month >
            providerDateMapping[_provider_address].Start_Month
        ) {
            return true;
        }
        if (
            requesterDateMapping[_requester_address].Start_Month <
            providerDateMapping[_provider_address].Start_Month
        ) {
            return false;
        }

        // month now equal
        if (
            requesterDateMapping[_requester_address].Start_Day >=
            providerDateMapping[_provider_address].Start_Day
        ) {
            return true;
        }
        if (
            requesterDateMapping[_requester_address].Start_Day <
            providerDateMapping[_provider_address].Start_Day
        ) {
            return false;
        }

        //  year, month, day now equal
        return true;
    }

    
    function CheckDisease(
        address _provider_address,
        address _requester_address
    ) public view virtual returns (bool) {
        revert("CheckDisease: Not implemented");
    }

    function CheckArea(
        address _provider_address,
        address _requester_address
    ) public view virtual returns (bool) {
        revert("CheckArea: Not implemented");
    }

    function Access_Research(
        address _provider_address,
        address _requester_address
    ) public view returns (uint32) {
        PurposeProvider memory provider = purpose_providers_mapping[
            _provider_address
        ];
        PurposeRequester memory requester = purpose_requesters_mapping[
            _requester_address
        ];

        uint32 result = 0;
        uint32 u1=1;

        bool generalResearch = (provider.GeneralResearch == true && 
        (requester.UseForHMBResearch == false ||
        requester.UseForPopulationsResearch == true ||
        requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);
        


        return 0;
    }

    function AccessData(address provider_address, address requester_address) view private  returns (uint32) {

        PurposeProvider memory provider = purpose_providers_mapping[provider_address];
        PurposeRequester memory requester = purpose_requesters_mapping[requester_address];
        
        if (provider.NoRestriction == true) {
            return 0;
        }
       
        uint32 result = 0;
        uint32 u1=1;

        bool generalResearch = (provider.GeneralResearch == true && 
        (requester.UseForHMBResearch == false ||
        requester.UseForPopulationsResearch == true ||
        requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);

        bool clinicalCare = (provider.ClinicalCare == true && 
            (requester.UseForMethodsDevelopment== true || 
            requester.UseForReferenceOrControlMaterial == true));

        bool hmbResearch =  (provider.HMBResearch == true && 
            (requester.UseForFundamentalBioResearch == true || 
            requester.UseForGeneticsResearch == true || 
            requester.UseForDrugDevelopmentResearch == true || 
            requester.SpecificDiseaseResearch == true || 
            requester.UseForAgeCategoriesResearch == true || 
           requester.UseForGenderCategoriesResearch == true) ||requester.UseByClinicalProfessionals==true);

        bool populationAndAncestryResearch = (provider.PopulationAndAncestryResearchOnly == true &&
            (requester.UseForPopulationsResearch == true || 
            requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);

        if (!(generalResearch || clinicalCare || hmbResearch || populationAndAncestryResearch)) {
            return  result += u1 << uint32(RESULT_CODE.FirstCategory);
        }

        bool tmp_result;
        
        
        if (!(provider.PopulationAndAncestryResearchNon == true &&
            (requester.UseForPopulationsResearch == false && 
            requester.UseForAncestryResearch == false) || requester.UseByAcademicProfessionals==false)) {
            result += u1 << uint32(RESULT_CODE.PopulationAndAncestryResearchNon);
        }

           if (!(provider.PopulationAndAncestryResearchOnly == true &&
            (requester.UseForPopulationsResearch == true || 
            requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true)) {
            result += u1 << uint32(RESULT_CODE.PopulationAndAncestryResearchOnly);
        }
        
        if (!((provider.ResearchSpecificRestriction == true && requester.UseForReferenceOrControlMaterial== false) || provider.ResearchSpecificRestriction == false)) {
            result += u1 << uint32(RESULT_CODE.ResearchSpecificRestriction);
        }

   

        // if (!((provider.OpenToResearchUseOnly == true && requester.UseForHMBResearch == false) ||
        //     provider.OpenToResearchUseOnly == false)) {
        //     result += u1 << uint32(RESULT_CODE.OpenToResearchUseOnly);
        // }

        tmp_result = ((provider.GeneticStudiesOnly==true && requester.UseForGeneticsResearch == true) || provider.GeneticStudiesOnly==false);
        if (tmp_result == false) {
            result += u1 << uint32(RESULT_CODE.GeneticStudiesOnly);
        }

        // bool generalMethodResearch = provider.GeneralMethodResearch ? true : requester.UseForMethodsDevelopment == false;

        tmp_result =  (provider.GeneralMethodResearchNon==true && requester.UseForMethodsDevelopment == false) || provider.GeneralMethodResearchNon==false;

        if (!tmp_result) {
            result += u1 << uint32(RESULT_CODE.GeneralMethodResearchNon);
        }

        tmp_result = (provider.NonProfitUseOnly == true && (requester.UseForNonProfitPurpose == true && requester.UseForProfitPurpose == false)) || 
            provider.NonProfitUseOnly == false;
        if (!tmp_result) {
                    result += u1 << uint32(RESULT_CODE.NonProfitUseOnly);
                }
                
        tmp_result = (provider.NonCommercialUseOnly == true && (requester.UseByProfitMakingProfessionals == false)) || 
            provider.NonCommercialUseOnly == false;
        if (!tmp_result) {
                    result += u1 << uint32(RESULT_CODE.NonCommercialUseOnly);
                }

       

        // bool publicationRequired = provider.PublicationRequired ? requester.PublicationRequired : true;

     


        if (!((provider.PublicationRequired == true && requester.PublicationRequired == true) ||
            provider.PublicationRequired == false)) {
            result += u1 << uint32(RESULT_CODE.PublicationRequired);
        }

         if (!((provider.PublicationMoratorium == true && requester.PublicationRequired == false) ||
            provider.PublicationMoratorium == false)) {
            result += u1 << uint32(RESULT_CODE.PublicationMoratorium);
        }

        // tmp_result = provider.CollaborationRequired ? requester.CollaborationRequired : true;
        if (!( (provider.CollaborationRequired == true && requester.CollaborationRequired == true) ||  provider.CollaborationRequired == false)) {
            result += u1 << uint32(RESULT_CODE.CollaborationRequired);
        }

    

        // bool ethicsApprovalrequired = 
        if (!((provider.EthicsApprovalrequired  == true && requester.FormalApprovalRequired == true) ||  provider.EthicsApprovalrequired  == false)) {
            result += u1 << uint32(RESULT_CODE.EthicsApprovalrequired);
        }

       bool dataSecurityMeasuresRequired =   (provider.DataSecurityMeasuresRequired == true && requester.DataSecurityMeasures == true  && requester.DataDestructionRequired == true && requester.LinkingOfAccessedRecords == true && requester.RecontactingDataSubjects == true && requester.IntellectualPropertyClaims == true && requester.UseOfAccessedResources == true) ||provider.DataSecurityMeasuresRequired == false;

        if (!dataSecurityMeasuresRequired) {
            result += u1 << uint8(RESULT_CODE.DataSecurityMeasuresRequired);
        }

     
        // if (!((provider.CostOnUse == true && requester.FeesForAccess ==  true) ||provider.CostOnUse == false) ) {
        //     result += u1 << uint8(RESULT_CODE.CostOnUse);
        // }


        return result;
    }


    
    function access_data(address provider_address, address requester_address) view public returns (uint32) {

        PurposeProvider memory provider = purpose_providers_mapping[provider_address];
        PurposeRequester memory requester = purpose_requesters_mapping[requester_address];
        
        if (provider.NoRestriction == true) {
            return 0;
        }
       
        uint32 result = AccessData(provider_address, requester_address);
        if (result != 0) {
            return result;
        }
        uint32 u1=1;

        if (provider.GeographicSpecific) {
            if (!requester.SpecifiedCountries || !CheckArea(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.GeographicSpecific);
            }
        }

        if (provider.DiseaseSpecific) {
            if (!requester.SpecificDiseaseResearch || !CheckDisease(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.DiseaseSpecific);
            }
        }

        if (provider.TimeLimitOnUse) {
            if (!requester.TimelineRestrictions || !CheckDate(provider_address, requester_address)) {
                result += u1 << uint32(RESULT_CODE.TimeLimitOnUse);
            }
        }
        return result;
    }

     

}
