from rest_framework.views import APIView
from rest_framework import permissions, parsers, renderers, status
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from utils.utils import get_initial_response
from utils import custom_exeptions

from .serializers import UserSerializer, PublicUserSerializer
from rest_framework.response import Response
from accounts.models import User
import logging

logger = logging.getLogger(__name__)


class UserRegistration(APIView):
    """
    Register a new user
    """

    def post(self, request, format=None):

        # Create an account for fake user
        create_wallet = request.data.get("create_wallet")
        create_wallet = True

        logger.info("Registering a new user: %s", request.data)

        serializer = UserSerializer(
            data=request.data,
            context={"create_wallet": create_wallet}
        )

        # serializer validation
        if not serializer.is_valid():
            logger.error("Registration failed: %s", serializer.errors)
            response = custom_exeptions.validation_exeption(serializer)
            return Response(response["body"], response["status"])

        instance = serializer.save()

        tx_receipt = self._address_get_or_create(instance, create_wallet)

        return Response(
            {
                "error": {
                    "code": 200,
                    "message": "registration successfull",
                    "status": "OK",
                    "details": [{"reason": "SUCCESS"}]
                },
                "data": {
                    "transaction_id": [tx_receipt.txid]
                }
            },

            status=status.HTTP_200_OK
        )

        # response = get_initial_response()
        # response["error"]["code"] = 200
        # response["error"]["message"] = "registration successfull"
        # response["error"]["status"] = "OK"
        # response["error"]["details"] = [{"reason": "SUCCESS"}]
        # response["data"]["transaction_id"] = [tx_receipt.txid]

        # return Response(response, status=status.HTTP_200_OK)

    def _address_get_or_create(self, user, create_wallet):
        if create_wallet:
            tx_receipt = user.create_wallet()
            user.save()
            return tx_receipt
        return None

    def address_get_or_create(self, instance, createWallet):
        if (createWallet):
            # User
            tx_receipt = instance.create_wallet()
            instance.save()

            if tx_receipt:
                return tx_receipt
        tx_receipt = None
        return tx_receipt


class LoginView(APIView):
    # user/login
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (
        parsers.FormParser,
        parsers.MultiPartParser,
        parsers.JSONParser,
    )
    renderer_classes = (renderers.JSONRenderer, )
    serializer_class = AuthTokenSerializer

    if coreapi_schema.is_enabled():
        schema = ManualSchema(
            fields=[
                coreapi.Field(
                    name="username",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Username",
                        description="Valid username for authentication",
                    ),
                ),
                coreapi.Field(
                    name="password",
                    required=True,
                    location='form',
                    schema=coreschema.String(
                        title="Password",
                        description="Valid password for authentication",
                    ),
                ),
            ],
            encoding="application/json",
        )

    def get_serializer_context(self):
        return {
            'request': self.request,
            'format': self.format_kwarg,
            'view': self
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        logger.info("Login information:" + str(request.data))

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            response = custom_exeptions.validation_exeption(serializer)
            return Response(response["body"], response["status"])

        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "login successfull"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["token"] = token.key

        return Response(response)


class UserUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request, format=None):
        user = self.request.user
        instance = user
        createWallet = request.data.get("create_wallet")
        serializer = UserSerializer(user,
                                    data=request.data,
                                    context={"create_wallet": createWallet},
                                    partial=True)

        if not serializer.is_valid():
            response = custom_exeptions.validation_exeption(serializer)
            return Response(response["body"], response["status"])

        tx_receipt = self.address_get_or_create(instance, createWallet)
        if type(tx_receipt) is list:
            response = custom_exeptions.blockchain_exception(tx_receipt)
            return Response(response["body"], response["status"])

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "update user successfull"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["transaction receipts"] = [tx_receipt]

        serializer.save()
        return Response(response, status=status.HTTP_200_OK)

    def address_get_or_create(self, instance, createWallet):
        if (createWallet):
            tx_receipt = instance.create_wallet()

            if tx_receipt:
                return tx_receipt
        tx_receipt = None
        return tx_receipt


class PublicUserInfoView(APIView):
    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = PublicUserSerializer(user)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"][
            "message"] = "user public data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["users"] = [serializer.data]

        return Response(response)

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404


class PrivateUserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"][
            "message"] = "user private data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["users"] = [serializer.data]
        return Response(response)


class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = PublicUserSerializer(users, many=True)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "all user data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["users"] = [serializer.data]
        return Response(response)
