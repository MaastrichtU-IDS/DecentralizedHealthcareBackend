from accounts.models import User, DataContract
from rest_framework import permissions, generics, filters, parsers, renderers,status
from rest_framework.compat import coreapi, coreschema
from rest_framework.schemas import ManualSchema
from rest_framework.schemas import coreapi as coreapi_schema
from rest_framework.authtoken.serializers import AuthTokenSerializer
import utils.custom_exeptions as custom_exeptions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from utils.web3_scripts import *
from utils.utils import get_initial_response


# APIview for registering donors and influencers.
class UserRegistration(APIView):
    def post(self, request, format=None):
        createWallet = request.data.get("create_wallet")
        serializer = UserSerializer(data = request.data, context={"create_wallet": createWallet})

        ##serializer validation
        if not serializer.is_valid(): 
            response = custom_exeptions.validation_exeption(serializer)
            return response
                   
        instance = serializer.save()
        tx_receipt = self.address_get_or_create(instance, createWallet)

        #blockchain error handling
        if type(tx_receipt) is list:
            instance.delete()
            return custom_exeptions.blockchain_exception(tx_receipt)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "registration successfull"
        response["error"]["status"] = "OK"
        response["error"]["details"] = [{"reason":"SUCCESS"}]    
        response["data"]["transaction receipts"] = [tx_receipt]
    
        return Response(response, status=status.HTTP_200_OK)

    def address_get_or_create(self, instance, createWallet):
            if(createWallet):
                tx_receipt = instance.create_wallet()
                instance.save()
            
                if tx_receipt:
                    return tx_receipt     
            tx_receipt = None
            return tx_receipt

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
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
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid(): 
            return custom_exeptions.validation_exeption(serializer)

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
        serializer = UserSerializer(user, data=request.data, context={"create_wallet": createWallet}, partial=True)

        if not serializer.is_valid(): 
            return custom_exeptions.validation_exeption(serializer)
        
        tx_receipt = self.address_get_or_create(instance, createWallet)
        if type(tx_receipt) is list:
            return custom_exeptions.blockchain_exception(tx_receipt)


        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "update user successfull"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"]["transaction receipts"] = [tx_receipt]

        serializer.save()
        return Response(response, status = status.HTTP_200_OK)

    def address_get_or_create(self, instance, createWallet):
                if(createWallet):
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
        response["error"]["message"] = "user public data retrieved successfully"
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
        response["error"]["message"] = "user private data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"]["users"] = [serializer.data]
        return Response(response)
    

class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        serializer = PublicUserSerializer(users, many = True)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "all user data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"]["users"] = [serializer.data]
        return Response(response)

class ContractsListView(APIView):
    def get(self, request, format=None):
        contracts = DataContract.objects.all()
        serializer = DataContractSerializer(contracts, many = True)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "all user data retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"]["contracts"] = serializer.data
        return Response(response)



class UploadDataView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        user = request.user
        estimate = request.data.get("estimate", False)
        link = request.data.get("link", False)

        if user.ethereum_public_key is None:
            return custom_exeptions.custom_message("user needs to have a wallet connected")

        if not link:
            return custom_exeptions.custom_message("link field is required")

        tx_receipts = []

        if not LuceRegistry.objects.filter(pk=1).exists():
                    return custom_exeptions.custom_message("luce registry was not deployed")
        luceregistry = LuceRegistry.objects.get(pk = 1)

        serializer = DataContractSerializer(data = request.data, context = {"estimate":estimate,"restrictions":request.data, "user":request.user}, partial = True)
        restriction_serializer = RestrictionsSerializer(data = request.data)


        ##check that user is registered in LuceRegistry, if not register him
        is_registered = luceregistry.is_registered(request.user, "provider")
        if not is_registered:
            cost = LuceRegistry.objects.get(pk=1).register_provider(user, estimate)
            if type(cost) is list:
                return custom_exeptions.blockchain_exception(cost)
            tx_receipts.append(cost)

        if not restriction_serializer.is_valid():
            return custom_exeptions.validation_exeption(restriction_serializer)
        if not serializer.is_valid():
            return custom_exeptions.validation_exeption(serializer)
        datacontract = serializer.save()
        
        tx_receipt = datacontract.consent_contract.deploy_contract()
        if type(tx_receipt) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt)
        tx_receipts.append(tx_receipt)

        tx_receipt0 = datacontract.consent_contract.upload_data_consent(estimate)
        if type(tx_receipt0) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt0)
        tx_receipts.append(tx_receipt0)

        tx_receipt2 = datacontract.deploy_contract()

        if type(tx_receipt2) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt2, tx_receipts)
        tx_receipts.append(tx_receipt2)


        tx_receipt3 = datacontract.set_registry_address(LuceRegistry.objects.get(pk=1), estimate)
        if type(tx_receipt3) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt3, tx_receipts)
        tx_receipts.append(tx_receipt3)

        tx_receipt4 = datacontract.set_consent_address(estimate)
        if type(tx_receipt4) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt4, tx_receipts)
        tx_receipts.append(tx_receipt4)

        tx_receipt5 = datacontract.publish_dataset(user,link, estimate)
        if type(tx_receipt5) is list:
                datacontract.delete()
                return custom_exeptions.blockchain_exception(tx_receipt5, tx_receipts)
        tx_receipts.append(tx_receipt5)
    
        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "data published successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"] = {}
        response["data"]["contracts"]= [serializer.data]
        response["data"]["transaction receipts"] = tx_receipts
        return Response(response)

    def get(self, request, format=None):
        contract_address = request.data.get('contract_address')
        c = ConsentContract.objects.get(contract_address = contract_address)
        CCS = ConsentContractSerializer(c)
        r = c.retrieve_contract_owner()
        return Response(CCS.data)

