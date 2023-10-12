from django.http import Http404
from rest_framework.views import APIView
from rest_framework import permissions, generics, filters, parsers, renderers, status
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from accounts.models import User
from blockchain.models import DataContract
from utils import custom_exeptions as custom_exeptions

from rest_framework.response import Response
from .serializers import *
from utils.web3_scripts import *
from utils.utils import get_initial_response, set_logger

from blockchain.models import LuceRegistryContract as LuceRegistry

from privacy.disposable_address import DisposableAddressService

logger = set_logger(__file__)


class ContractsListView(APIView):
    def get(self, request, format=None):
        contracts = DataContract.objects.all()
        serializer = DataContractSerializer(contracts, many=True)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "all user data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"]["contracts"] = serializer.data
        return Response(response)


class UploadDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_a_new_account(self):
        new_account = accounts.add()
        accounts[0].transfer(new_account, 1e18)
        return new_account

    def is_luce_registry_deployed(self):
        return LuceRegistry.objects.filter(pk=1).exists()

    def get_luce_registry(self):
        return LuceRegistry.objects.get(pk=1)

    def post(self, request, format=None):
        user = request.user
        estimate = request.data.get("estimate", False)
        link = request.data.get("link", False)

        print("###########")
        # print(request.data)
        print("request.data:\n", request.data)

        logger.info("Upload data from: " + link)

        if not link:
            response = custom_exeptions.custom_message(
                "link field is required")

            logger.error("Link field is invalid (empty?)")
            return Response(response["body"], response["status"])

        # new_account = self.get_a_new_account()
        user_account = accounts.at(user.ethereum_public_key)
        print("user_account:\n", user_account)
        user_balance = user_account.balance()
        print("user_balance:\n", user_balance)

        disposable_address_service = DisposableAddressService()
        new_account = disposable_address_service.get_a_new_address_with_balance(
            user_account, 1e15)
        # print("new_account:\n", new_account)
        balance_of_new_account = new_account.balance()
        print(f"balance_of_new_account: {balance_of_new_account}")

        user_balance = user_account.balance()
        print("user_balance after deposit:\n", user_balance)

        user.ethereum_private_key = new_account.private_key

        tx_receipts = []

        if not self.is_luce_registry_deployed():
            response = custom_exeptions.custom_message(
                "luce registry was not deployed")

            logger.error("Luce registry was not deployed!")
            return Response(response["body"], response["status"])

        luceregistry = LuceRegistry.objects.get(pk=1)

        logger.info("LUCE Registry done")

        serializer = DataContractSerializer(data=request.data,
                                            context={
                                                "estimate": estimate,
                                                "restrictions": request.data,
                                                "user": request.user
                                            },
                                            partial=True)

        print("serializer:\n", serializer)

        restriction_serializer = RestrictionsSerializer(data=request.data)
        # check that user is registered in LuceRegistry, if not register him
        is_registered = luceregistry.is_registered(request.user, "provider")

        # if not is_registered:
        #     cost = LuceRegistry.objects.get(pk=1).register_provider(
        #         user, estimate)

        #     if type(cost) is list:
        #         response = custom_exeptions.blockchain_exception(cost)
        #         return Response(response["body"], response["status"])
        #     tx_receipts.append(cost)

        if not restriction_serializer.is_valid():
            response = custom_exeptions.validation_exeption(
                restriction_serializer)
            return Response(response["body"], response["status"])

        if not serializer.is_valid():
            response = custom_exeptions.validation_exeption(serializer)
            return Response(response["body"], response["status"])

        datacontract = serializer.save()

        print("datacontract licence:\n", datacontract.licence)
        # print("###########")
        logger.info("Start to deploy ConsentCode smart contract")
        tx_receipt = datacontract.consent_contract.deploy()
        logger.info("Deploy Consentcode smart contract receipt:")
        logger.info(tx_receipt)

        # print(tx_receipt)

        # logger.info(type(tx_receipt))
        if type(tx_receipt) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(tx_receipt)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt)

        # tx_receipt0 = datacontract.consent_contract.upload_data_consent(
        #     estimate)

        logger.info("Start to update ConsentCode smart contract")

        tx_receipt0 = datacontract.consent_contract.update_data_consent()
        logger.info("Update consent:")
        logger.info(tx_receipt0)

        if type(tx_receipt0) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(tx_receipt0)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt0)

        # tx_receipt2 = datacontract.deploy_contract()
        logger.info("Start to deploy Dataset smart contract")

        tx_receipt2 = datacontract.deploy()
        logger.info("Datacontract receipt:")
        logger.info(tx_receipt2)

        if type(tx_receipt2) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(
                tx_receipt2, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt2)

        registry_address = LuceRegistry.objects.get(pk=1).contract_address

        # tx_receipt3 = datacontract.set_registry_address(
        #     LuceRegistry.objects.get(pk=1), estimate)

        logger.info("Start to set registry address")
        tx_receipt3 = datacontract.set_registry_address(registry_address)
        logger.info("Set registry address receipt:")
        logger.info(tx_receipt3)

        if type(tx_receipt3) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(
                tx_receipt3, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt3)

        logger.info("Start to set consent address")
        tx_receipt4 = datacontract.set_consent_address()
        logger.info("Set consent address receipt:")
        logger.info(tx_receipt4)
        if type(tx_receipt4) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(
                tx_receipt4, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt4)

        logger.info("Start to publish data")
        tx_receipt5 = datacontract.publish_dataset(link)
        logger.info("Publish data receipt:")
        logger.info(tx_receipt5)
        if type(tx_receipt5) is list:
            datacontract.delete()
            response = custom_exeptions.blockchain_exception(
                tx_receipt5, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(tx_receipt5)

        logger.info(tx_receipts)

        print("###########")
        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "data published successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["contracts"] = serializer.data
        response["data"]["transaction receipts"] = tx_receipts
        return Response(response)

    def get(self, request, format=None):
        contract_address = request.data.get('contract_address')
        c = ConsentContract.objects.get(contract_address=contract_address)
        CCS = ConsentContractSerializer(c)
        r = c.retrieve_contract_owner()
        return Response(CCS.data)


class RequestDatasetView(APIView):
    """
    Handles dataset access requests by authenticated users.

    Users must be authenticated to make dataset access requests. This view supports 
    registration and validation of data contracts on the Ethereum blockchain.
    """

    # Specifies that the user must be authenticated to use this view
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        """
        Handles POST requests for dataset access.

        This method extracts request data, logs relevant information, checks the Ethereum public key
        of the requesting user, and processes each dataset contract address in the request.

        Args:
            request (Request): The HTTP request object.
            format (str, optional): Format of the request. Defaults to None.

        Returns:
            Response: A Response object with either the transaction receipts or error message.
        """
        estimate = request.data.pop("estimate", False)
        access_time = request.data.pop("access_time", 100000000)
        purpose_code = request.data.pop("purpose_code", 1)
        dataset_addresses = request.data.pop("dataset_addresses", False)

        if request.user.ethereum_public_key is None:
            response = custom_exeptions.custom_message(
                "user needs to have a wallet connected")
            return Response(response["body"], response["status"])

        if not dataset_addresses:
            return Response({"error": "please specify a dataset_contrat"})
        all_receipts = []

        for contract in dataset_addresses:
            tx_receipts = self.request_access(contract, request, access_time,
                                              estimate, purpose_code)
            if type(tx_receipts) is Response:
                return tx_receipts
            all_receipts.append(tx_receipts)

        response = get_initial_response()
        print("all_receipts:\n", all_receipts)
        response["error"]["code"] = 200
        response["error"]["message"] = "data requested successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["transaction receipts"] = all_receipts

        return Response(response)

    def request_access(self, c_address, request, access_time, estimate,
                       purpose_code):
        """
        Requests access to a specific dataset contract address.

        This method validates the research purpose, checks the existence of the dataset and LuceRegistry,
        and handles the registration and research purpose assignments on the Ethereum blockchain.

        Args:
            c_address (str): The contract address to request access to.
            request (Request): The HTTP request object.
            access_time (int): Time to access the dataset.
            estimate (bool): Flag to determine if this is an estimation request.
            purpose_code (int): Code indicating the purpose of the request.

        Returns:
            Union[Response, List]: A Response object with an error message or a list of transaction receipts.
        """

        rp_serializer = ResearchPurposeSerializer(data=request.data)
        if not rp_serializer.is_valid():
            response = custom_exeptions.validation_exeption(rp_serializer)
            return Response(response["body"], response["status"])
        rp = rp_serializer.save()
        if not DataContract.objects.filter(
                contract_address=c_address).exists():
            response = custom_exeptions.custom_message(
                "dataset was not specified")
            return Response(response["body"], response["status"])

        if not LuceRegistry.objects.filter(pk=1).exists():
            response = custom_exeptions.custom_message(
                "luce registry was not deployed")
            return Response(response["body"], response["status"])

        luceregistry = LuceRegistry.objects.get(pk=1)
        datacontract = DataContract.objects.get(contract_address=c_address)
        datacontract.consent_contract.research_purpose = rp
        datacontract.save()

        tx_receipts = []

        is_registered = luceregistry.is_registered(request.user, "requester")
        # print(is_registered)
        if is_registered == 0:
            receipt = luceregistry.register_requester(request.user, 1,
                                                      estimate)
            if type(receipt) is list:
                datacontract.consent_contract.research_purpose.delete()
                response = custom_exeptions.blockchain_exception(
                    receipt, tx_receipts)
                return Response(response["body"], response["status"])
            tx_receipts.append(receipt.status)

        # print("hereeeeeeeeeeee")
        receipt2 = datacontract.consent_contract.give_general_research_purpose(
            request.user, estimate)
        if type(receipt2) is list:
            datacontract.consent_contract.research_purpose.delete()
            response = custom_exeptions.blockchain_exception(
                receipt2, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(receipt2)

        receipt3 = datacontract.consent_contract.give_HMB_research_purpose(
            request.user, estimate)
        if type(receipt3) is list:
            datacontract.consent_contract.research_purpose.delete()
            response = custom_exeptions.blockchain_exception(
                receipt3, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(receipt3)

        receipt4 = datacontract.consent_contract.give_clinical_research_purpose(
            request.user, estimate)
        if type(receipt4) is list:
            datacontract.consent_contract.research_purpose.delete()
            response = custom_exeptions.blockchain_exception(
                receipt4, tx_receipts)
            return Response(response["body"], response["status"])
        tx_receipts.append(receipt4)

        receipt5 = datacontract.add_data_requester(access_time, purpose_code,
                                                   request.user, estimate)

        if type(receipt5) is list:
            datacontract.consent_contract.research_purpose.delete()
            response = custom_exeptions.blockchain_exception(
                receipt5, tx_receipts)
            return Response(response["body"], response["status"])

        tx_receipts.append(receipt5)
        # print("111111")
        if estimate:
            return Response({
                "gas_estimate":
                receipt + receipt2 + receipt3 + receipt5 + receipt5
            })

        logger.info(tx_receipts)
        return tx_receipts


class GetLink(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        estimate = request.data.pop("estimate", False)
        access_time = request.data.pop("access_time", 1000)
        purpose_code = request.data.pop("purpose_code", 1)
        dataset_address = request.data.pop("dataset_address", False)
        logger.info(dataset_address)

        if not DataContract.objects.filter(
                contract_address=dataset_address).exists():
            response = custom_exeptions.custom_message(
                "dataset was not specified")
            return Response(response["body"], response["status"])

        tx_receipts = []
        datacontract = DataContract.objects.get(
            contract_address=dataset_address)
        link = datacontract.getLink(request.user, estimate)
        if type(link) is list:
            # datacontract.consent_contract.research_purpose.delete()
            response = custom_exeptions.custom_message("no access")
            return Response(response["body"], response["status"])
        tx_receipts.append(link)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "link requested successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["link"] = link
        return Response(response)


class RetrieveContractByUserIDView(APIView):
    def get(self, request, id, format=None):
        if not User.objects.filter(pk=id).exists():
            response = custom_exeptions.custom_message("user does not exist")
            return Response(response["body"], response["status"])
        user = User.objects.get(pk=id)
        contracts = DataContract.objects.filter(user=id)
        contracts_serializer = DataContractSerializer(contracts, many=True)
        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "contracts retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["contracts"] = contracts_serializer.data

        return Response(response)


class SearchContract(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        searchparam = request.data.pop("search_content", "")

        RP_serializer = ResearchPurposeSerializer(data=request.data)
        if not RP_serializer.is_valid():
            response = custom_exeptions.validation_exeption(RP_serializer)
            return Response(response["body"], response["status"])
        researchPurpose = RP_serializer.save()
        print(researchPurpose)

        final_result = []
        contracts = DataContract.objects.filter(
            description__contains=searchparam)
        for contract in contracts:
            if (contract.checkAccess(user, researchPurpose)):
                final_result.append(contract)
        contracts = DataContractSerializer(final_result, many=True)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "contracts retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["contracts"] = contracts.data
        return Response(response)


class LuceRegistryView(APIView):
    """
    While deploying LUCERegistry contract, the request should be handled
    by Django first (in case of failure), and then blockchain.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if not LuceRegistry.objects.filter(pk=1).exists():
            return Response({"error": "luce registry was not deployed"},
                            status=status.HTTP_400_BAD_REQUEST)

        registry = LuceRegistry.objects.get(pk=1)
        serializer = RegestryContractSerializer(registry)
        return Response(serializer.data)

    def post(self, request, format=None):
        estimate = request.data.get('estimate', False)
        user = request.user

        # Deploy verifier
        from blockchain.models import PlonkVerifierContract
        if not PlonkVerifierContract.objects.filter(pk=1).exists():
            verifier = PlonkVerifierContract.objects.create(pk=1)
            verifier.deploy()
            # verifier.save()

        if user.ethereum_public_key is None or user.ethereum_private_key is None:
            response = custom_exeptions.custom_message(
                "user must connect a wallet first")
            return Response(response["body"], response["status"])

        if (estimate):
            return self.estimated_gas

        # get contract if doesn't exist create it
        if LuceRegistry.objects.filter(pk=1).exists():
            registry = LuceRegistry.objects.get(pk=1)
        else:
            registry = LuceRegistry.objects.create(pk=1, user=user)

        registry.user = user
        tx_receipt = registry.deploy()
        if type(tx_receipt) is list:
            response = custom_exeptions.blockchain_exception(tx_receipt)
            return Response(response["body"], response["status"])

        registry.save()
        serializer = RegestryContractSerializer(registry)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "luceRegistry was deployed successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["contracts"] = [serializer.data]
        response["data"]["transaction receipts"] = [tx_receipt]

        return Response(response)
