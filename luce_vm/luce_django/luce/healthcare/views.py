from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from utils import custom_exeptions
from accounts.models import User
from blockchain.models import DataContract
from blockchain.models import LuceRegistryContract as LuceRegistry
from privacy.disposable_address import DisposableAddressService
from utils.utils import get_initial_response, set_logger
from .serializers import *
from utils.web3_scripts import *


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

    def get(self, request, format=None):
        contract_address = request.data.get('contract_address')
        c = ConsentContract.objects.get(contract_address=contract_address)
        CCS = ConsentContractSerializer(c)
        r = c.retrieve_contract_owner()
        return Response(CCS.data)

    def post(self, request, format=None):
        link = request.data.get("link", False)
        # print(request.data)
        logger.info(request.data)
        if not link:
            return self.handle_error("link field is required", "Link field is invalid (empty?)")

        if not self.is_luce_registry_deployed():
            return self.handle_error("luce registry was not deployed", "Luce registry was not deployed!")

        contract_serializer, restriction_serializer = self.initialize_serializers(
            request)

        if not restriction_serializer.is_valid():
            return self.handle_serializer_error(restriction_serializer)

        if not contract_serializer.is_valid():
            return self.handle_serializer_error(contract_serializer)

        datacontract = contract_serializer.save()

        try:
            tx_receipts = self.handle_smart_contracts(datacontract, link)
        except Exception as e:
            return Response({"error": str(e)}, status=400)

        response = self.get_success_response(contract_serializer, tx_receipts)
        return Response(response)

    def is_luce_registry_deployed(self):
        return LuceRegistry.objects.filter(pk=1).exists()

    def get_luce_registry(self):
        return LuceRegistry.objects.get(pk=1)

    def get_disposable_address(self, user_account, amount):
        disposable_address_service = DisposableAddressService()
        return disposable_address_service.get_a_new_address_with_balance(
            user_account, amount)

    def handle_error(self, user_message, log_message):
        logger.error(log_message)
        response = custom_exeptions.custom_message(user_message)
        return Response(response["body"], response["status"])

    def initialize_serializers(self, request):
        serializer = DataContractSerializer(
            data=request.data,
            context={
                "estimate": request.data.get("estimate", False),
                "restrictions": request.data,
                "user": request.user
            },
            partial=True
        )
        restriction_serializer = RestrictionsSerializer(data=request.data)
        return serializer, restriction_serializer

    def handle_smart_contracts(self, datacontract, link):
        tx_receipts = []

        # Deploy ConsentCode smart contract
        tx_receipt = self.deploy_consent_code_contract(datacontract)
        if isinstance(tx_receipt, list):
            datacontract.delete()
            raise Exception("Error deploying ConsentCode smart contract")
        tx_receipts.append(tx_receipt)

        # Update ConsentCode smart contract
        tx_receipt0 = self.update_consent_code_contract(datacontract)
        if isinstance(tx_receipt0, list):
            datacontract.delete()
            raise Exception("Error updating ConsentCode smart contract")
        tx_receipts.append(tx_receipt0)

        # Deploy Dataset smart contract
        tx_receipt2 = self.deploy_dataset_contract(datacontract)
        if isinstance(tx_receipt2, list):
            datacontract.delete()
            raise Exception("Error deploying Dataset smart contract")
        tx_receipts.append(tx_receipt2)

        # Set registry address
        registry_address = LuceRegistry.objects.get(pk=1).contract_address
        tx_receipt3 = self.set_registry_address(datacontract, registry_address)
        if isinstance(tx_receipt3, list):
            datacontract.delete()
            raise Exception(
                "Error setting registry address for Dataset smart contract")
        tx_receipts.append(tx_receipt3)

        # Set consent address
        tx_receipt4 = self.set_consent_address(datacontract)
        if isinstance(tx_receipt4, list):
            datacontract.delete()
            raise Exception(
                "Error setting consent address for Dataset smart contract")
        tx_receipts.append(tx_receipt4)

        # Publish data
        tx_receipt5 = self.publish_data(datacontract, link)
        if isinstance(tx_receipt5, list):
            datacontract.delete()
            raise Exception("Error publishing data")
        tx_receipts.append(tx_receipt5)

        return tx_receipts

    def deploy_consent_code_contract(self, datacontract):
        logger.info("Start to deploy ConsentCode smart contract")
        tx_receipt = datacontract.consent_contract.deploy()
        logger.info("Deploy Consentcode smart contract receipt:")
        logger.info(tx_receipt)
        return tx_receipt

    def update_consent_code_contract(self, datacontract):
        logger.info("Start to update ConsentCode smart contract")
        tx_receipt = datacontract.consent_contract.update_data_consent()
        logger.info("Update consent:")
        logger.info(tx_receipt)
        return tx_receipt

    def deploy_dataset_contract(self, datacontract):
        logger.info("Start to deploy Dataset smart contract")
        tx_receipt = datacontract.deploy()
        logger.info("Datacontract receipt:")
        logger.info(tx_receipt)
        return tx_receipt

    def set_registry_address(self, datacontract, registry_address):
        logger.info("Start to set registry address")
        tx_receipt = datacontract.set_registry_address(registry_address)
        logger.info("Set registry address receipt:")
        logger.info(tx_receipt)
        return tx_receipt

    def set_consent_address(self, datacontract):
        logger.info("Start to set consent address")
        tx_receipt = datacontract.set_consent_address()
        logger.info("Set consent address receipt:")
        logger.info(tx_receipt)
        return tx_receipt

    def publish_data(self, datacontract, link):
        logger.info("Start to publish data")
        tx_receipt = datacontract.publish_dataset(link)
        logger.info("Publish data receipt:")
        logger.info(tx_receipt)
        return tx_receipt

    def get_success_response(self, serializer, tx_receipts):
        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "data published successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]
        response["data"] = {}
        response["data"]["contracts"] = serializer.data
        response["data"]["transaction receipts"] = tx_receipts
        return response


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
