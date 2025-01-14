// SPDX-License-Identifier: AFL-3.0	

pragma solidity ^0.8;

contract ConsentCode {
    address public dataProvider;

    constructor() public {
        dataProvider = msg.sender;
    }

    struct DataProvider {
        address address1;
        bool Restrictions;
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

    struct DataRequester {
        address address2;
        bool UseForMethodsDevelopment;
        bool UseForReferenceOrControlMaterial;
        bool UseForPopulationsResearch;
        bool UseForAncestryResearch;
        bool UseForHMBResearch;
        bool UseForFundamentalBioResearch;
        bool UseForGeneticsResearch;
        bool UseForDrugDevelopmentResearch;
        bool UseForAnyDiseaseResearch;
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

    mapping(address => DataProvider) dataProviders;
    mapping(address => DataRequester) dataRequesters;

    address[] DataSubjectAcc;
    address[] DataRequesterAcc;

    function uploadDataProvider(
        address _address1,
        bool _Restrictions,
        bool _OpenToGeneralResearchAndClinicalCare,
        bool _OpenToHMBResearch,
        bool _OpenToPopulationAndAncestryResearch,
        bool _OpenToDiseaseSpecific,
        bool _OpenToGeneticStudiesOnly,
        bool _ResearchSpecificRestrictions,
        bool _OpenToResearchUseOnly,
        bool _GeneralMethodResearch,
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
        dataProviders[_address1] = DataProvider(
            _address1,
            _Restrictions,
            _OpenToGeneralResearchAndClinicalCare,
            _OpenToHMBResearch,
            _OpenToPopulationAndAncestryResearch,
            _OpenToDiseaseSpecific,
            _OpenToGeneticStudiesOnly,
            _ResearchSpecificRestrictions,
            _OpenToResearchUseOnly,
            _GeneralMethodResearch,
            _GeographicSpecificRestriction,
            _OpenToNonProfitUseOnly,
            _PublicationRequired,
            _CollaborationRequired,
            _EthicsApprovalrequired,
            _TimeLimitOnUse,
            _CostOnUse,
            _DataSecurityMeasuresRequired
        );
        // DataSubjectAcc.push(_address1);
    }

    function uploadDataRequester(
        address _address2,
        bool _UseForMethodsDevelopment,
        bool _UseForReferenceOrControlMaterial,
        bool _UseForPopulationsResearch,
        bool _UseForAncestryResearch,
        bool _UseForHMBResearch,
        bool _UseForFundamentalBioResearch,
        bool _UseForGeneticsResearch,
        bool _UseForDrugDevelopmentResearch,
        bool _UseForAnyDiseaseResearch,
        bool _UseForAgeCategoriesResearch,
        bool _UseForGenderCategoriesResearch,
        bool _UseForDecisionSupport,
        bool _UseForDiseaseSupport,
        bool _UseByAcademicProfessionals,
        bool _UseByClinicalProfessionals,
        bool _UseByProfitMakingProfessionals,
        bool _UseByNonProfessionals,
        bool _UseBySpecifiedCountries,
        bool _UseForProfitPurpose,
        bool _UseForNonProfitPurpose,
        bool _TimelineRestrictions,
        bool _FormalApprovalRequired,
        bool _CollaborationRequired,
        bool _PublicationRequired,
        bool _DataSecurityMeasures,
        bool _DataDestructionRequired,
        bool _LinkingOfAccessedRecords,
        bool _RecontactingDataSubjects,
        bool _IntellectualPropertyClaims,
        bool _UseOfAccessedResources,
        bool _FeesForAccess
    ) public {
        dataRequesters[_address2] = DataRequester(
            _address2,
            _UseForMethodsDevelopment,
            _UseForReferenceOrControlMaterial,
            _UseForPopulationsResearch,
            _UseForAncestryResearch,
            _UseForHMBResearch,
            _UseForFundamentalBioResearch,
            _UseForGeneticsResearch,
            _UseForDrugDevelopmentResearch,
            _UseForAnyDiseaseResearch,
            _UseForAgeCategoriesResearch,
            _UseForGenderCategoriesResearch,
            _UseForDecisionSupport,
            _UseForDiseaseSupport,
            _UseByAcademicProfessionals,
            _UseByClinicalProfessionals,
            _UseByProfitMakingProfessionals,
            _UseByNonProfessionals,
            _UseBySpecifiedCountries,
            _UseForProfitPurpose,
            _UseForNonProfitPurpose,
            _TimelineRestrictions,
            _FormalApprovalRequired,
            _CollaborationRequired,
            _PublicationRequired,
            _DataSecurityMeasures,
            _DataDestructionRequired,
            _LinkingOfAccessedRecords,
            _RecontactingDataSubjects,
            _IntellectualPropertyClaims,
            _UseOfAccessedResources,
            _FeesForAccess
        );
        // DataRequesterAcc.push(_address2);
    }

    // function displayDataSubjectAcc(address _address1) view public returns (address[] memory) {
    //     return DataSubjectAcc;
    // }

    // function displayDataRequesterAcc() view public returns (address[] memory) {
    //     return DataRequesterAcc;
    // }

    function accessData(address _address1, address _address2) view public returns (bool) {
        DataProvider memory provider = dataProviders[_address1];
        DataRequester memory requester = dataRequesters[_address2];

        bool generalResearchAndClinicalCare = provider.OpenToGeneralResearchAndClinicalCare &&
            (requester.UseForMethodsDevelopment ||
            requester.UseForReferenceOrControlMaterial ||
            requester.UseForPopulationsResearch ||
            requester.UseForAncestryResearch) &&
            requester.UseByAcademicProfessionals;

        bool hmbResearch = provider.OpenToHMBResearch &&
            (requester.UseForFundamentalBioResearch ||
            requester.UseForGeneticsResearch ||
            requester.UseForDrugDevelopmentResearch ||
            requester.UseForAgeCategoriesResearch ||
            requester.UseForGenderCategoriesResearch) &&
            requester.UseByClinicalProfessionals;

        bool populationAndAncestryResearch = provider.OpenToPopulationAndAncestryResearch &&
            (requester.UseForPopulationsResearch ||
            requester.UseForAncestryResearch) &&
            requester.UseByAcademicProfessionals;

        bool diseaseSpecificResearch = provider.OpenToDiseaseSpecific &&
            requester.UseForAnyDiseaseResearch &&
            requester.UseByClinicalProfessionals;

        bool researchSpecificRestrictions = provider.ResearchSpecificRestrictions && requester.UseForReferenceOrControlMaterial;
        bool openToResearchUseOnly = provider.OpenToResearchUseOnly && requester.UseForHMBResearch;
        bool openToGeneticStudiesOnly = provider.OpenToGeneticStudiesOnly && !requester.UseForGeneticsResearch;
        bool generalMethodResearch = provider.GeneralMethodResearch && requester.UseForMethodsDevelopment;
        bool openToNonProfitUseOnly = provider.OpenToNonProfitUseOnly &&
            (requester.UseForProfitPurpose || requester.UseByProfitMakingProfessionals);
        bool publicationRequired = provider.PublicationRequired && requester.PublicationRequired;
        bool geographicSpecificRestriction = provider.GeographicSpecificRestriction && !requester.UseBySpecifiedCountries;
        bool timeLimitOnUse = provider.TimeLimitOnUse && requester.TimelineRestrictions;
        bool collaborationRequired = provider.CollaborationRequired && requester.CollaborationRequired;
        bool ethicsApprovalrequired = provider.EthicsApprovalrequired && requester.FormalApprovalRequired;
        bool dataSecurityMeasuresRequired = provider.DataSecurityMeasuresRequired &&
            (requester.DataSecurityMeasures ||
            requester.DataDestructionRequired ||
            requester.LinkingOfAccessedRecords ||
            requester.RecontactingDataSubjects ||
            requester.IntellectualPropertyClaims ||
            requester.UseOfAccessedResources);
        bool costOnUse = provider.CostOnUse && requester.FeesForAccess;

        return provider.Restrictions ||
            generalResearchAndClinicalCare ||
            hmbResearch ||
            populationAndAncestryResearch ||
            diseaseSpecificResearch ||
            !researchSpecificRestrictions &&
            !openToResearchUseOnly &&
            !openToGeneticStudiesOnly &&
            !generalMethodResearch &&
            !openToNonProfitUseOnly &&
            !publicationRequired &&
            !geographicSpecificRestriction &&
            !timeLimitOnUse &&
            !collaborationRequired &&
            !ethicsApprovalrequired &&
            !dataSecurityMeasuresRequired &&
            !costOnUse;
    }
}
