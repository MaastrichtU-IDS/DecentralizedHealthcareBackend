pragma solidity ^0.4.25;

contract LinkedList{
    
  // data subjects... this is the only part the data subject // will have to fill in regarding his consent

struct Object{
    bytes32 address1;
    bool OpenToGeneralResearch; 
    bool OpenToHMBResearch; 
    bool OpenForClinicalPurpose; 
    bool OpenToProfit;
}

// ======== What follows are the structs and the mappings for the // data requesters purpose statements =======
// === DATA REQUESTER STRUCT ===

struct HMBResearchPurpose { 
    bytes32 address2;
    bool FundamentalBio;
    bool Genetics;
    bool DrugDevelopment; 
    bool AnyDisease;
    bool AgeCategories;
}

// data requesters general research purpose // 

struct ResearchPurpose{
    bytes32 address2;
    bool MethodsDevelopment;
    bool ReferenceOrControlMaterial; 
    bool Populations;
    bool Ancestry;
}

// date requesters clinical purposes // 

struct ClinicalPurpose{
    bytes32 address2; 
    bool DecisionSupport; 
    bool DiseaseSupport;
}

struct Person{ 
    bytes32 address2; 
    bool Academic;
    bool Clinical;
    bool ProfitMaking; 
    bool NonProfessional;
}

mapping (bytes32 => Object) objects; // data subject
mapping (bytes32 => ResearchPurpose) researchpurpose; // data requester 
mapping (bytes32 => HMBResearchPurpose) hmbresearchpurpose; 
mapping (bytes32 => ClinicalPurpose) clinicalpurpose;
mapping (bytes32 => Person) person;

bytes32[] DataSubjectAcc; 
bytes32[] DataRequesterAcc;

// This is the part for the data subject // 

function UploadData(
    bytes32 _address1,
    bool _OpenToGeneralResearch, 
    bool _OpenToHMBResearch, 
    bool _OpenForClinicalPurpose, 
    bool _OpenToProfit
)

public {
    objects[_address1].OpenToGeneralResearch = _OpenToGeneralResearch; 
    objects[_address1].OpenToHMBResearch = _OpenToHMBResearch; 
    objects[_address1].OpenForClinicalPurpose = _OpenForClinicalPurpose; 
    objects[_address1].OpenToProfit = _OpenToProfit;

    DataSubjectAcc.push(_address1)-1; 
}

// +++ function is done +++

// ==== FUNCTION FOR THE DATA REQUESTER === //

function giveResearchPurpose( 
    bytes32 _address2,
    bool _MethodsDevelopment,
    bool _ReferenceOrControlMaterial, 
    bool _Populations,
    bool _Ancestry )

public {
    researchpurpose[_address2].MethodsDevelopment = _MethodsDevelopment;
    researchpurpose[_address2].ReferenceOrControlMaterial = _ReferenceOrControlMaterial;
    researchpurpose[_address2].Populations = _Populations; 
    researchpurpose[_address2].Ancestry = _Ancestry; 
    DataRequesterAcc.push(_address2) -1;
}

function giveHMBPurpose( 
    bytes32 _address2,
    bool _FundamentalBio, 
    bool _Genetics,
    bool _DrugDevelopment, 
    bool _AnyDisease,
    bool _AgeCategories
) 

public {
    hmbresearchpurpose[_address2].FundamentalBio = _FundamentalBio; 
    hmbresearchpurpose[_address2].Genetics = _Genetics; 
    hmbresearchpurpose[_address2].DrugDevelopment = _DrugDevelopment; 
    hmbresearchpurpose[_address2].AnyDisease = _AnyDisease; 
    hmbresearchpurpose[_address2].AgeCategories = _AgeCategories;
}

function giveClinicalPurpose( 
    bytes32 _address2,
    bool _DecisionSupport,
    bool _DiseaseSupport)

public {
    clinicalpurpose[_address2].DecisionSupport = _DecisionSupport; 
    clinicalpurpose[_address2].DiseaseSupport = _DiseaseSupport;
}

function givePerson( 
    bytes32 _address2, 
    bool _Academic,
    bool _Clinical,
    bool _ProfitMaking, 
    bool _NonProfessional)

public {
    person[_address2].Academic = _Academic; 
    person[_address2].Clinical = _Clinical; 
    person[_address2].ProfitMaking = _ProfitMaking; 
    person[_address2].NonProfessional = _NonProfessional;
}

function displayDataSubjectAcc() view public returns(bytes32[] memory) { 
    return DataSubjectAcc;
}

function displayDataREquesterAcc() view public returns(bytes32[] memory) { 
    return DataRequesterAcc;
}


function getDataInfo(bytes32 _address1) view public returns(bool,bool,bool,bool) {
    return( 
        objects[_address1].OpenToGeneralResearch, 
        objects[_address1].OpenToHMBResearch, 
        objects[_address1].OpenForClinicalPurpose, 
        objects[_address1].OpenToProfit
        );
}

function getHMBpurpose(bytes32 _address1) view public returns(bool,bool,bool,bool,bool) {
    return (
        hmbresearchpurpose[_address1].FundamentalBio, 
        hmbresearchpurpose[_address1].Genetics, 
        hmbresearchpurpose[_address1].DrugDevelopment, 
        hmbresearchpurpose[_address1].AnyDisease, 
        hmbresearchpurpose[_address1].AgeCategories
        ); 
}

function AccessData (bytes32 _address1, bytes32 _address2) view public returns (bool) { 
    if(
    objects[_address1].OpenToGeneralResearch == true && 
    (researchpurpose[_address2].MethodsDevelopment == true || 
    researchpurpose[_address2].ReferenceOrControlMaterial == true ||
    researchpurpose[_address2].Populations == true || 
    researchpurpose[_address2].Ancestry == true) && 
    (person[_address2].Academic==true)
    ||
    objects[_address1].OpenToHMBResearch == true && 
    (hmbresearchpurpose[_address2].FundamentalBio == true || 
    hmbresearchpurpose[_address2].Genetics == true || 
    hmbresearchpurpose[_address2].DrugDevelopment == true || 
    hmbresearchpurpose[_address2].AnyDisease == true || 
    hmbresearchpurpose[_address2].AgeCategories == true) && 
    (person[_address2].Academic==true)
    ||
    objects[_address1].OpenForClinicalPurpose == true && 
    (clinicalpurpose[_address2].DecisionSupport == true || 
    clinicalpurpose[_address2].DiseaseSupport) && 
    (person[_address2].Clinical==true)
    ||
    objects[_address1].OpenToProfit == true && 
    (person[_address2].ProfitMaking == true)
    ||
    objects[_address1].OpenToProfit == false && 
    (person[_address2].ProfitMaking == false)
    )

    {return true;}

else
    {if (
    (objects[_address1].OpenToGeneralResearch == true && 
    researchpurpose[_address2].MethodsDevelopment == false && 
    researchpurpose[_address2].ReferenceOrControlMaterial == false && 
    researchpurpose[_address2].Populations == false && 
    researchpurpose[_address2].Ancestry == false)
    ||
    objects[_address1].OpenToHMBResearch == false || 
    objects[_address1].OpenForClinicalPurpose == false || 
    (objects[_address1].OpenToProfit == false &&
    person[_address2].ProfitMaking == true &&
    person[_address2].ProfitMaking == true) )
    return false;} 
}
}