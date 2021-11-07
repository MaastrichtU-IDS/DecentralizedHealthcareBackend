pragma solidity ^0.4.25;

contract LinkedList{
    
  // data subjects... this is the only part the data subject // will have to fill in regarding his consent

struct Object{
    address address1;
    bool OpenToGeneralResearch; 
    bool OpenToHMBResearch; 
    bool OpenForClinicalPurpose; 
    bool OpenToProfit;
}

// ======== What follows are the structs and the mappings for the // data requesters purpose statements =======
// === DATA REQUESTER STRUCT ===

struct HMBResearchPurpose { 
    address address2;
    bool FundamentalBio;
    bool Genetics;
    bool DrugDevelopment; 
    bool AnyDisease;
    bool AgeCategories;
}

// data requesters general research purpose // 

struct ResearchPurpose{
    address address2;
    bool MethodsDevelopment;
    bool ReferenceOrControlMaterial; 
    bool Populations;
    bool Ancestry;
}

// date requesters clinical purposes // 

struct ClinicalPurpose{
    address address2; 
    bool DecisionSupport; 
    bool DiseaseSupport;
}

struct Person{ 
    address address2; 
    bool Academic;
    bool Clinical;
    bool ProfitMaking; 
    bool NonProfessional;
}

mapping (address => Object) objects; // data subject
mapping (address => ResearchPurpose) researchpurpose; // data requester 
mapping (address => HMBResearchPurpose) hmbresearchpurpose; 
mapping (address => ClinicalPurpose) clinicalpurpose;
mapping (address => Person) person;

address[] DataSubjectAcc; 
address[] DataRequesterAcc;

// This is the part for the data subject // 

function UploadData(
    address _address1,
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
    address _address2,
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
    address _address2,
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
    address _address2,
    bool _DecisionSupport,
    bool _DiseaseSupport)

public {
    clinicalpurpose[_address2].DecisionSupport = _DecisionSupport; 
    clinicalpurpose[_address2].DiseaseSupport = _DiseaseSupport;
}

function givePerson( 
    address _address2, 
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

function displayDataSubjectAcc() view public returns(address[] memory) { 
    return DataSubjectAcc;
}

function displayDataREquesterAcc() view public returns(address[] memory) { 
    return DataRequesterAcc;
}


function getDataInfo(address _address1) view public returns(bool,bool,bool,bool) {
    return( 
        objects[_address1].OpenToGeneralResearch, 
        objects[_address1].OpenToHMBResearch, 
        objects[_address1].OpenForClinicalPurpose, 
        objects[_address1].OpenToProfit
        );
}

function getHMBpurpose(address _address1) view public returns(bool,bool,bool,bool,bool) {
    return (
        hmbresearchpurpose[_address1].FundamentalBio, 
        hmbresearchpurpose[_address1].Genetics, 
        hmbresearchpurpose[_address1].DrugDevelopment, 
        hmbresearchpurpose[_address1].AnyDisease, 
        hmbresearchpurpose[_address1].AgeCategories
        ); 
}

function AccessData (address _address1, address _address2) view public returns (bool) { 
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