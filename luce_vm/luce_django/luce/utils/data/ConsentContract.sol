pragma solidity ^0.4.25;

contract ConsentCode{
    address public dataProvider;
    
    constructor () public{
                dataProvider=msg.sender;
    }
    
    /// Consent Statement
    /// It stores the consent of each individual data subject 
    struct DataProvider_PrimaryCategory{
        address address1;
        bool NoRestrictions;
        bool OpenToGeneralResearchAndClinicalCare;
        bool OpenToHMBResearch; 
        bool OpenToPopulationAndAncestryResearch;
        bool OpenToDiseaseSpecific;
    }
        
    struct DataProvider_SecondaryCategory{
        address address1;
        bool OpenToGeneticStudiesOnly;
        bool ResearchSpecificRestrictions;
        bool OpenToResearchUseOnly;
        bool NoGeneralMethodResearch;
    }
        
    struct DataProvider_Requirements{
        bool GeographicSpecificRestriction;
        bool OpenToNonProfitUseOnly;
        bool PublicationRequired;
        bool CollaborationRequired;
        bool EthicsApprovalrequired;
        bool TimeLimitOnUse;
        bool CostOnUse;
        bool DataSecurityMeasuresRequired;
    }

    /// data requesters purpose statements 
    struct HMBResearchPurpose{ 
        address address2;
        bool UseForFundamentalBioResearch;
        bool UseForGeneticsResearch;
        bool UseForDrugDevelopmentResearch; 
        bool UseForAnyDiseaseResearch;
        bool UseForAgeCategoriesResearch;
        bool UseForGenderCategoriesResearch;
    }

    // data requesters general research purpose //
    struct ResearchPurpose{
        address address2;
        bool UseForMethodsDevelopment;
        bool UseForReferenceOrControlMaterial; 
        bool UseForPopulationsResearch;
        bool UseForAncestryResearch;
        bool UseForHMBResearch;
    }

    // data requesters clinical purposes //
    struct ClinicalPurpose{ 
        address address2; 
        bool UseForDecisionSupport; 
        bool UseForDiseaseSupport;
    }
    /// data requesters type 
    struct Person{
        address address2; 
        bool UseByAcademicProfessionals;
        bool UseByClinicalProfessionals;
        bool UseByProfitMakingProfessionals; 
        bool UseByNonProfessionals;
    }
    
    struct GeographicSpecificRestriction{
        address address2;
        bool UseBySpecifiedCountries;
    }

    struct Profit{
        address address2;
        bool UseForProfitPurpose;
        bool UseForNonProfitPurpose;
    }
    
    struct DataRequester_Terms{
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
    }
    
    // mapping helps link the input variables to an address //
    mapping (address => DataProvider_PrimaryCategory) objects; // data subject
    mapping (address => DataProvider_SecondaryCategory) objects1; // data subject
    mapping (address => DataProvider_Requirements) objects2; // data subject
    mapping (address => ResearchPurpose) researchpurpose; // data requester 
    mapping (address => HMBResearchPurpose) hmbresearchpurpose; 
    mapping (address => ClinicalPurpose) clinicalpurpose;
    mapping (address => Person) person;
    mapping (address => GeographicSpecificRestriction) geographicrestriction;
    mapping (address => Profit) profit;
    mapping (address => DataRequester_Terms) datarequesterterms;
    
    address[] DataSubjectAcc; 
    address[] DataRequesterAcc;

    // This is the part for the data subject //
    function UploadDataPrimaryCategory(
        address _address1, 
        bool _NoRestrictions,
        bool _OpenToGeneralResearchAndClinicalCare,
        bool _OpenToHMBResearch,
        bool _OpenToPopulationAndAncestryResearch,
        bool _OpenToDiseaseSpecific) public {
            require(msg.sender == dataProvider);
            objects[_address1].NoRestrictions = _NoRestrictions;
            objects[_address1].OpenToGeneralResearchAndClinicalCare = _OpenToGeneralResearchAndClinicalCare; 
            objects[_address1].OpenToHMBResearch = _OpenToHMBResearch; 
            objects[_address1].OpenToPopulationAndAncestryResearch = _OpenToPopulationAndAncestryResearch; 
            objects[_address1].OpenToDiseaseSpecific = _OpenToDiseaseSpecific;
            DataSubjectAcc.push(_address1)-1; 
    }
    
    function UploadDataSecondaryCategory(
        address _address1, 
        bool _OpenToGeneticStudiesOnly,
        bool _ResearchSpecificRestrictions,
        bool _OpenToResearchUseOnly,
        bool _NoGeneralMethodResearch) public {
            require(msg.sender == dataProvider);
            objects1[_address1].OpenToGeneticStudiesOnly = _OpenToGeneticStudiesOnly;
            objects1[_address1].ResearchSpecificRestrictions = _ResearchSpecificRestrictions;
            objects1[_address1].OpenToResearchUseOnly = _OpenToResearchUseOnly;
            objects1[_address1].NoGeneralMethodResearch = _NoGeneralMethodResearch;
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
        bool _DataSecurityMeasuresRequired) public {
            require(msg.sender == dataProvider);
            objects2[_address1].GeographicSpecificRestriction = _GeographicSpecificRestriction;
            objects2[_address1].OpenToNonProfitUseOnly = _OpenToNonProfitUseOnly;
            objects2[_address1].PublicationRequired = _PublicationRequired;
            objects2[_address1].CollaborationRequired = _CollaborationRequired;
            objects2[_address1].EthicsApprovalrequired = _EthicsApprovalrequired;
            objects2[_address1].TimeLimitOnUse = _TimeLimitOnUse;
            objects2[_address1].CostOnUse = _CostOnUse;
            objects2[_address1].DataSecurityMeasuresRequired = _DataSecurityMeasuresRequired;
    }
        
    /// Function for data requestor
    function giveResearchPurpose( 
        address _address2,
        bool _UseForMethodsDevelopment,
        bool _UseForReferenceOrControlMaterial,
        bool _UseForPopulationsResearch,
        bool _UseForAncestryResearch,
        bool _UseForHMBResearch) public {
            researchpurpose[_address2].UseForMethodsDevelopment = _UseForMethodsDevelopment; 
            researchpurpose[_address2].UseForReferenceOrControlMaterial = _UseForReferenceOrControlMaterial; 
            researchpurpose[_address2].UseForPopulationsResearch = _UseForPopulationsResearch; 
            researchpurpose[_address2].UseForAncestryResearch = _UseForAncestryResearch;
            researchpurpose[_address2].UseForHMBResearch = _UseForHMBResearch;
            DataRequesterAcc.push(_address2) -1;
    }

    function giveHMBPurpose( 
        address _address2, 
        bool _UseForFundamentalBioResearch,
        bool _UseForGeneticsResearch,
        bool _UseForDrugDevelopmentResearch, 
        bool _UseForAnyDiseaseResearch,
        bool _UseForAgeCategoriesResearch,
        bool _UseForGenderCategoriesResearch)public {
            hmbresearchpurpose[_address2].UseForFundamentalBioResearch = _UseForFundamentalBioResearch; 
            hmbresearchpurpose[_address2].UseForGeneticsResearch = _UseForGeneticsResearch; 
            hmbresearchpurpose[_address2].UseForDrugDevelopmentResearch = _UseForDrugDevelopmentResearch; 
            hmbresearchpurpose[_address2].UseForAnyDiseaseResearch = _UseForAnyDiseaseResearch; 
            hmbresearchpurpose[_address2].UseForAgeCategoriesResearch = _UseForAgeCategoriesResearch;
            hmbresearchpurpose[_address2].UseForGenderCategoriesResearch = _UseForGenderCategoriesResearch;
    }

    function giveClinicalPurpose( 
        address _address2, 
        bool _UseForDecisionSupport, 
        bool _UseForDiseaseSupport)public {
            clinicalpurpose[_address2].UseForDecisionSupport = _UseForDecisionSupport; 
            clinicalpurpose[_address2].UseForDiseaseSupport = _UseForDiseaseSupport;
    }
    
    function givePerson( 
        address _address2,
        bool _UseByAcademicProfessionals,
        bool _UseByClinicalProfessionals,
        bool _UseByProfitMakingProfessionals, 
        bool _UseByNonProfessionals)public {
            person[_address2].UseByAcademicProfessionals = _UseByAcademicProfessionals; 
            person[_address2].UseByClinicalProfessionals = _UseByClinicalProfessionals;
            person[_address2].UseByProfitMakingProfessionals = _UseByProfitMakingProfessionals;
            person[_address2].UseByNonProfessionals = _UseByNonProfessionals; 
    }
    
    function giveGeographicSpecificRestriction( 
        address _address2, 
        bool _UseBySpecifiedCountries)public {
            geographicrestriction[_address2].UseBySpecifiedCountries = _UseBySpecifiedCountries; 
    }
    
    function giveProfit( 
        address _address2, 
        bool _UseForProfitPurpose,
        bool _UseForNonProfitPurpose)public {
            profit[_address2].UseForProfitPurpose = _UseForProfitPurpose; 
            profit[_address2].UseForNonProfitPurpose = _UseForNonProfitPurpose; 
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
        bool _NoFeesForAccess)public {
            datarequesterterms[_address2].NoTimelineRestrictions = _NoTimelineRestrictions; 
            datarequesterterms[_address2].NoFormalApprovalRequired = _NoFormalApprovalRequired;
            datarequesterterms[_address2].NoCollaborationRequired = _NoCollaborationRequired;
            datarequesterterms[_address2].NoPublicationRequired = _NoPublicationRequired;
            datarequesterterms[_address2].NoDataSecurityMeasures = _NoDataSecurityMeasures;
            datarequesterterms[_address2].NoDataDestructionRequired = _NoDataDestructionRequired;
            datarequesterterms[_address2].NoLinkingOfAccessedRecords = _NoLinkingOfAccessedRecords;
            datarequesterterms[_address2].NoRecontactingDataSubjects = _NoRecontactingDataSubjects;
            datarequesterterms[_address2].NoIntellectualPropertyClaims = _NoIntellectualPropertyClaims;
            datarequesterterms[_address2].NoUseOfAccessedResources = _NoUseOfAccessedResources;
            datarequesterterms[_address2].NoFeesForAccess = _NoFeesForAccess;
    }
    
    function displayDataSubjectAcc() view public returns(address[] memory) { 
        return DataSubjectAcc;
    }
    
    function displayDataRequesterAcc() view public returns(address[] memory) { 
        return DataRequesterAcc;
    }
    
    // AccessData function implements the logic of compliance between the consent and purpose statement
    function AccessData (address _address1,address _address2) view public returns (bool) { 
        
        /// **Data provider primary categories
        
        /// NoRestrictions Block           
        if(objects[_address1].NoRestrictions==true) {
                return true;
            }
            /// GeneralResearch and ClinicalCare block
            else if(((objects[_address1].OpenToGeneralResearchAndClinicalCare == true && 
            (researchpurpose[_address2].UseForMethodsDevelopment== true || 
            researchpurpose[_address2].UseForReferenceOrControlMaterial == true || 
            researchpurpose[_address2].UseForHMBResearch == false ||
            researchpurpose[_address2].UseForPopulationsResearch == true ||
            researchpurpose[_address2].UseForAncestryResearch == true) && person[_address2].UseByAcademicProfessionals==true)||
            
            /// HMB research block
            (objects[_address1].OpenToHMBResearch == true && 
            (hmbresearchpurpose[_address2].UseForFundamentalBioResearch == true || 
            hmbresearchpurpose[_address2].UseForGeneticsResearch == true || 
            hmbresearchpurpose[_address2].UseForDrugDevelopmentResearch == true || 
            hmbresearchpurpose[_address2].UseForAnyDiseaseResearch == false || 
            hmbresearchpurpose[_address2].UseForAgeCategoriesResearch == true || 
            hmbresearchpurpose[_address2].UseForGenderCategoriesResearch == true) && person[_address2].UseByClinicalProfessionals==true)||
            
            /// Population and Ancestry research block
            (objects[_address1].OpenToPopulationAndAncestryResearch == true &&
            (researchpurpose[_address2].UseForPopulationsResearch == true || 
            researchpurpose[_address2].UseForAncestryResearch == true) && person[_address2].UseByAcademicProfessionals==true)||
            
            /// Disease specific research Block
            (objects[_address1].OpenToDiseaseSpecific == true &&
            (hmbresearchpurpose[_address2].UseForAnyDiseaseResearch == true) && person[_address2].UseByClinicalProfessionals==true)) &&
            
            /// **Data provider secondary categories
            
            /// Research specific restriction Block
            ((objects1[_address1].ResearchSpecificRestrictions == true && researchpurpose[_address2].UseForReferenceOrControlMaterial== false) || 
             (objects1[_address1].ResearchSpecificRestrictions == false && (researchpurpose[_address2].UseForReferenceOrControlMaterial== true || researchpurpose[_address2].UseForReferenceOrControlMaterial== false))) &&
            
            /// research use only Block
            ((objects1[_address1].OpenToResearchUseOnly == true && researchpurpose[_address2].UseForHMBResearch == false) ||
            (objects1[_address1].OpenToResearchUseOnly == false && (researchpurpose[_address2].UseForHMBResearch == true || researchpurpose[_address2].UseForHMBResearch == false))) &&
           
            /// Genetics study Block
            ((objects1[_address1].OpenToGeneticStudiesOnly==true && hmbresearchpurpose[_address2].UseForGeneticsResearch == true) ||
            (objects1[_address1].OpenToGeneticStudiesOnly==false && (hmbresearchpurpose[_address2].UseForGeneticsResearch == false || hmbresearchpurpose[_address2].UseForGeneticsResearch == true))) &&
            
            /// No general method research block
            ((objects1[_address1].NoGeneralMethodResearch==true && researchpurpose[_address2].UseForMethodsDevelopment == false) ||
            (objects1[_address1].NoGeneralMethodResearch==false && (researchpurpose[_address2].UseForMethodsDevelopment == true || researchpurpose[_address2].UseForMethodsDevelopment == false)))  &&
            
            /// **Data provider requirements
            
            /// Profit block
            ((objects2[_address1].OpenToNonProfitUseOnly == true && (profit[_address2].UseForNonProfitPurpose == true && profit[_address2].UseForProfitPurpose == false &&
            person[_address2].UseByProfitMakingProfessionals == false)) || 
            (objects2[_address1].OpenToNonProfitUseOnly == false && (profit[_address2].UseForNonProfitPurpose == false || profit[_address2].UseForNonProfitPurpose == true || profit[_address2].UseForProfitPurpose == true || profit[_address2].UseForProfitPurpose == false ||
            person[_address2].UseByProfitMakingProfessionals == true || person[_address2].UseByProfitMakingProfessionals == false))) &&
            
            
            /// Publication required
            ((objects2[_address1].PublicationRequired == true && datarequesterterms[_address2].NoPublicationRequired == false) ||
            (objects2[_address1].PublicationRequired == false && (datarequesterterms[_address2].NoPublicationRequired == true || datarequesterterms[_address2].NoPublicationRequired == false))) &&
            
            /// Geographical restrictions
            ((objects2[_address1].GeographicSpecificRestriction == true && geographicrestriction[_address2].UseBySpecifiedCountries == true) ||
            (objects2[_address1].GeographicSpecificRestriction == false && (geographicrestriction[_address2].UseBySpecifiedCountries == false || geographicrestriction[_address2].UseBySpecifiedCountries == true))) &&
              
            /// Time limit restrictions
            ((objects2[_address1].TimeLimitOnUse == true && datarequesterterms[_address2].NoTimelineRestrictions == false) ||
            (objects2[_address1].TimeLimitOnUse == false && (datarequesterterms[_address2].NoTimelineRestrictions == true || datarequesterterms[_address2].NoTimelineRestrictions == false))) &&
             
            /// Collaboration required
            ((objects2[_address1].CollaborationRequired == true && datarequesterterms[_address2].NoCollaborationRequired == false) ||
            (objects2[_address1].CollaborationRequired == false && (datarequesterterms[_address2].NoCollaborationRequired == true || datarequesterterms[_address2].NoCollaborationRequired == false))) &&
            
            /// Ethics approval required
            ((objects2[_address1].EthicsApprovalrequired == true && datarequesterterms[_address2].NoFormalApprovalRequired == false) ||
            (objects2[_address1].EthicsApprovalrequired == false && (datarequesterterms[_address2].NoFormalApprovalRequired == true || datarequesterterms[_address2].NoFormalApprovalRequired == false))) &&
            
            /// Data security measures required
            ((objects2[_address1].DataSecurityMeasuresRequired == true && datarequesterterms[_address2].NoDataSecurityMeasures == false  && datarequesterterms[_address2].NoDataDestructionRequired == false && datarequesterterms[_address2].NoLinkingOfAccessedRecords == false && datarequesterterms[_address2].NoRecontactingDataSubjects == false && datarequesterterms[_address2].NoIntellectualPropertyClaims == false && datarequesterterms[_address2].NoUseOfAccessedResources == false) ||
            (objects2[_address1].DataSecurityMeasuresRequired == false && ((datarequesterterms[_address2].NoDataSecurityMeasures == true  || datarequesterterms[_address2].NoDataDestructionRequired == true || datarequesterterms[_address2].NoLinkingOfAccessedRecords == true || datarequesterterms[_address2].NoRecontactingDataSubjects == true || datarequesterterms[_address2].NoIntellectualPropertyClaims == true || datarequesterterms[_address2].NoUseOfAccessedResources == true) || (datarequesterterms[_address2].NoDataSecurityMeasures == false  || datarequesterterms[_address2].NoDataDestructionRequired == false || datarequesterterms[_address2].NoLinkingOfAccessedRecords == false || datarequesterterms[_address2].NoRecontactingDataSubjects == false || datarequesterterms[_address2].NoIntellectualPropertyClaims == false || datarequesterterms[_address2].NoUseOfAccessedResources == false)))) &&
            
            /// Cost on Use
            ((objects2[_address1].CostOnUse == true && datarequesterterms[_address2].NoFeesForAccess == false) || 
            (objects2[_address1].CostOnUse == false && (datarequesterterms[_address2].NoFeesForAccess == true || datarequesterterms[_address2].NoFeesForAccess == false)))) 
            {
            return true;
        } else{
            return false;
        } 
    }
}