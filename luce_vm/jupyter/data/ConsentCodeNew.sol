    // SPDX-License-Identifier: AFL-3.0	

    pragma solidity ^0.6.2;

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
                DataSubjectAcc.push(_address1);
                DataSubjectAcc.length-1;
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
                DataRequesterAcc.push(_address2);
                DataRequesterAcc.length-1;
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
            return (DataSubjectAcc);
        }
        
        function displayDataRequesterAcc() view public returns(address[] memory) { 
            return (DataRequesterAcc);
        }
        
        // AccessData function implements the logic of compliance between the consent and purpose statement
        function AccessData (address _address1,address _address2) view public returns (bool) { 
            
            bool[4] memory accessparams;
        
            accessparams[0] = NoRestrictionCheck(objects[_address1].NoRestrictions);
            

            bool[4] memory primaryCategoryparams;

                   
            primaryCategoryparams[0] = GeneralResearchCheck([objects[_address1].OpenToGeneralResearchAndClinicalCare,
                    researchpurpose[_address2].UseForMethodsDevelopment, 
                    researchpurpose[_address2].UseForReferenceOrControlMaterial, 
                    researchpurpose[_address2].UseForHMBResearch,
                    researchpurpose[_address2].UseForPopulationsResearch,
                    researchpurpose[_address2].UseForAncestryResearch, 
                    person[_address2].UseByAcademicProfessionals]);
            
            
            primaryCategoryparams[1] = HMBResearchCheck([objects[_address1].OpenToHMBResearch,
                        hmbresearchpurpose[_address2].UseForFundamentalBioResearch, 
                        hmbresearchpurpose[_address2].UseForGeneticsResearch, 
                        hmbresearchpurpose[_address2].UseForDrugDevelopmentResearch, 
                        hmbresearchpurpose[_address2].UseForAnyDiseaseResearch, 
                        hmbresearchpurpose[_address2].UseForAgeCategoriesResearch, 
                        hmbresearchpurpose[_address2].UseForGenderCategoriesResearch,
                        person[_address2].UseByClinicalProfessionals]);
          
            primaryCategoryparams[2] = PopulationAncestryResearchCheck([objects[_address1].OpenToPopulationAndAncestryResearch,
                        researchpurpose[_address2].UseForPopulationsResearch,
                        researchpurpose[_address2].UseForAncestryResearch, 
                        person[_address2].UseByAcademicProfessionals]);
          
            primaryCategoryparams[3] = DiseaseSpecificResearchCheck([objects[_address1].OpenToDiseaseSpecific,
                        hmbresearchpurpose[_address2].UseForAnyDiseaseResearch,
                        person[_address2].UseByClinicalProfessionals]);

            accessparams[1] = PrimaryCategoryCheck([primaryCategoryparams[0],primaryCategoryparams[1],primaryCategoryparams[2],primaryCategoryparams[3]]);
            
           
            bool[4] memory secondaryCategoryparams;

            /// Research specific restriction Block
            secondaryCategoryparams[0] = ResearchSpecificRestrictionsCheck([objects1[_address1].ResearchSpecificRestrictions,
                        researchpurpose[_address2].UseForReferenceOrControlMaterial]);
           
            
                    /// research use only Block
            secondaryCategoryparams[1] = ResearchUseOnlyCheck([objects1[_address1].OpenToResearchUseOnly,
                    researchpurpose[_address2].UseForHMBResearch]);
           
                    

                    /// Genetics study Block
            secondaryCategoryparams[2] = GeneticsStudyCheck([objects1[_address1].OpenToGeneticStudiesOnly,
                    hmbresearchpurpose[_address2].UseForGeneticsResearch]);

           
                    
                    
                    
                    /// No general method research block
            secondaryCategoryparams[3] = NoGeneralMethodCheck([objects1[_address1].NoGeneralMethodResearch,
                    researchpurpose[_address2].UseForMethodsDevelopment]); 
            
            
            accessparams[2] = SecondaryCategoryCheck([secondaryCategoryparams[0],secondaryCategoryparams[1], secondaryCategoryparams[2], secondaryCategoryparams[3]] );
            
            
           
            bool[8] memory dataProviderRequirementsparams;
            
            dataProviderRequirementsparams[0] = ProfitCheck(objects2[_address1].OpenToNonProfitUseOnly,
                        profit[_address2].UseForNonProfitPurpose, 
                        profit[_address2].UseForProfitPurpose,
                        person[_address2].UseByProfitMakingProfessionals);
                
            
            dataProviderRequirementsparams[1] =PublicationRequiredCheck(objects2[_address1].PublicationRequired,
                        datarequesterterms[_address2].NoPublicationRequired);
           
            dataProviderRequirementsparams[2] = GeographicalRestrictionCheck(objects2[_address1].GeographicSpecificRestriction,
                        geographicrestriction[_address2].UseBySpecifiedCountries);
            
            dataProviderRequirementsparams[3] = TimeLimitCheck(objects2[_address1].TimeLimitOnUse,
                    datarequesterterms[_address2].NoTimelineRestrictions);
           
            dataProviderRequirementsparams[4] = CollaborationRequiredCheck(objects2[_address1].CollaborationRequired,
                    datarequesterterms[_address2].NoCollaborationRequired);
            
            dataProviderRequirementsparams[5] = EthicsApprovalCheck(objects2[_address1].EthicsApprovalrequired,
                    datarequesterterms[_address2].NoFormalApprovalRequired);
            
            dataProviderRequirementsparams[6] = DataSecurityCheck(objects2[_address1].DataSecurityMeasuresRequired,
                    datarequesterterms[_address2].NoDataSecurityMeasures,
                    datarequesterterms[_address2].NoDataDestructionRequired,
                    datarequesterterms[_address2].NoLinkingOfAccessedRecords,
                    datarequesterterms[_address2].NoRecontactingDataSubjects,
                    datarequesterterms[_address2].NoIntellectualPropertyClaims,
                    datarequesterterms[_address2].NoUseOfAccessedResources);
            
            dataProviderRequirementsparams[7] = CostOfUseCheck(objects2[_address1].CostOnUse,
                    datarequesterterms[_address2].NoFeesForAccess);
            
            
            
            accessparams[3] =  DataProviderRequirementsCheck([dataProviderRequirementsparams[0],dataProviderRequirementsparams[1],dataProviderRequirementsparams[2],dataProviderRequirementsparams[3], dataProviderRequirementsparams[4],dataProviderRequirementsparams[5],dataProviderRequirementsparams[6],dataProviderRequirementsparams[7]]);
            
            
            return AccessCheck([accessparams[0],accessparams[1], accessparams[2], accessparams[3]]); 
                
        }

        function AccessCheck(bool[4] memory params) pure public returns(bool){
            if(params[0])
            {return true;}
            else if(params[1] && params[2] && params[3])
            {return true;}
            else
            {return false;}
        }

        function PrimaryCategoryCheck(bool[4]memory params) pure public returns(bool){
            if(params[0] || params[1] || params[2] || params[3])
            {return true;}
            else
            {return false;}
        }

        function SecondaryCategoryCheck(bool[4] memory params) pure public returns(bool){
                if(params[0] && params[1] && params[2] && params[3])
                {return true;}
                else
                {return false;}
        }

        function DataProviderRequirementsCheck(bool[8] memory params) pure public returns(bool){
                if(params[0] && params[1] && params[2] && params[3] && params[4] && params[5] && params[6] && params[7])
                {return true;}
                else
                {return false;}
        }

        function NoRestrictionCheck(bool noRestriction) pure public returns(bool){
            return noRestriction;
        }

        function GeneralResearchCheck(bool[7] memory params) pure public returns(bool){
                if((params[0] == true && 
                (params[1]== true || 
                params[2] == true || 
                params[3] == false ||
                params[4] == true ||
                params[5] == true) || params[6]==true))
                {return true;}
                else
                {return false;}
        }

        function HMBResearchCheck(bool[8] memory params) pure public returns(bool){
            if(params[0] == true 
                && 
                (params[1] == true || params[2] == true || params[3] == true || params[4] == false || params[5] == true || params[6] == true) 
                || 
                params[7]==true)
                {return true;}
                else
                {return false;}
        }

        function PopulationAncestryResearchCheck(bool[4] memory params) pure public returns(bool){
            if(params[0] == true 
                && 
                (params[1] == true || params[2] == true) 
                ||
                params[3]==true)
                {return true;}
                else
                {return false;}
        }

        function DiseaseSpecificResearchCheck(bool[3] memory params) pure public returns(bool){
            if(params[0] == true &&(params[1] == true) || params[2]==true)
            {return true;}
            else
            {return false;}
        }

        function ResearchSpecificRestrictionsCheck(bool[2] memory params) pure public returns(bool){
            if((params[0] == true && params[1]== false) 
            || 
            (params[0] == false && (params[1]== true || params[1]== false)))
            {return true;}
            else
            {return false;}
        }

        function ResearchUseOnlyCheck(bool[2] memory params) pure public returns(bool){
            if((params[0] == true && params[1] == false) 
            ||
            (params[0] == false && (params[1] == true || params[1] == false)))
            {return true;}
            else
            {return false;}
        }

        function GeneticsStudyCheck(bool[2] memory params) pure public returns(bool){
            if((params[0]==true && params[1] == true) 
            ||
            (params[0]==false && (params[1] == false || params[1] == true)))
            {return true;}
            else 
            {return false;}
        }

        function NoGeneralMethodCheck(bool[2] memory params) pure public returns(bool){
            if((params[0]==true && params[1] == false) 
            ||
            (params[0]==false && (params[1] == true || params[1] == false)))
            {return true;}
            else
            {return false;}
        }

        function ProfitCheck(bool OpenToNonProfitUseOnly, bool UseForNonProfitPurpose, bool UseForProfitPurpose, bool UseByProfitMakingProfessionals) pure public returns(bool){
            if((OpenToNonProfitUseOnly == true && (UseForNonProfitPurpose == true && UseForProfitPurpose == false && UseByProfitMakingProfessionals == false)) 
            || 
            (OpenToNonProfitUseOnly == false && (UseForNonProfitPurpose == false || UseForNonProfitPurpose == true || UseForProfitPurpose == true || UseForProfitPurpose == false || UseByProfitMakingProfessionals == true || UseByProfitMakingProfessionals == false)))
            {return true;}
            else
            {return false;}  
        }

        function PublicationRequiredCheck(bool PublicationRequired, bool NoPublicationRequired) pure public returns(bool){
            if((PublicationRequired == true && NoPublicationRequired == false) 
            ||
            (PublicationRequired == false && (NoPublicationRequired == true || NoPublicationRequired == false)))
            {return true;}
            else
            {return false;}
        }

        function GeographicalRestrictionCheck(bool GeographicSpecificRestriction_, bool UseBySpecifiedCountries) pure public returns(bool){
            if((GeographicSpecificRestriction_ == true && UseBySpecifiedCountries == true) 
            ||
            (GeographicSpecificRestriction_ == false && (UseBySpecifiedCountries == false || UseBySpecifiedCountries == true)))
            {return true;}
            else
            {return false;}
        }

        function TimeLimitCheck(bool TimeLimitOnUse, bool NoTimelineRestrictions) pure public returns(bool){
            if((TimeLimitOnUse == true && NoTimelineRestrictions == false) 
            ||
            (TimeLimitOnUse == false && (NoTimelineRestrictions == true || NoTimelineRestrictions == false)))
            {return true;}
            else
            {return true;}
        }

        function CollaborationRequiredCheck(bool CollaborationRequired, bool NoCollaborationRequired) pure public returns(bool){
            if((CollaborationRequired == true && NoCollaborationRequired == false) 
            ||
            (CollaborationRequired == false && (NoCollaborationRequired == true || NoCollaborationRequired == false)))
            {return true;}
            else 
            {return false;}
        }

        function EthicsApprovalCheck(bool EthicsApprovalrequired, bool NoFormalApprovalRequired) pure public returns(bool){
            if((EthicsApprovalrequired == true && NoFormalApprovalRequired == false) 
            ||
            (EthicsApprovalrequired == false && (NoFormalApprovalRequired == true || NoFormalApprovalRequired == false)))
            {return true;}
            else
            {return false;}
        }

        function DataSecurityCheck(bool DataSecurityMeasuresRequired , bool NoDataSecurityMeasures, bool NoDataDestructionRequired, bool NoLinkingOfAccessedRecords, bool NoRecontactingDataSubjects, bool NoIntellectualPropertyClaims, bool NoUseOfAccessedResources) pure public returns(bool){
            if((DataSecurityMeasuresRequired == true && NoDataSecurityMeasures == false  && NoDataDestructionRequired == false && NoLinkingOfAccessedRecords == false && NoRecontactingDataSubjects == false && NoIntellectualPropertyClaims == false && NoUseOfAccessedResources == false) 
            ||
                (DataSecurityMeasuresRequired == false 
                && 
                ((NoDataSecurityMeasures == true  || NoDataDestructionRequired == true || NoLinkingOfAccessedRecords == true || NoRecontactingDataSubjects == true || NoIntellectualPropertyClaims == true || NoUseOfAccessedResources == true) || (NoDataSecurityMeasures == false  || NoDataDestructionRequired == false || NoLinkingOfAccessedRecords == false || NoRecontactingDataSubjects == false || NoIntellectualPropertyClaims == false || NoUseOfAccessedResources == false))))
            {return true;}
            else
            {return false;}
        }

        function CostOfUseCheck(bool CostOnUse, bool NoFeesForAccess) pure public returns(bool){
            if((CostOnUse == true && NoFeesForAccess == false) 
            || 
            (CostOnUse == false && (NoFeesForAccess == true || NoFeesForAccess == false)))
            {return true;}
        }

        
            

        
                
        

    }
