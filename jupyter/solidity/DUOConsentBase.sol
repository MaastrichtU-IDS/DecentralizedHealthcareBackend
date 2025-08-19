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

    struct DUO_Extension {
        uint32[] UserSpecificRestriction;
        uint32[] ProjectSpecificRestriction;
        uint32[] InstitutionSpecificRestriction;
    }

    mapping(address => DUO) provider_mapping;
    mapping(address => DUO) requester_mapping;

    mapping(address => DUO_Extension) provider_extension_mapping;
    mapping(address => DUO_Extension) requester_extension_mapping;

    function uploadPurpose(
        uint8 role,
        address _address1,
        DUO memory purpose
    ) public {
        if (role == ROLE_PROVIDER) {
            provider_mapping[_address1] = purpose;
        } else if (role == ROLE_REQUESTER) {
            requester_mapping[_address1] = purpose;
        }
    }

    function GetPurposeItems(
        uint8 role,
        address _address
    ) public view returns (DUO memory) {
        if (role == ROLE_PROVIDER) {
            return provider_mapping[_address];
        } else if (role == ROLE_REQUESTER) {
            return requester_mapping[_address];
        }
    }

    function upload_extension(
        uint8 role,
        address _address1,
        DUO_Extension memory extension
    ) public {
        if (role == ROLE_PROVIDER) {
            provider_extension_mapping[_address1] = extension;
        } else if (role == ROLE_REQUESTER) {
            requester_extension_mapping[_address1] = extension;
        }
    }

    function check_users(
        address provider_address,
        address requester_address
    ) private view returns (bool) {
        DUO_Extension memory provider_extension = provider_extension_mapping[
            provider_address
        ];
        DUO_Extension memory requester_extension = requester_extension_mapping[
            requester_address
        ];

        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (
            uint256 j = 0;
            j < requester_extension.UserSpecificRestriction.length;
            j++
        ) {
            tmp_requester = requester_extension.UserSpecificRestriction[j];
            for (
                uint256 i = 0;
                i < provider_extension.UserSpecificRestriction.length;
                i++
            ) {
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
        DUO_Extension memory provider_extension = provider_extension_mapping[
            provider_address
        ];
        DUO_Extension memory requester_extension = requester_extension_mapping[
            requester_address
        ];

        // Check if the provider's extension is empty
        if (
            provider_extension.UserSpecificRestriction.length == 0 &&
            provider_extension.InstitutionSpecificRestriction.length == 0 &&
            provider_extension.ProjectSpecificRestriction.length == 0
        ) {
            return true; // No restrictions, access granted
        }
        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (
            uint256 j = 0;
            j < requester_extension.UserSpecificRestriction.length;
            j++
        ) {
            tmp_requester = requester_extension.UserSpecificRestriction[j];
            for (
                uint256 i = 0;
                i < provider_extension.InstitutionSpecificRestriction.length;
                i++
            ) {
                tmp_provider = provider_extension
                    .InstitutionSpecificRestriction[i];
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
        DUO_Extension memory provider_extension = provider_extension_mapping[
            provider_address
        ];
        DUO_Extension memory requester_extension = requester_extension_mapping[
            requester_address
        ];

        uint32 tmp_provider = 0;
        uint32 tmp_requester = 0;
        bool flag = false;

        for (
            uint256 j = 0;
            j < requester_extension.UserSpecificRestriction.length;
            j++
        ) {
            tmp_requester = requester_extension.UserSpecificRestriction[j];
            for (
                uint256 i = 0;
                i < provider_extension.ProjectSpecificRestriction.length;
                i++
            ) {
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
    //     provider_mapping[_address1] = purpose;
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

    function basic_access_check(
        address provider_address,
        address requester_address
    ) private view returns (uint32) {
        DUO memory provider = provider_mapping[provider_address];
        DUO memory requester = requester_mapping[requester_address];

        if (provider.NoRestriction == true) {
            return 0;
        }

        uint32 result = 0;
        uint32 u1 = 1;

        if (provider.GeneralResearch == true) {
            if (requester.GeneralResearch == false) {
                result += u1 << uint32(RESULT_CODE.GeneralResearch);
            }
        }
        if (provider.ClinicalCare == true) {
            if (requester.ClinicalCare == false) {
                result += u1 << uint32(RESULT_CODE.ClinicalCare);
            }
        }

        if (provider.HMBResearch == true) {
            if (requester.HMBResearch == false) {
                result += u1 << uint32(RESULT_CODE.HMBResearch);
            }
        }

        if (provider.populationAndAncestryResearchOnly == true) {
            if (requester.populationAndAncestryResearchOnly == false) {
                result +=
                    u1 <<
                    uint32(RESULT_CODE.PopulationAndAncestryResearchOnly);
            }
        }

        if (provider.populationAndAncestryResearchNon == true) {
            if (requester.populationAndAncestryResearchNon == false) {
                result +=
                    u1 <<
                    uint32(RESULT_CODE.PopulationAndAncestryResearchNon);
            }
        }

        if (provider.ResearchSpecificRestriction == true) {
            if (requester.ReturnToResource == false) {
                result += u1 << uint32(RESULT_CODE.ResearchSpecificRestriction);
            }
        }

        if (provider.UserSpecificRestriction == true) {
            if (
                requester.UserSpecificRestriction == false ||
                check_users(provider_address, requester_address) == false
            ) {
                result += u1 << uint32(RESULT_CODE.UserSpecificRestriction);
            }
        }

        if (provider.ProjectSpecificRestriction == true) {
            if (
                requester.ProjectSpecificRestriction == false ||
                check_project(provider_address, requester_address) == false
            ) {
                result += u1 << uint32(RESULT_CODE.ProjectSpecificRestriction);
            }
        }

        if (provider.InstitutionSpecificRestriction == true) {
            if (
                requester.InstitutionSpecificRestriction == false ||
                check_institution(provider_address, requester_address) == false
            ) {
                result +=
                    u1 <<
                    uint32(RESULT_CODE.InstitutionSpecificRestriction);
            }
        }

        if (provider.GeneticStudiesOnly == true) {
            if (requester.GeneticStudiesOnly == false) {
                result += u1 << uint32(RESULT_CODE.GeneticStudiesOnly);
            }
        }

        if (provider.NonGeneralMethodResearch == true) {
            if (requester.NonGeneralMethodResearch == true) {
                result += u1 << uint32(RESULT_CODE.NonGeneralMethodResearch);
            }
        }

        if (provider.NonProfitUseOnly == true) {
            if (
                requester.NonProfitUseOnly == false ||
                requester.NonCommercialUseOnly == true
            ) {
                result += u1 << uint32(RESULT_CODE.NonProfitUseOnly);
            }
        }

        if (provider.NonCommercialUseOnly == true) {
            if (requester.NonCommercialUseOnly == true) {
                result += u1 << uint32(RESULT_CODE.NonCommercialUseOnly);
            }
        }

        if (provider.PublicationRequired == true) {
            if (requester.PublicationRequired == false) {
                result += u1 << uint32(RESULT_CODE.PublicationRequired);
            }
        }

        if (provider.PublicationMoratorium == true) {
            if (requester.PublicationMoratorium == false) {
                result += u1 << uint32(RESULT_CODE.PublicationMoratorium);
            }
        }

        if (provider.CollaborationRequired == true) {
            if (requester.CollaborationRequired == false) {
                result += u1 << uint32(RESULT_CODE.CollaborationRequired);
            }
        }

        if (provider.EthicsApprovalrequired == true) {
            if (requester.EthicsApprovalrequired == false) {
                result += u1 << uint32(RESULT_CODE.EthicsApprovalRequired);
            }
        }

        if (provider.ReturnToResource == true) {
            if (requester.ReturnToResource == false) {
                result += u1 << uint32(RESULT_CODE.ReturnToResource);
            }
        }

        if (provider.DataUsePermission == true) {
            if (requester.DataUsePermission == false) {
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

    function access_data(
        address provider_address,
        address requester_address
    ) public view returns (uint32) {
        DUO memory provider = provider_mapping[provider_address];
        DUO memory requester = requester_mapping[requester_address];

        if (provider.NoRestriction == true) {
            return 0;
        }

        uint32 result = basic_access_check(provider_address, requester_address);
        if (result != 0) {
            return result;
        }
        uint32 u1 = 1;

        if (provider.GeographicSpecific) {
            if (
                !requester.GeographicSpecific ||
                !CheckArea(provider_address, requester_address)
            ) {
                result += u1 << uint32(RESULT_CODE.GeographicSpecific);
            }
        }

        if (provider.DiseaseSpecific) {
            if (
                !requester.DiseaseSpecific ||
                !CheckDisease(provider_address, requester_address)
            ) {
                result += u1 << uint32(RESULT_CODE.DiseaseSpecific);
            }
        }

        if (provider.TimeLimitOnUse) {
            if (
                !requester.TimeLimitOnUse ||
                !CheckDate(provider_address, requester_address)
            ) {
                result += u1 << uint32(RESULT_CODE.TimeLimitOnUse);
            }
        }
        return result;
    }
}