class RequestDatasetView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        estimate = request.data.pop("estimate", False)
        access_time = request.data.pop("access_time", 100000000)
        purpose_code = request.data.pop("purpuse_code", 1)
        dataset_addresses = request.data.pop("dataset_addresses", False)


        if not dataset_addresses:
            return Response({"error":"please specify a dataset_contrat"})
        all_receipts = []
        
        for contract in dataset_addresses:
            print("##################CONTRACT########################")
            tx_receipts = self.request_access(contract, request, access_time, estimate, purpose_code)
            if type(tx_receipts) is Response:
                return tx_receipts
            all_receipts.append(tx_receipts)

        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "data requested successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"] = {}
        response["data"]["transaction receipts"] = all_receipts
            
        return Response(response)


    def request_access(self, c_address, request, access_time, estimate, purpose_code):
        
        rp_serializer = ResearchPurposeSerializer(data = request.data)
        if not rp_serializer.is_valid():
            return Response(rp_serializer.errors)
        rp = rp_serializer.save()

        if not DataContract.objects.filter(contract_address = c_address).exists():
            return custom_exeptions.custom_message("dataset was not specified")


        if not LuceRegistry.objects.filter(pk=1).exists():
            return custom_exeptions.custom_message("luce registry was not deployed")


        luceregistry = LuceRegistry.objects.get(pk = 1)
        datacontract = DataContract.objects.get(contract_address = c_address)
        datacontract.consent_contract.research_purpuse = rp
        datacontract.save()

        tx_receipts = []

        is_registered = luceregistry.is_registered(request.user, "requester")
        if is_registered==0:
            receipt = luceregistry.register_requester(request.user, 1, estimate)
            if type(receipt) is list:
                    datacontract.consent_contract.research_purpuse.delete()
                    return custom_exeptions.blockchain_exception(receipt, tx_receipts)
            tx_receipts.append(receipt)
        receipt2 = datacontract.consent_contract.give_research_purpose(rp, request.user, estimate)
        if type(receipt2) is list:
                datacontract.consent_contract.research_purpuse.delete()
                return custom_exeptions.blockchain_exception(receipt2, tx_receipts)
        tx_receipts.append(receipt2)

        receipt3 = datacontract.add_data_requester(access_time,purpose_code, request.user, estimate)
        if type(receipt3) is list:
                datacontract.consent_contract.research_purpuse.delete()
                return custom_exeptions.blockchain_exception(receipt3, tx_receipts)
        tx_receipts.append(receipt3)
        
        if estimate:
            return Response({"gas_estimate": receipt+receipt2+receipt3})

        return tx_receipts



class GetLink(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        estimate = request.data.pop("estimate", False)
        access_time = request.data.pop("access_time", 1000)
        purpose_code = request.data.pop("purpuse_code", 1)
        dataset_address = request.data.pop("dataset_address", False)
        if not DataContract.objects.filter(contract_address = dataset_address).exists():
            return custom_exeptions.custom_message("dataset was not specified")
        tx_receipts = []
        datacontract = DataContract.objects.get(contract_address = dataset_address)
        link = datacontract.getLink(request.user, estimate)
        if type(link) is list:
                datacontract.consent_contract.research_purpuse.delete()
                return custom_exeptions.blockchain_exception(link, tx_receipts)
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
        if not User.objects.filter(pk = id).exists():
            return custom_exeptions.custom_message("user does not exist")
        user = User.objects.get(pk = id)
        contracts = DataContract.objects.filter(user = id)
        contracts_serializer = DataContractSerializer(contracts, many=True)
        response = get_initial_response()
        response["error"]["code"] = 200
        response["error"]["message"] = "contracts retrieved successfully"
        response["error"]["status"] = "OK"
        response["error"]["details"] = ["SUCCESS"]    
        response["data"] = {}
        response["data"]["contracts"] = contracts_serializer.data

        return Response(response)


class SearchContract(generics.ListAPIView):
    serializer_class = DataContract
    queryset = DataContract.objects.all()
    serializer_class = DataContractSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['description'] 




    

class LuceRegistryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        if not LuceRegistry.objects.filter(pk=1).exists():
            return Response({"error":"luce registry was not deployed"}, status=status.HTTP_400_BAD_REQUEST)
        registry = LuceRegistry.objects.get(pk=1)
        serializer = RegestryContractSerializer(registry)
        return Response(serializer.data)

    def post(self, request, format=None):
        estimate = request.data.get('estimate', False)
        user = request.user

        if user.ethereum_public_key is None or user.ethereum_private_key is None:
            return custom_exeptions.custom_message("user must connect a wallet first")

        if(estimate):
            return self.estimated_gas
            
        #get contract if doesn't exist create it
        if LuceRegistry.objects.filter(pk=1).exists():
            registry = LuceRegistry.objects.get(pk=1)
        else:
            registry = LuceRegistry.objects.create(pk=1, user = user)

        registry.user = user
        tx_receipt = registry.deploy_contract()
        if type(tx_receipt) is list:
            return custom_exeptions.blockchain_exception(tx_receipt)

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
    
    

