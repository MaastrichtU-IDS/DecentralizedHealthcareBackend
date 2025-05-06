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
        FirstCategory,
        GeneralResearch,
        ClinicalCare,
        HMBResearch,
        PopulationAndAncestryResearchOnly,
        PopulationAndAncestryResearchNon,
        DiseaseSpecific,
        GeneticStudiesOnly,
        NonGeneralMethodResearch,
        GeographicSpecific,
        NonProfitUseOnly,
        NonCommercialUseOnly,
        PublicationRequired,
        PublicationMoratorium,
        CollaborationRequired,
        EthicsApprovalRequired,
        TimeLimitOnUse,
        ReturnToResource,
        ResearchSpecificRestriction,
        DataUsePermission,
        UserSpecificRestriction,
        ProjectSpecificRestriction,
        InstitutionSpecificRestriction
    }


    

    mapping(address => Date) providerDateMapping; // data subject
    mapping(address => Date) requesterDateMapping; // data subject

    uint8 constant ROLE_PROVIDER = 1;
    uint8 constant ROLE_REQUESTER = 2;


    // uint8[] Country_Code_8;
    // uint32[] Country_Group_Code_32;
    // mapping(uint8 => uint32) Country_Code_Mapping;
    // mapping(uint8 => uint8[]) Country_Group_Code_Mapping_Baseline;
    // mapping(uint8 => mapping(uint32 => bool)) Country_Group_Code_Mapping_Mapping;



    struct DUO {
        bool NoRestriction;
        bool GeneralResearch;
        bool ClinicalCare;
        bool HMBResearch;
        bool populationAndAncestryResearchOnly;
        bool populationAndAncestryResearchNon;
        bool DiseaseSpecific;
        bool GeneticStudiesOnly;
        bool NonGeneralMethodResearch;
        bool GeographicSpecific;
        bool NonProfitUseOnly;
        bool NonCommercialUseOnly;
        bool PublicationRequired;
        bool PublicationMoratorium;
        bool CollaborationRequired;
        bool EthicsApprovalrequired;
        bool TimeLimitOnUse;
        bool ReturnToResource;
        bool ResearchSpecificRestriction;
        bool DataUsePermission;

        bool UserSpecificRestriction;
        bool ProjectSpecificRestriction;
        bool InstitutionSpecificRestriction;

    }



    struct ADAM {
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
        bool NonPublicationRequired;
        bool DataSecurityMeasures;
        bool DataDestructionRequired;
        bool LinkingOfAccessedRecords;
        bool RecontactingDataSubjects;
        bool IntellectualPropertyClaims;
        bool UseOfAccessedResources;
        bool FeesForAccess;

        bool ReportUsage;
        bool UniformConsent;

        bool UsedByPersons;
        bool UsedByProjects;
        bool UsedByOrganisations;
  
    }

    struct DUO_Extension{
         uint32[] UserSpecificRestriction;
         uint32[] ProjectSpecificRestriction;
         uint32[] InstitutionSpecificRestriction;
    }

    struct ADAM_Extension{
        uint32[] UsedByPersons;
        uint32[] UsedByProjects;
        uint32[] UsedByOrganisations;
    }



    mapping(address => DUO) duo_mapping;
    mapping(address => ADAM) adam_maaping;

    mapping(address => DUO_Extension) provider_extension_mapping;
    mapping(address => ADAM_Extension) requester_extension_maaping;


     function uploadPurposeProvider(
        address _address1,
        DUO memory purpose
    ) public {
        duo_mapping[_address1] = purpose;
        // DataSubjectAcc.push(_address1);
    }

    function uploadPurposeRequester(
        address _address2,
        ADAM memory purpose
    ) public {
        adam_maaping[_address2] = purpose;
        // DataRequesterAcc.push(_address2);
    }

    function GetPurposeItemsProvider(address _address) view public returns (DUO memory) {
              return duo_mapping[_address];
    }

    function GetPurposeItemsRequester(address _address) view public returns (ADAM memory) {
        return adam_maaping[_address];
    }

    function upload_extension_provider(
        address _address1,
        DUO_Extension memory extension
    ) public {
        provider_extension_mapping[_address1] = extension;
    }

    function upload_extension_requester(
        address _address2,
        ADAM_Extension memory extension
    ) public {
        requester_extension_maaping[_address2] = extension;
    }

    function check_users(
        address provider_address,
        address requester_address   
    ) private view returns (bool) {
        DUO_Extension memory provider_extension = provider_extension_mapping[provider_address];
        ADAM_Extension memory requester_extension = requester_extension_maaping[requester_address];

        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (uint256 j = 0; j < requester_extension.UsedByPersons.length; j++) {
            tmp_requester = requester_extension.UsedByPersons[j];
            for (uint256 i = 0; i < provider_extension.UserSpecificRestriction.length; i++) {
                tmp_provider = provider_extension.UserSpecificRestriction[i];
                if (tmp_requester == tmp_provider) {
                    flag = true;
                    break;
                }
            }
            if (flag == false) {
                return false; // Access denied
            }
        }

        return false; // Access denied
    }

    function check_institution(
        address provider_address,
        address requester_address   
    ) private view returns (bool) {
        DUO_Extension memory provider_extension = provider_extension_mapping[provider_address];
        ADAM_Extension memory requester_extension = requester_extension_maaping[requester_address];

        // Check if the provider's extension is empty
        if (provider_extension.UserSpecificRestriction.length == 0 && 
            provider_extension.InstitutionSpecificRestriction.length == 0 && 
            provider_extension.ProjectSpecificRestriction.length == 0) {
            return true; // No restrictions, access granted
        }
        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (uint256 j = 0; j < requester_extension.UsedByOrganisations.length; j++) {
            tmp_requester = requester_extension.UsedByOrganisations[j];
            for (uint256 i = 0; i < provider_extension.InstitutionSpecificRestriction.length; i++) {
                tmp_provider = provider_extension.InstitutionSpecificRestriction[i];
                if (tmp_requester == tmp_provider) {
                    flag = true;
                    break;
                }
            }
            if (flag == false) {
                return false; // Access denied
            }
        }

        return false; // Access denied
    }

    function check_project(
        address provider_address,
        address requester_address   
    ) private view returns (bool) {
        DUO_Extension memory provider_extension = provider_extension_mapping[provider_address];
        ADAM_Extension memory requester_extension = requester_extension_maaping[requester_address];

     
        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (uint256 j = 0; j < requester_extension.UsedByProjects.length; j++) {
            tmp_requester = requester_extension.UsedByProjects[j];
            for (uint256 i = 0; i < provider_extension.ProjectSpecificRestriction.length; i++) {
                tmp_provider = provider_extension.ProjectSpecificRestriction[i];
                if (tmp_requester == tmp_provider) {
                    flag = true;
                    break;
                }
            }
            if (flag == false) {
                return false; // Access denied
            }
        }

        return false; // Access denied
    }

    // function upload_provider_extension(
    //     address _address1,
    //     DUO_Extension memory purpose
    // ) public {
    //     duo_mapping[_address1] = purpose;
    //     // DataSubjectAcc.push(_address1);
    // }
  
    //MARK - UpdateAreaSimple


    // MARK: - DisplayCountryGroupRelation
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
    function DateByRole(
        uint8 role,
        address _address
    ) private view returns (Date storage) {
        if (role == ROLE_PROVIDER) {
            // require(msg.sender == dataProvider, "TermsByRole: Invalid sender");
            return providerDateMapping[_address];
        } else if (role == ROLE_REQUESTER) {
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
        DUO memory provider = duo_mapping[
            _provider_address
        ];
        ADAM memory requester = adam_maaping[
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

        DUO memory provider = duo_mapping[provider_address];
        ADAM memory requester = adam_maaping[requester_address];
        
        if (provider.NoRestriction == true) {
            return 0;
        }
       
        uint32 result = 0;
        uint32 u1=1;

        bool generalResearch = (provider.GeneralResearch == true && 
        (requester.UseForHMBResearch == false ||
        requester.UseForPopulationsResearch == true ||
        requester.UseForAncestryResearch == true || requester.UseByAcademicProfessionals==true));

        bool clinicalCare = (provider.ClinicalCare == true && 
            (requester.UseForMethodsDevelopment== true || 
            requester.UseForReferenceOrControlMaterial == true));

        bool hmbResearch =  (provider.HMBResearch == true && 
            (requester.UseForFundamentalBioResearch == true || 
            requester.UseForGeneticsResearch == true || 
            requester.UseForDrugDevelopmentResearch == true || 
            requester.UseForAgeCategoriesResearch == true || 
           requester.UseForGenderCategoriesResearch == true) ||requester.UseByClinicalProfessionals==true);

        // bool populationAndAncestryResearch = (provider.populationAndAncestryResearchOnly == true &&
        //     (requester.UseForPopulationsResearch == true || 
            // requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true);
        bool populationAndAncestryResearchOnly = (provider.populationAndAncestryResearchOnly == true &&
            (requester.UseForPopulationsResearch == true || 
            requester.UseForAncestryResearch == true || requester.UseByAcademicProfessionals==true));
        bool populationAndAncestryResearchNon = (provider.populationAndAncestryResearchNon == true &&
            (requester.UseForPopulationsResearch == false && 
            requester.UseForAncestryResearch == false || requester.UseByAcademicProfessionals==false));
        
        //  if (!(provider.populationAndAncestryResearchNon == true &&
        //     (requester.UseForPopulationsResearch == false && 
        //     requester.UseForAncestryResearch == false) || requester.UseByAcademicProfessionals==false)) {
        //     result += u1 << uint32(RESULT_CODE.populationAndAncestryResearchNon);
        // }

        // if (!(provider.populationAndAncestryResearchOnly == true &&
        //     (requester.UseForPopulationsResearch == true || 
        //     requester.UseForAncestryResearch == true) || requester.UseByAcademicProfessionals==true)) {
        //     result += u1 << uint32(RESULT_CODE.populationAndAncestryResearchOnly);
        // }

        if ((generalResearch || clinicalCare || hmbResearch || populationAndAncestryResearchOnly || populationAndAncestryResearchNon) == false) {
            return  result += u1 << uint32(RESULT_CODE.FirstCategory);
        }



        // bool tmp_result;
        
        
       
        
        if (provider.ResearchSpecificRestriction == true ){
            if (requester.UseForReferenceOrControlMaterial== false) {
                result += u1 << uint32(RESULT_CODE.ResearchSpecificRestriction);
            }

        }

        if (provider.UserSpecificRestriction == true ){
            if (requester.UsedByPersons == false || check_users(provider_address, requester_address) == false) {
                result += u1 << uint32(RESULT_CODE.UserSpecificRestriction);
            }
        }

        if (provider.ProjectSpecificRestriction == true ){
            if (requester.UsedByProjects == false || check_project(provider_address, requester_address) == false) {
                result += u1 << uint32(RESULT_CODE.ProjectSpecificRestriction);
            }
        }

        if (provider.InstitutionSpecificRestriction == true ){
            if (requester.UsedByOrganisations == false || check_institution(provider_address, requester_address) == false) {
                result += u1 << uint32(RESULT_CODE.InstitutionSpecificRestriction);
            }
        }

   

        // if (!((provider.OpenToResearchUseOnly == true && requester.UseForHMBResearch == false) ||
        //     provider.OpenToResearchUseOnly == false)) {
        //     result += u1 << uint32(RESULT_CODE.OpenToResearchUseOnly);
        // }

  
        if (provider.GeneticStudiesOnly==true) {
            if (requester.UseForGeneticsResearch == false) {
                result += u1 << uint32(RESULT_CODE.GeneticStudiesOnly);
            }
        
        }

        // bool generalMethodResearch = provider.GeneralMethodResearch ? true : requester.UseForMethodsDevelopment == false;



        if (provider.NonGeneralMethodResearch==true) {
            if (requester.UseForMethodsDevelopment == true) {
                result += u1 << uint32(RESULT_CODE.NonGeneralMethodResearch);
            }
            
        }

       
        if (provider.NonProfitUseOnly == true) {
            if (requester.UseForNonProfitPurpose == false || requester.UseForProfitPurpose == true) {
                    result += u1 << uint32(RESULT_CODE.NonProfitUseOnly);
            }
        }
                

        if (provider.NonCommercialUseOnly == true ){
            if (requester.UseByProfitMakingProfessionals == true) {
                result += u1 << uint32(RESULT_CODE.NonCommercialUseOnly);
            }
        }

        if (provider.PublicationRequired == true ){
            if(requester.PublicationRequired == false){
                result += u1 << uint32(RESULT_CODE.PublicationRequired);
            }
        }

        if (provider.PublicationMoratorium == true){
            if (requester.NonPublicationRequired == false) {
                result += u1 << uint32(RESULT_CODE.PublicationMoratorium);
            }
         }

        // tmp_result = provider.CollaborationRequired ? requester.CollaborationRequired : true;
        if (provider.CollaborationRequired == true) { 
            if(requester.CollaborationRequired == false) {
                result += u1 << uint32(RESULT_CODE.CollaborationRequired);
            }
        }

    

        // bool ethicsApprovalrequired = 
        if (provider.EthicsApprovalrequired  == true){
            if(requester.FormalApprovalRequired == false){
                result += u1 << uint32(RESULT_CODE.EthicsApprovalRequired);
            }
        }

        if (provider.ReturnToResource == true ){
            if(requester.ReportUsage == false){
                result += u1 << uint32(RESULT_CODE.ReturnToResource);
            }
        }

        if (provider.DataUsePermission == true ){
            if(requester.UniformConsent == false){
                result += u1 << uint32(RESULT_CODE.DataUsePermission);
            }
        }

        // tmp_result = provider.ProfitOrganisationNon ? requester.UseByProfitMakingProfessionals : true;if 

    //    bool dataSecurityMeasuresRequired =   (provider.DataSecurityMeasuresRequired == true && requester.DataSecurityMeasures == true  && requester.DataDestructionRequired == true && requester.LinkingOfAccessedRecords == true && requester.RecontactingDataSubjects == true && requester.IntellectualPropertyClaims == true && requester.UseOfAccessedResources == true) ||provider.DataSecurityMeasuresRequired == false;

    //     if (!dataSecurityMeasuresRequired) {
    //         result += u1 << uint8(RESULT_CODE.DataSecurityMeasuresRequired);
    //     }

     
        // if (!((provider.CostOnUse == true && requester.FeesForAccess ==  true) ||provider.CostOnUse == false) ) {
        //     result += u1 << uint8(RESULT_CODE.CostOnUse);
        // }


        return result;
    }


    
    function access_data(address provider_address, address requester_address) view public returns (uint32) {

        DUO memory provider = duo_mapping[provider_address];
        ADAM memory requester = adam_maaping[requester_address];
        
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
