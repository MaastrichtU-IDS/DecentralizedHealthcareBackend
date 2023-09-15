from pyexpat import model
from accounts.models import *
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import utils.custom_exeptions as custom_exeptions
from rest_framework.response import Response

from blockchain.models import *


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "gender", "age",
            "user_type", "ethereum_public_key", "country", "institution"
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "first_name", "last_name", "email", "gender", "age",
            "password", "user_type", "ethereum_public_key",
            "ethereum_private_key", "country", "institution"
        ]

    #override create method because the authomatic token authentication fails
    def create(self, validated_data):

        validated_data["password"] = make_password(
            validated_data.get("password"))
        instance = super(UserSerializer, self).create(validated_data)

        return instance

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name',
                                                 instance.first_name)
        instance.last_name = validated_data.get('last_name',
                                                instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.age = validated_data.get('age', instance.age)
        instance.country = validated_data.get('country', instance.country)
        instance.institution = validated_data.get('institution',
                                                  instance.institution)

        instance.password = validated_data.get(
            'password', instance.password)  #TODO: change password check.
        instance.user_type = validated_data.get(
            'user_type', instance.user_type)  #TODO: is this changable?
        instance.save()
        return instance

    def validate(self, data):
        return data