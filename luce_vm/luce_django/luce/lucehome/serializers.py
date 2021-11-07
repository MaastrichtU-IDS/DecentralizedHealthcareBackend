from accounts.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender","age", "user_type", "ethereum_public_key"]
 
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email", "gender", "age", "password", "user_type", "ethereum_public_key", "ethereum_private_key"]
    
    #override create method because the authomatic token authentication fails 
    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data.get("password"))
        user = super(UserSerializer, self).create(validated_data)
        return user
  
#This serializer purpose is to validate the contract deployer API route
class ContractSerializer(serializers.Serializer):
    user_type = serializers.IntegerField()
    def validate(self, data):
        return data




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