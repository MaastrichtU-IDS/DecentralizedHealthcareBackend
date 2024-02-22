from pyexpat import model
from accounts.models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import utils.custom_exeptions as custom_exeptions
from rest_framework.response import Response

from blockchain.models import *
# from blockchain.models import PrimaryCategoty


class RestrictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrictions
        fields = [
            "id", "no_restrictions",
            "open_to_general_research_and_clinical_care",
            "open_to_HMB_research", "open_to_population_and_ancestry_research",
            "open_to_disease_specific"
        ]


class PrimaryCategotySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrimaryCategory
        fields = [
            "no_restrictions", "open_to_general_research_and_clinical_care",
            "open_to_HMB_research", "open_to_population_and_ancestry_research",
            "open_to_disease_specific"
        ]


class SecondaryCategotySerializer(serializers.ModelSerializer):
    class Meta:
        model = SecondaryCategory
        fields = [
            "open_to_genetic_studies", "research_specific_restrictions",
            "open_to_research_use_only", "no_general_method_research"
        ]


class RequirementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Requirements
        fields = [
            "geographic_specific_restriction", "open_to_non_profit_use_only",
            "publication_required", "collaboration_required",
            "ethics_approval_required", "time_limit_on_use", "cost_on_use",
            "data_security_measures_required"
        ]


class GeneralResearchPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneralResearchPurpose
        fields = [
            "use_for_methods_development",
            "use_for_reference_or_control_material",
            "use_for_research_concerning_populations",
            "use_for_research_ancestry", "use_for_biomedical_research"
        ]


class HMBResearchPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = HMBResearchPurpose
        fields = [
            "use_for_research_concerning_fundamental_biology",
            "use_for_research_concerning_genetics",
            "use_for_research_concerning_drug_development",
            "use_for_research_concerning_any_disease",
            "use_for_research_concerning_age_categories",
            "use_for_research_concerning_gender_categories"
        ]


class ClinicalPurposeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalPurpose
        fields = ["use_for_decision_support", "use_for_disease_support"]


class ResearchPurposeSerializer(serializers.ModelSerializer):
    general_research_purpose = GeneralResearchPurposeSerializer()
    HMB_research_purpose = HMBResearchPurposeSerializer()
    clinical_purpose = ClinicalPurposeSerializer()

    class Meta:
        model = ResearchPurpose
        fields = [
            "general_research_purpose", "HMB_research_purpose",
            "clinical_purpose"
        ]

    def create(self, validated_data):
        # print(0.5)
        general_research_purpose = validated_data.get(
            "general_research_purpose", {})
        HMB_research_purpose = validated_data.get("HMB_research_purpose", {})
        clinical_purpose = validated_data.get("clinical_purpose", {})

        GRP_serializer = GeneralResearchPurposeSerializer(
            data=general_research_purpose)
        if not GRP_serializer.is_valid():
            return custom_exeptions.validation_exeption(GRP_serializer)
        GRP_purpose = GRP_serializer.save()

        HMB_serializer = HMBResearchPurposeSerializer(
            data=HMB_research_purpose)
        if not HMB_serializer.is_valid():
            return custom_exeptions.validation_exeption(HMB_serializer)
        HMB_purpose = HMB_serializer.save()

        clinical_serializer = ClinicalPurposeSerializer(data=clinical_purpose)
        if not clinical_serializer.is_valid():
            custom_exeptions.validation_exeption(clinical_serializer)
            return custom_exeptions.validation_exeption(clinical_serializer)
        clinical_purpose_obj = clinical_serializer.save()

        rp = ResearchPurpose.objects.create(
            general_research_purpose=GRP_purpose,
            HMB_research_purpose=HMB_purpose,
            clinical_purpose=clinical_purpose_obj)

        return rp


class ConsentContractSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    restrictions = RestrictionsSerializer()
    DEPLOYMENT_COST = 53000

    class Meta:
        model = ConsentContract
        fields = ["contract_address", "user_id", "restrictions"]

    def create(self, validated_data):
        user = self.context.get("user")
        estimate = self.context.get("estimate", False)
        restrictions = RestrictionsSerializer(
            data=self.context.get("restrictions"))
        if (not restrictions.is_valid()):
            raise serializers.ValidationError(restrictions.errors)
        restriction = restrictions.save()

        consentContract = ConsentContract.objects.create(
            user=user, restrictions=restriction)
        return consentContract


#TODO: change validation to restrict the creation of the contract
class RegestryContractSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    estimated_gas = 53000

    class Meta:
        model = LuceRegistryContract
        fields = ["user_id", "contract_address"]


class DataContractSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    consent_contract = ConsentContractSerializer()
    DEPLOYMENT_COST = 53000

    class Meta:
        model = DataContract
        fields = [
            "id", "user", "description", "licence", "contract_address",
            "consent_contract"
        ]

    def validate(self, data):
        user = self.context.get("user")
        if user.ethereum_public_key is None or user.ethereum_private_key is None:
            raise serializers.ValidationError(
                {"error": "user must connect a wallet first"})
        return data

    def create(self, validated_data):
        user = self.context.get("user")
        estimate = self.context.get("estimate", False)
        description = validated_data.get("description", "")

        dataContract = DataContract.objects.create(user=user)
        conset_serializer = ConsentContractSerializer(data=validated_data,
                                                      context=self.context,
                                                      partial=True)

        if not conset_serializer.is_valid():
            raise serializers.ValidationError(conset_serializer.errors)
        consentContract = conset_serializer.save()

        dataContract.description = description

        dataContract.consent_contract = consentContract

        dataContract.save()

        return dataContract
