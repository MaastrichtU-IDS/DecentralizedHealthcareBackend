
// SPDX-License-Identifier: UNLICENSED
pragma solidity  ^0.8;

contract ConsentCode {
     event LogMessage(string message);

    address public dataProvider;

    constructor()   {
        dataProvider = msg.sender;
    }

    // / Consent Statement
    // / It stores the consent of each individual data subject
    struct DataProvider_PrimaryCategory {
        address address1;
        bool NoRestrictions;
        bool OpenToGeneralResearchAndClinicalCare;
        bool OpenToHMBResearch;
        bool OpenToPopulationAndAncestryResearch;
        bool OpenToDiseaseSpecific;
    }

    struct DataProvider_SecondaryCategory {
        address address1;
        bool OpenToGeneticStudiesOnly;
        bool ResearchSpecificRestrictions;
        bool OpenToResearchUseOnly;
        bool NoGeneralMethodResearch;
    }

    struct DataProvider_Requirements {
        bool GeographicSpecificRestriction;
        bool OpenToNonProfitUseOnly;
        bool PublicationRequired;
        bool CollaborationRequired;
        bool EthicsApprovalrequired;
        bool TimeLimitOnUse;
        bool CostOnUse;
        bool DataSecurityMeasuresRequired;
    }

    // / data requesters purpose statements
    struct HMBResearchPurpose {
        address address2;
        bool UseForFundamentalBioResearch;
        bool UseForGeneticsResearch;
        bool UseForDrugDevelopmentResearch;
        bool UseForAnyDiseaseResearch;
        bool UseForAgeCategoriesResearch;
        bool UseForGenderCategoriesResearch;
    }

    // data requesters general research purpose //
    struct ResearchPurpose {
        address address2;
        bool UseForMethodsDevelopment;
        bool UseForReferenceOrControlMaterial;
        bool UseForPopulationsResearch;
        bool UseForAncestryResearch;
        bool UseForHMBResearch;
    }

    // data requesters clinical purposes //
    struct ClinicalPurpose {
        address address2;
        bool UseForDecisionSupport;
        bool UseForDiseaseSupport;
    }
    // / data requesters type
    struct Person {
        address address2;
        bool UseByAcademicProfessionals;
        bool UseByClinicalProfessionals;
        bool UseByProfitMakingProfessionals;
        bool UseByNonProfessionals;
    }

    struct GeographicSpecificRestriction {
        address address2;
        bool UseBySpecifiedCountries;
    }

    struct Profit {
        address address2;
        bool UseForProfitPurpose;
        bool UseForNonProfitPurpose;
    }

    struct DataRequester_Terms {
        address address2;
        bool NoTimelineRestrictions;
        bool NoFormalApprovalRequired;
        bool NoCollaborationRequired;
        bool NoPublicationRequired;
        bool NoDataSecurityMeasures;
        bool NoDataDestructionRequired;
        bool NoLinkingOfAccessedRecords;
        bool NoRecontactingDataSubjects;
        bool NoIntellectualPropertyClaims;
        bool NoUseOfAccessedResources;
        bool NoFeesForAccess;
        uint16 Year;
        uint16 Month;
        uint16 Day;
    }
    struct DataRequester_Date {
        uint16 Start_Year;
        uint16 Start_Month;
        uint16 Start_Day;
        uint16 End_Year;
        uint16 End_Month;
        uint16 End_Day;
    }

    struct DataProvider_Date {
        uint16 Start_Year;
        uint16 Start_Month;
        uint16 Start_Day;
        uint16 Max_Months;
    }

    struct Requester_Disease_Purpose {
        // string Disease_Name;
        // uint16 Disease_Code;
        uint16[] Disease_Code_Array;
    }

    struct Provider_Disease_Purpose {
        // string Disease_Name;
        // uint16 Disease_Code;
        uint16[] Disease_Code_Array;
    }
    struct Country_Purpose {
        uint32 Group_Code;
        uint256 Country_Code;
    }

    // mapping helps link the input variables to an address //
    mapping(address => DataProvider_PrimaryCategory) providerPrimaryCategoryMapping; // data subject
    mapping(address => DataProvider_SecondaryCategory) providerSecondCategoryMapping; // data subject
    mapping(address => DataProvider_Requirements) provider_requirements_mapping; // data subject
    mapping(address => ResearchPurpose) researchpurpose; // data requester
    mapping(address => HMBResearchPurpose) hmbresearchpurpose;
    mapping(address => ClinicalPurpose) clinicalpurpose;
    mapping(address => Person) requester_person_mapping;
    mapping(address => GeographicSpecificRestriction) requester_geograph_mapping;
    mapping(address => Profit) requester_profit_mapping;
    mapping(address => DataRequester_Terms) datarequesterterms;
    mapping(address => DataRequester_Date) requester_date_mapping;
    mapping(address => DataProvider_Date) provider__date_mapping;

    mapping(address => Provider_Disease_Purpose) provider_disease_mapping;
    mapping(address => Requester_Disease_Purpose) requester_disease_mapping;

    mapping(address => Country_Purpose) provider_country_mapping;
    mapping(address => Country_Purpose) requester_country_mapping;

    address[] DataSubjectAcc;
    address[] DataRequesterAcc;

    // This is the part for the data subject //
    function UploadDataPrimaryCategory(
        address _address1,
        bool _NoRestrictions,
        bool _OpenToGeneralResearchAndClinicalCare,
        bool _OpenToHMBResearch,
        bool _OpenToPopulationAndAncestryResearch,
        bool _OpenToDiseaseSpecific
    ) public {
        require(msg.sender == dataProvider);
        providerPrimaryCategoryMapping[_address1]
            .NoRestrictions = _NoRestrictions;
        providerPrimaryCategoryMapping[_address1]
            .OpenToGeneralResearchAndClinicalCare = _OpenToGeneralResearchAndClinicalCare;
        providerPrimaryCategoryMapping[_address1]
            .OpenToHMBResearch = _OpenToHMBResearch;
        providerPrimaryCategoryMapping[_address1]
            .OpenToPopulationAndAncestryResearch = _OpenToPopulationAndAncestryResearch;
        providerPrimaryCategoryMapping[_address1]
            .OpenToDiseaseSpecific = _OpenToDiseaseSpecific;
        DataSubjectAcc.push(_address1);
    }

    function UploadProviderDate(
        address _address1,
        uint16 start_date_year,
        uint16 start_date_month,
        uint16 start_date_day,
        uint16 max_month_for_requester
    ) public {
        require(msg.sender == dataProvider);
        provider__date_mapping[_address1].Start_Year = start_date_year;
        provider__date_mapping[_address1].Start_Month = start_date_month;
        provider__date_mapping[_address1].Start_Day = start_date_day;

        provider__date_mapping[_address1].Max_Months = max_month_for_requester;
    }

    function GiveRequesterDate(
        address _address2,
        uint16 start_date_year,
        uint16 start_date_month,
        uint16 start_date_day,
        uint16 end_date_year,
        uint16 end_date_month,
        uint16 end_date_day
    ) public {
        requester_date_mapping[_address2].Start_Year = start_date_year;
        requester_date_mapping[_address2].Start_Month = start_date_month;
        requester_date_mapping[_address2].Start_Day = start_date_day;
        requester_date_mapping[_address2].End_Year = end_date_year;
        requester_date_mapping[_address2].End_Month = end_date_month;
        requester_date_mapping[_address2].End_Day = end_date_day;
    }

    function UploadProviderDiseasePurpose(
        address _provider_address,
        uint16[] memory code_array // string memory _provider_purpose_str
    ) public {
        require(msg.sender == dataProvider);

        // provider_disease_purpose_mapping[_provider_address]
        // .Disease_Name = _provider_purpose_str;
        // provider_disease_mapping[_provider_address]
        // .Disease_Code = _provider_purpose_int;
        delete provider_disease_mapping[_provider_address].Disease_Code_Array;
        for (uint i = 0; i < code_array.length; i++) {
            provider_disease_mapping[_provider_address].Disease_Code_Array.push(
                    code_array[i]
                );
        }
    }

    function UploadProviderCountry(
        address _provider_address,
        uint32 _provider_community_code,
        uint256 _provider_country_code
    ) public {
        require(msg.sender == dataProvider);
        provider_country_mapping[_provider_address]
            .Group_Code = _provider_community_code;
        provider_country_mapping[_provider_address]
            .Country_Code = _provider_country_code;
    }

    function GiveRequesterCountry(
        address _requester_address,
        uint32 _requester_community_code,
        uint256 _country_code
    ) public {
        requester_country_mapping[_requester_address]
            .Group_Code = _requester_community_code;
        requester_country_mapping[_requester_address]
            .Country_Code = _country_code;
    }

    function GiveRequesterDiseasePurpose(
        address _requester_address,
        uint16[] memory code_array // string memory _requester_purpose_name
    ) public {
        // requester_disease_purpose_mapping[_requester_address]
        // .Disease_Name = _requester_purpose_name;
        delete requester_disease_mapping[_requester_address].Disease_Code_Array;
        for (uint i = 0; i < code_array.length; i++) {
            requester_disease_mapping[_requester_address]
                .Disease_Code_Array
                .push(code_array[i]);
        }

        // requester_disease_mapping[_requester_address]
        //     .Disease_Code = _requester_purpose_int;
    }

    function UploadDataSecondaryCategory(
        address _address1,
        bool _OpenToGeneticStudiesOnly,
        bool _ResearchSpecificRestrictions,
        bool _OpenToResearchUseOnly,
        bool _NoGeneralMethodResearch
    ) public {
        require(msg.sender == dataProvider);
        providerSecondCategoryMapping[_address1]
            .OpenToGeneticStudiesOnly = _OpenToGeneticStudiesOnly;
        providerSecondCategoryMapping[_address1]
            .ResearchSpecificRestrictions = _ResearchSpecificRestrictions;
        providerSecondCategoryMapping[_address1]
            .OpenToResearchUseOnly = _OpenToResearchUseOnly;
        providerSecondCategoryMapping[_address1]
            .NoGeneralMethodResearch = _NoGeneralMethodResearch;
    }

    function UploadDataRequirements(
        address _address1,
        bool _GeographicSpecificRestriction,
        bool _OpenToNonProfitUseOnly,
        bool _PublicationRequired,
        bool _CollaborationRequired,
        bool _EthicsApprovalrequired,
        bool _TimeLimitOnUse,
        bool _CostOnUse,
        bool _DataSecurityMeasuresRequired
    ) public {
        require(msg.sender == dataProvider);
        provider_requirements_mapping[_address1]
            .GeographicSpecificRestriction = _GeographicSpecificRestriction;
        provider_requirements_mapping[_address1]
            .OpenToNonProfitUseOnly = _OpenToNonProfitUseOnly;
        provider_requirements_mapping[_address1]
            .PublicationRequired = _PublicationRequired;
        provider_requirements_mapping[_address1]
            .CollaborationRequired = _CollaborationRequired;
        provider_requirements_mapping[_address1]
            .EthicsApprovalrequired = _EthicsApprovalrequired;
        provider_requirements_mapping[_address1]
            .TimeLimitOnUse = _TimeLimitOnUse;
        provider_requirements_mapping[_address1].CostOnUse = _CostOnUse;
        provider_requirements_mapping[_address1]
            .DataSecurityMeasuresRequired = _DataSecurityMeasuresRequired;
    }

    // / Function for data requestor
    function giveResearchPurpose(
        address _address2,
        bool _UseForMethodsDevelopment,
        bool _UseForReferenceOrControlMaterial,
        bool _UseForPopulationsResearch,
        bool _UseForAncestryResearch,
        bool _UseForHMBResearch
    ) public {
        researchpurpose[_address2]
            .UseForMethodsDevelopment = _UseForMethodsDevelopment;
        researchpurpose[_address2]
            .UseForReferenceOrControlMaterial = _UseForReferenceOrControlMaterial;
        researchpurpose[_address2]
            .UseForPopulationsResearch = _UseForPopulationsResearch;
        researchpurpose[_address2]
            .UseForAncestryResearch = _UseForAncestryResearch;
        researchpurpose[_address2].UseForHMBResearch = _UseForHMBResearch;
        DataRequesterAcc.push(_address2);
    }

    function giveHMBPurpose(
        address _address2,
        bool _UseForFundamentalBioResearch,
        bool _UseForGeneticsResearch,
        bool _UseForDrugDevelopmentResearch,
        bool _UseForAnyDiseaseResearch,
        bool _UseForAgeCategoriesResearch,
        bool _UseForGenderCategoriesResearch
    ) public {
        hmbresearchpurpose[_address2]
            .UseForFundamentalBioResearch = _UseForFundamentalBioResearch;
        hmbresearchpurpose[_address2]
            .UseForGeneticsResearch = _UseForGeneticsResearch;
        hmbresearchpurpose[_address2]
            .UseForDrugDevelopmentResearch = _UseForDrugDevelopmentResearch;
        hmbresearchpurpose[_address2]
            .UseForAnyDiseaseResearch = _UseForAnyDiseaseResearch;
        hmbresearchpurpose[_address2]
            .UseForAgeCategoriesResearch = _UseForAgeCategoriesResearch;
        hmbresearchpurpose[_address2]
            .UseForGenderCategoriesResearch = _UseForGenderCategoriesResearch;
    }

    function giveClinicalPurpose(
        address _address2,
        bool _UseForDecisionSupport,
        bool _UseForDiseaseSupport
    ) public {
        clinicalpurpose[_address2]
            .UseForDecisionSupport = _UseForDecisionSupport;
        clinicalpurpose[_address2].UseForDiseaseSupport = _UseForDiseaseSupport;
    }

    function givePerson(
        address _address2,
        bool _UseByAcademicProfessionals,
        bool _UseByClinicalProfessionals,
        bool _UseByProfitMakingProfessionals,
        bool _UseByNonProfessionals
    ) public {
        requester_person_mapping[_address2]
            .UseByAcademicProfessionals = _UseByAcademicProfessionals;
        requester_person_mapping[_address2]
            .UseByClinicalProfessionals = _UseByClinicalProfessionals;
        requester_person_mapping[_address2]
            .UseByProfitMakingProfessionals = _UseByProfitMakingProfessionals;
        requester_person_mapping[_address2]
            .UseByNonProfessionals = _UseByNonProfessionals;
    }

    function giveGeographicSpecificRestriction(
        address _address2,
        bool _UseBySpecifiedCountries
    ) public {
        requester_geograph_mapping[_address2]
            .UseBySpecifiedCountries = _UseBySpecifiedCountries;
    }

    function giveProfit(
        address _address2,
        bool _UseForProfitPurpose,
        bool _UseForNonProfitPurpose
    ) public {
        requester_profit_mapping[_address2]
            .UseForProfitPurpose = _UseForProfitPurpose;
        requester_profit_mapping[_address2]
            .UseForNonProfitPurpose = _UseForNonProfitPurpose;
    }

    function getRelativeDays(
        uint16 year,
        uint16 month,
        uint16 day
    ) private pure returns (uint32) {
        return (year - 2000) * 400 + month * 31 + day;
    }

    function giveDataRequester_Terms(
        address _address2,
        bool _NoTimelineRestrictions,
        bool _NoFormalApprovalRequired,
        bool _NoCollaborationRequired,
        bool _NoPublicationRequired,
        bool _NoDataSecurityMeasures,
        bool _NoDataDestructionRequired,
        bool _NoLinkingOfAccessedRecords,
        bool _NoRecontactingDataSubjects,
        bool _NoIntellectualPropertyClaims,
        bool _NoUseOfAccessedResources,
        bool _NoFeesForAccess
    ) public {
        datarequesterterms[_address2]
            .NoTimelineRestrictions = _NoTimelineRestrictions;
        datarequesterterms[_address2]
            .NoFormalApprovalRequired = _NoFormalApprovalRequired;
        datarequesterterms[_address2]
            .NoCollaborationRequired = _NoCollaborationRequired;
        datarequesterterms[_address2]
            .NoPublicationRequired = _NoPublicationRequired;
        datarequesterterms[_address2]
            .NoDataSecurityMeasures = _NoDataSecurityMeasures;
        datarequesterterms[_address2]
            .NoDataDestructionRequired = _NoDataDestructionRequired;
        datarequesterterms[_address2]
            .NoLinkingOfAccessedRecords = _NoLinkingOfAccessedRecords;
        datarequesterterms[_address2]
            .NoRecontactingDataSubjects = _NoRecontactingDataSubjects;
        datarequesterterms[_address2]
            .NoIntellectualPropertyClaims = _NoIntellectualPropertyClaims;
        datarequesterterms[_address2]
            .NoUseOfAccessedResources = _NoUseOfAccessedResources;
        datarequesterterms[_address2].NoFeesForAccess = _NoFeesForAccess;
    }

    function displayDataSubjectAcc() public view returns (address[] memory) {
        return DataSubjectAcc;
    }

    function displayProviderDataRequirement(
        address provider_address
    ) public view returns (bool) {
        return (
            provider_requirements_mapping[provider_address]
                .OpenToNonProfitUseOnly
        );
    }

    function displayRequesterCountry(
        address requester_address
    ) public view returns (uint256) {
        return requester_country_mapping[requester_address].Country_Code;
    }

    function displayProviderCountry(
        address provider_address
    ) public view returns (uint256) {
        return provider_country_mapping[provider_address].Country_Code;
    }

    function displayProviderDiseasePurpose(
        address _provider_address
    ) public view returns (uint16[] memory) {
        return (
            // provider_disease_purpose_mapping[_provider_address].Disease_Name,
            provider_disease_mapping[_provider_address].Disease_Code_Array
        );
    }

    function displayProviderPrimaryCategorye(
        address _provider_address
    ) public view returns (bool, bool, bool, bool, bool) {
        // DataProvider_PrimaryCategory pc = providerPrimaryCategoryMapping[
        //     _provider_address
        // ];
        //     bool NoRestrictions;
        // bool OpenToGeneralResearchAndClinicalCare;
        // bool OpenToHMBResearch;
        // bool OpenToPopulationAndAncestryResearch;
        // bool OpenToDiseaseSpecific;
        return (
            providerPrimaryCategoryMapping[_provider_address].NoRestrictions,
            providerPrimaryCategoryMapping[_provider_address]
                .OpenToGeneralResearchAndClinicalCare,
            providerPrimaryCategoryMapping[_provider_address].OpenToHMBResearch,
            providerPrimaryCategoryMapping[_provider_address]
                .OpenToPopulationAndAncestryResearch,
            providerPrimaryCategoryMapping[_provider_address]
                .OpenToDiseaseSpecific
        );
    }

    function displayRequesterDiseasePurpose(
        address _requester_address
    ) public view returns (uint16[] memory) {
        return (
            // requester_disease_purpose_mapping[_requester_address].Disease_Name,
            requester_disease_mapping[_requester_address].Disease_Code_Array
        );
    }

    function displayDataRequesterAcc() public view returns (address[] memory) {
        return DataRequesterAcc;
    }

    // AccessData function implements the logic of compliance between the consent and purpose statement
    // uint256 public b = 0;
    
    function AccessData1() public pure  returns (int)  {
     uint256 b = 0;
    //  b.push(1);
     return int(0);
    }

    function AccessData2() public pure {
     uint256 b = 0+1;
    //  b.push(1);
    //  return int(0);
    }


/*
     * @dev Function to determine access permission based on various conditions.
     * @param _provider_address The address of the data provider.
     * @param _requester_address The address of the data requester.
     * @return An integer representing the access permission:
     *   - 0: Access granted
     *   - 1: Denied due to research restrictions
     *   - 2: Denied due to research-specific restrictions
     *   - 3: Denied due to research use only restrictions
     *   - 4: Denied for genetics study
     *   - 5: Denied for general method research
     *   - 6: Denied due to disease-specific restrictions
     *   - 7: Denied due to geographical restrictions
     *   - 8: Denied due to profit restrictions
     *   - 9: Denied due to date restrictions
     *   - 10: Denied for various other reasons
     */

    function AccessCountry(       
    address _provider_address,
        address _requester_address
        ) public view returns (int8) {
        // console.log("provider_country_mapping[_provider_address].Country_Code",provider_country_mapping[_provider_address].Country_Code);
        if (
            !(provider_requirements_mapping[_provider_address]
                .GeographicSpecificRestriction ==
                false ||
                (provider_requirements_mapping[_provider_address]
                    .GeographicSpecificRestriction ==
                    true &&
                    requester_geograph_mapping[_requester_address]
                        .UseBySpecifiedCountries ==
                    true))
        ) {
            // console.log("yes");
            if (
                !((requester_country_mapping[_requester_address].Group_Code !=
                    0 &&
                    (requester_country_mapping[_requester_address]
                        .Country_Code &
                        provider_country_mapping[_provider_address]
                            .Country_Code ==
                        requester_country_mapping[_requester_address]
                            .Country_Code)) ||
                    (requester_country_mapping[_requester_address].Group_Code !=
                        0 &&
                        requester_country_mapping[_requester_address]
                            .Group_Code &
                            provider_country_mapping[_provider_address]
                                .Group_Code ==
                        requester_country_mapping[_requester_address]
                            .Group_Code))
            ) {
                // return "false  country purpose";
                return 7;
            }
        }

        return 0;
    }

    function AccessDisease(
        address _provider_address,
        address _requester_address
        )public view returns (uint8) {
        
        if (
            (providerPrimaryCategoryMapping[_provider_address]
                .OpenToGeneralResearchAndClinicalCare ==
                false ||
                (providerPrimaryCategoryMapping[_provider_address]
                    .OpenToGeneralResearchAndClinicalCare ==
                    true &&
                    providerPrimaryCategoryMapping[_provider_address]
                        .OpenToHMBResearch ==
                    true &&
                    providerPrimaryCategoryMapping[_provider_address]
                        .OpenToDiseaseSpecific ==
                    true))
        ) {
            bool disease_flag = false;

            for (
                uint i = 0;
                i <
                provider_disease_mapping[_provider_address]
                    .Disease_Code_Array
                    .length;
                i++
            ) {
                uint16 provider_code = provider_disease_mapping[
                    _provider_address
                ].Disease_Code_Array[i];

                for (
                    uint j = 0;
                    j <
                    requester_disease_mapping[_requester_address]
                        .Disease_Code_Array
                        .length;
                    j++
                ) {
                    uint16 requester_code = requester_disease_mapping[
                        _requester_address
                    ].Disease_Code_Array[j];

                    if (
                        requester_code & provider_code == provider_code &&
                        requester_code >= provider_code
                    ) {
                        // ensure the provider code is a subset of the requester code
                        // given provider 1100,  requester  1110 is granted but 1011 is not

                        disease_flag = true;
                        break;
                    }
                }
                if (disease_flag == true) {
                    break;
                }
            }

            if (disease_flag == false) {
                // return "false  disease purpose";
                return 6;
            }else{
                return 0;
            }

        }
        else{
            return 6;
        }
        // return 0;
    }
    function AccessData(
        address _provider_address,
        address _requester_address
    ) public view returns (uint8) {
        /// **Data provider primary categories

        /// NoRestrictions Block
        if (
            providerPrimaryCategoryMapping[_provider_address].NoRestrictions ==
            true
        ) {
            return 0;
        }
        if (
            /// **Data provider secondary categories
            !((providerPrimaryCategoryMapping[_provider_address]
                .OpenToGeneralResearchAndClinicalCare ==
                true &&
                (researchpurpose[_requester_address].UseForMethodsDevelopment ==
                    true ||
                    researchpurpose[_requester_address]
                        .UseForReferenceOrControlMaterial ==
                    true ||
                    researchpurpose[_requester_address].UseForHMBResearch ==
                    false ||
                    researchpurpose[_requester_address]
                        .UseForPopulationsResearch ==
                    true ||
                    researchpurpose[_requester_address]
                        .UseForAncestryResearch ==
                    true) &&
                requester_person_mapping[_requester_address]
                    .UseByAcademicProfessionals ==
                true) ||
                /// HMB research block
                (providerPrimaryCategoryMapping[_provider_address]
                    .OpenToHMBResearch ==
                    true &&
                    (hmbresearchpurpose[_requester_address]
                        .UseForFundamentalBioResearch ==
                        true ||
                        hmbresearchpurpose[_requester_address]
                            .UseForGeneticsResearch ==
                        true ||
                        hmbresearchpurpose[_requester_address]
                            .UseForDrugDevelopmentResearch ==
                        true ||
                        hmbresearchpurpose[_requester_address]
                            .UseForAnyDiseaseResearch ==
                        false ||
                        hmbresearchpurpose[_requester_address]
                            .UseForAgeCategoriesResearch ==
                        true ||
                        hmbresearchpurpose[_requester_address]
                            .UseForGenderCategoriesResearch ==
                        true) &&
                    requester_person_mapping[_requester_address]
                        .UseByClinicalProfessionals ==
                    true) ||
                /// Population and Ancestry research block
                (providerPrimaryCategoryMapping[_provider_address]
                    .OpenToPopulationAndAncestryResearch ==
                    true &&
                    (researchpurpose[_requester_address]
                        .UseForPopulationsResearch ==
                        true ||
                        researchpurpose[_requester_address]
                            .UseForAncestryResearch ==
                        true) &&
                    requester_person_mapping[_requester_address]
                        .UseByAcademicProfessionals ==
                    true) ||
                /// Disease specific research Block
                (providerPrimaryCategoryMapping[_provider_address]
                    .OpenToDiseaseSpecific ==
                    true &&
                    (hmbresearchpurpose[_requester_address]
                        .UseForAnyDiseaseResearch == true) &&
                    requester_person_mapping[_requester_address]
                        .UseByClinicalProfessionals ==
                    true))
        ) {
            // console.log("research ");
            return 1;
            // return "false research";
        }

        if (
            /// Research specific restriction Block
            //  ////////////////////////////////////////
            !((providerSecondCategoryMapping[_provider_address]
                .ResearchSpecificRestrictions ==
                true &&
                researchpurpose[_requester_address]
                    .UseForReferenceOrControlMaterial ==
                false) ||
                (providerSecondCategoryMapping[_provider_address]
                    .ResearchSpecificRestrictions ==
                    false &&
                    (researchpurpose[_requester_address]
                        .UseForReferenceOrControlMaterial ==
                        true ||
                        researchpurpose[_requester_address]
                            .UseForReferenceOrControlMaterial ==
                        false)))
        ) {
            return 2;
            // return "false  Research specific restriction Block";
        }

        if (
            /// research use only Block
            !((providerSecondCategoryMapping[_provider_address]
                .OpenToResearchUseOnly ==
                true &&
                researchpurpose[_requester_address].UseForHMBResearch ==
                false) ||
                (providerSecondCategoryMapping[_provider_address]
                    .OpenToResearchUseOnly ==
                    false &&
                    (researchpurpose[_requester_address].UseForHMBResearch ==
                        true ||
                        researchpurpose[_requester_address].UseForHMBResearch ==
                        false)))
        ) {
            // return "false  research use only Block";
            return 3;
        }
        if (
            /// Genetics study Block
            !((providerSecondCategoryMapping[_provider_address]
                .OpenToGeneticStudiesOnly ==
                true &&
                hmbresearchpurpose[_requester_address].UseForGeneticsResearch ==
                true) ||
                (providerSecondCategoryMapping[_provider_address]
                    .OpenToGeneticStudiesOnly ==
                    false &&
                    (hmbresearchpurpose[_requester_address]
                        .UseForGeneticsResearch ==
                        false ||
                        hmbresearchpurpose[_requester_address]
                            .UseForGeneticsResearch ==
                        true)))
        ) {
            // return "false  Genetics study Blockk";
            return 4;
        }

        if (
            /// No general method research block
            !((providerSecondCategoryMapping[_provider_address]
                .NoGeneralMethodResearch ==
                true &&
                researchpurpose[_requester_address].UseForMethodsDevelopment ==
                false) ||
                (providerSecondCategoryMapping[_provider_address]
                    .NoGeneralMethodResearch ==
                    false &&
                    (researchpurpose[_requester_address]
                        .UseForMethodsDevelopment ==
                        true ||
                        researchpurpose[_requester_address]
                            .UseForMethodsDevelopment ==
                        false)))
        ) {
            // provider_disease_purpose_mapping[_address1].Disease_Namea;
            // return "false  No general method research block";
            return 5;
        }

        if (
            (providerPrimaryCategoryMapping[_provider_address]
                .OpenToGeneralResearchAndClinicalCare ==
                false ||
                (providerPrimaryCategoryMapping[_provider_address]
                    .OpenToGeneralResearchAndClinicalCare ==
                    true &&
                    providerPrimaryCategoryMapping[_provider_address]
                        .OpenToHMBResearch ==
                    true &&
                    providerPrimaryCategoryMapping[_provider_address]
                        .OpenToDiseaseSpecific ==
                    true))
        ) {
            bool disease_flag = false;

            for (
                uint i = 0;
                i <
                provider_disease_mapping[_provider_address]
                    .Disease_Code_Array
                    .length;
                i++
            ) {
                uint16 provider_code = provider_disease_mapping[
                    _provider_address
                ].Disease_Code_Array[i];

                for (
                    uint j = 0;
                    j <
                    requester_disease_mapping[_requester_address]
                        .Disease_Code_Array
                        .length;
                    j++
                ) {
                    uint16 requester_code = requester_disease_mapping[
                        _requester_address
                    ].Disease_Code_Array[j];

                    if (
                        requester_code & provider_code == provider_code &&
                        requester_code <= provider_code
                    ) {
                        // ensure the provider code is a subset of the requester code
                        // given provider 1100,  requester  1110 is granted but 1011 is not

                        disease_flag = true;
                        break;
                    }
                }
                if (disease_flag == true) {
                    break;
                }
            }

            if (disease_flag == false) {
                // return "false  disease purpose";
                return 6;
            }
        }

        // if (
        //     !(providerPrimaryCategoryMapping[_provider_address]
        //         .OpenToGeneralResearchAndClinicalCare ==
        //         false ||
        //         (providerPrimaryCategoryMapping[_provider_address]
        //             .OpenToGeneralResearchAndClinicalCare ==
        //             true &&
        //             providerPrimaryCategoryMapping[_provider_address]
        //                 .OpenToHMBResearch ==
        //             true &&
        //             providerPrimaryCategoryMapping[_provider_address]
        //                 .OpenToDiseaseSpecific ==
        //             true &&
        //             (requester_disease_mapping[_requester_address]
        //                 .Disease_Code ==
        //                 provider_disease_mapping[_provider_address]
        //                     .Disease_Code)))
        // ) {
        //     return "false  disease purpose";
        // }

        if (
            !(provider_requirements_mapping[_provider_address]
                .GeographicSpecificRestriction ==
                false ||
                (provider_requirements_mapping[_provider_address]
                    .GeographicSpecificRestriction ==
                    true &&
                    requester_geograph_mapping[_requester_address]
                        .UseBySpecifiedCountries ==
                    true))
        ) {
            if (
                !((requester_country_mapping[_requester_address].Group_Code !=
                    0 &&
                    (requester_country_mapping[_requester_address]
                        .Country_Code &
                        provider_country_mapping[_provider_address]
                            .Country_Code ==
                        requester_country_mapping[_requester_address]
                            .Country_Code)) ||
                    (requester_country_mapping[_requester_address].Group_Code !=
                        0 &&
                        requester_country_mapping[_requester_address]
                            .Group_Code &
                            provider_country_mapping[_provider_address]
                                .Group_Code ==
                        requester_country_mapping[_requester_address]
                            .Group_Code))
            ) {
                // return "false  country purpose";
                return 7;
            }
        }

        if (
            /// Profit block
            !((provider_requirements_mapping[_provider_address]
                .OpenToNonProfitUseOnly ==
                true &&
                (requester_profit_mapping[_requester_address]
                    .UseForNonProfitPurpose ==
                    true &&
                    requester_profit_mapping[_requester_address]
                        .UseForProfitPurpose ==
                    false &&
                    requester_person_mapping[_requester_address]
                        .UseByProfitMakingProfessionals ==
                    false)) ||
                provider_requirements_mapping[_provider_address]
                    .OpenToNonProfitUseOnly ==
                false)
        ) {
            // return "false  Profit block";
            return 8;
        }

        if (
            /// Profit block
            /// Check date
            !(
                ((getRelativeDays(
                    provider__date_mapping[_provider_address].Start_Year,
                    provider__date_mapping[_provider_address].Start_Month,
                    provider__date_mapping[_provider_address].Start_Day
                ) <
                    getRelativeDays(
                        requester_date_mapping[_requester_address].Start_Year,
                        requester_date_mapping[_requester_address].Start_Month,
                        requester_date_mapping[_requester_address].Start_Day
                    )) &&
                    ((requester_date_mapping[_requester_address].End_Year -
                        requester_date_mapping[_requester_address].Start_Year) *
                        12 +
                        (requester_date_mapping[_requester_address].End_Month -
                            requester_date_mapping[_requester_address]
                                .Start_Month)) <
                    provider__date_mapping[_provider_address].Max_Months)
            )
        ) {
            // return "false Check date";
            return 9;
        }

        if (
            /// **Data provider requirements

            /// Publication required
            ((provider_requirements_mapping[_provider_address]
                .PublicationRequired ==
                true &&
                datarequesterterms[_requester_address].NoPublicationRequired ==
                false) ||
                (provider_requirements_mapping[_provider_address]
                    .PublicationRequired ==
                    false &&
                    (datarequesterterms[_requester_address]
                        .NoPublicationRequired ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoPublicationRequired ==
                        false))) &&
            /// Geographical restrictions
            ((provider_requirements_mapping[_provider_address]
                .GeographicSpecificRestriction ==
                true &&
                requester_geograph_mapping[_requester_address]
                    .UseBySpecifiedCountries ==
                true) ||
                (provider_requirements_mapping[_provider_address]
                    .GeographicSpecificRestriction ==
                    false &&
                    (requester_geograph_mapping[_requester_address]
                        .UseBySpecifiedCountries ==
                        false ||
                        requester_geograph_mapping[_requester_address]
                            .UseBySpecifiedCountries ==
                        true))) &&
            /// Time limit restrictions
            ((provider_requirements_mapping[_provider_address].TimeLimitOnUse ==
                true &&
                datarequesterterms[_requester_address].NoTimelineRestrictions ==
                false) ||
                (provider_requirements_mapping[_provider_address]
                    .TimeLimitOnUse ==
                    false &&
                    (datarequesterterms[_requester_address]
                        .NoTimelineRestrictions ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoTimelineRestrictions ==
                        false))) &&
            /// Collaboration required
            ((provider_requirements_mapping[_provider_address]
                .CollaborationRequired ==
                true &&
                datarequesterterms[_requester_address]
                    .NoCollaborationRequired ==
                false) ||
                (provider_requirements_mapping[_provider_address]
                    .CollaborationRequired ==
                    false &&
                    (datarequesterterms[_requester_address]
                        .NoCollaborationRequired ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoCollaborationRequired ==
                        false))) &&
            /// Ethics approval required
            ((provider_requirements_mapping[_provider_address]
                .EthicsApprovalrequired ==
                true &&
                datarequesterterms[_requester_address]
                    .NoFormalApprovalRequired ==
                false) ||
                (provider_requirements_mapping[_provider_address]
                    .EthicsApprovalrequired ==
                    false &&
                    (datarequesterterms[_requester_address]
                        .NoFormalApprovalRequired ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoFormalApprovalRequired ==
                        false))) &&
            /// Data security measures required
            ((provider_requirements_mapping[_provider_address]
                .DataSecurityMeasuresRequired ==
                true &&
                datarequesterterms[_requester_address].NoDataSecurityMeasures ==
                false &&
                datarequesterterms[_requester_address]
                    .NoDataDestructionRequired ==
                false &&
                datarequesterterms[_requester_address]
                    .NoLinkingOfAccessedRecords ==
                false &&
                datarequesterterms[_requester_address]
                    .NoRecontactingDataSubjects ==
                false &&
                datarequesterterms[_requester_address]
                    .NoIntellectualPropertyClaims ==
                false &&
                datarequesterterms[_requester_address]
                    .NoUseOfAccessedResources ==
                false) ||
                (provider_requirements_mapping[_provider_address]
                    .DataSecurityMeasuresRequired ==
                    false &&
                    ((datarequesterterms[_requester_address]
                        .NoDataSecurityMeasures ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoDataDestructionRequired ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoLinkingOfAccessedRecords ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoRecontactingDataSubjects ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoIntellectualPropertyClaims ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoUseOfAccessedResources ==
                        true) ||
                        (datarequesterterms[_requester_address]
                            .NoDataSecurityMeasures ==
                            false ||
                            datarequesterterms[_requester_address]
                                .NoDataDestructionRequired ==
                            false ||
                            datarequesterterms[_requester_address]
                                .NoLinkingOfAccessedRecords ==
                            false ||
                            datarequesterterms[_requester_address]
                                .NoRecontactingDataSubjects ==
                            false ||
                            datarequesterterms[_requester_address]
                                .NoIntellectualPropertyClaims ==
                            false ||
                            datarequesterterms[_requester_address]
                                .NoUseOfAccessedResources ==
                            false)))) &&
            /// Cost on Use
            ((provider_requirements_mapping[_provider_address].CostOnUse ==
                true &&
                datarequesterterms[_requester_address].NoFeesForAccess ==
                false) ||
                (provider_requirements_mapping[_provider_address].CostOnUse ==
                    false &&
                    (datarequesterterms[_requester_address].NoFeesForAccess ==
                        true ||
                        datarequesterterms[_requester_address]
                            .NoFeesForAccess ==
                        false)))
        ) {
            // return "true";
            return 0;
        } else {
            // return "false";
            return 10;
        }
    }
}
