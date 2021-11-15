from accounts.models import User, ConsentContract, Restrictions
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from utils.web3_scripts import *

class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender","age", "user_type", "ethereum_public_key"]
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender", "age", "password", "user_type", "ethereum_public_key", "ethereum_private_key"]
    
    def address_get_or_create(self, instance, validated_data):
        createWallet = self.context.get("create_wallet")
        if(createWallet):
            account = assign_address_v3()
            instance.ethereum_public_key = account.address
            instance.ethereum_private_key = account.privateKey.hex()

        else: #otherwise if a key is specified use that one
            instance.ethereum_public_key = validated_data.get('ethereum_public_public', instance.ethereum_public_key)
            instance.ethereum_private_key = validated_data.get('ethereum_private_key', instance.ethereum_private_key)
        return instance
        
     #override create method because the authomatic token authentication fails 
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        instance = super(UserSerializer, self).create(validated_data)
        self.address_get_or_create(instance, validated_data)

        return instance

        
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)

        instance.password = validated_data.get('password',instance.password) #TODO: change password check.
        instance.user_type = validated_data.get('user_type', instance.user_type) #TODO: is this changable?
        self.address_get_or_create(instance, validated_data)
        instance.save()
        return instance


class RestrictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restrictions
        fields = ["id", "no_restrictions", "open_to_general_research_and_clinical_care", "open_to_HMB_research", "open_to_population_and_ancestry_research", "open_to_disease_specific"]

    def validate(self, data):
        required_restrictions = ["no_restrictions","open_to_general_research_and_clinical_care","open_to_HMB_research","open_to_population_and_ancestry_research","open_to_disease_specific"]
        restrictions = data
      
        if(self.restrictions_validator(restrictions)):
            raise serializers.ValidationError("restrictions selected are ambiguous")
        return data
   

    def restrictions_validator(self, restrictions):
        if(restrictions["no_restrictions"] and
        (
        not restrictions["open_to_general_research_and_clinical_care"] or
        not restrictions["open_to_HMB_research"] or 
        not restrictions["open_to_population_and_ancestry_research"] or
        not restrictions["open_to_disease_specific"]
        )):
            return True
        return False
    

class ConsentContractSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    restrictions_id = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = ConsentContract
        fields = ["contract_address", "user_id", "restrictions_id"]


    def create(self, validated_data):        
        user = self.context.get("user")
        tx_receipt = deploy_contract_v3(user)
        restrictions = RestrictionsSerializer(data = self.context.get("restrictions"))
        if (not restrictions.is_valid()):
            raise serializers.ValidationError(restrictions.errors)
        restriction = restrictions.save()
        consentContract = ConsentContract.objects.create(user = user, restrictions = restriction, contract_address=tx_receipt.contractAddress)
        upload_data(consentContract, restriction, user)
        return consentContract



"""
class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","contract_address", "email", "ethereum_public_key", "first_name", "last_name", "user_type"]

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email""contract_address", "email", "ethereum_public_key", "ethereum_private_key", "password", "first_name", "last_name", "user_type"]

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(UserSerializer, self).create(validated_data)
        return user

    def validate(self, data):
        return data
#This serializer purpose is to validate the contract deployer API route
class ContractSerializer(serializers.Serializer):
    user_type = serializers.IntegerField()
    def validate(self, data):
        return data

class CauseSerializer(serializers.ModelSerializer):
    creator = PublicUserSerializer(read_only=True)

    class Meta: 
        model = Cause
        fields = ["id", "title", "description", "ethereum_public_key", "ethereum_private_key", "goal", "percentBPS","creator"]

    def create(self, validated_data):
        user = self.context["request"].user
        cause = Cause.objects.create( creator = user,  **validated_data)
        return cause
    def validate(self,data):
        user = self.context["request"].user
        user_serializer = PublicUserSerializer(user)
        usertype = user_serializer["user_type"].value

        #only influencers can create causes
        if usertype != 0:   
            raise serializers.ValidationError({"error":"Donors cannot create causes"})
        return data

class PublicCauseSerializer(serializers.ModelSerializer):
    creator = PublicUserSerializer(read_only=True)
    class Meta:
        model = Cause
        fields =  ["id", "title", "description", "ethereum_public_key", "goal", "percentBPS","creator"]

class DonationSerializer(serializers.ModelSerializer):
    cause = serializers.PrimaryKeyRelatedField(many = False, queryset = Cause.objects.all())
    donor = serializers.PrimaryKeyRelatedField(many = False, queryset = User.objects.all())
    
    class Meta:
        model = Donation
        fields = [ "cause", "amount", "donor"]

class PublicDonationSerializer(serializers.ModelSerializer):
    cause = PublicCauseSerializer(read_only = True)
    donor = PublicUserSerializer(read_only = True)

    class Meta:
        model = Donation
        fields = ["id","cause", "amount", "donor"]

class PublicGroupInfoSerializer(serializers.ModelSerializer):
    cause = serializers.PrimaryKeyRelatedField(many = False,queryset = Cause.objects.all())
    class Meta:
        model = GroupInfo
        fields = ["cause", "split", "group"]

class PublicGroupSerializer(serializers.ModelSerializer):
    info = PublicGroupInfoSerializer(many=True, read_only=True)
    class Meta:
        model = CauseGroup
        fields = ["id",'name', 'description', 'info', "creator"]

   """