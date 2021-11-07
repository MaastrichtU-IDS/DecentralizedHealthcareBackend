import re
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.http import is_safe_url
from django.utils.regex_helper import Group
from accounts.models import User
from rest_framework import serializers, authentication, permissions
from rest_framework import generics
from rest_framework import filters
from rest_framework import viewsets



from django.http import JsonResponse
import json
from django.http import Http404
from rest_framework.views import APIView

from rest_framework.response import Response
from rest_framework import status

# Access to Dataset model
from datastore.models import Dataset

# Access to forms
from accounts.forms import RegisterForm, LoginForm

# For login view:
from django.contrib.auth import authenticate, login, get_user_model

# For class-based views:
from django.views.generic import CreateView, FormView

# For redirect after form submission
from django.shortcuts import redirect
# Import newest versions of web3 scripts
from utils.web3_scripts import (
assign_address_v3,
deploy_contract_v3, 
publish_data_v3, 
add_requester_v3, 
update_contract_v3,
donate,
register_cause,
add_balance,
check_balance,
check_cause,
createGroup, 
contractDonations,
groupCreations,
donateToGroup,
check_balance_influencer,
)

from .serializers import (
    UserSerializer, PublicUserSerializer
 )



# APIview for registering donors and influencers.
class UserRegistration(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data = request.data)
        
        if not serializer.is_valid(): 
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PublicUserInfoView(APIView):

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = PublicUserSerializer(user)
        return Response(serializer.data)

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

class PrivateUserInfoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, id, format=None):
        user = self.get_object(id)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def get_object(self, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            raise Http404

class UserListView(APIView):
    def get(self, request, format=None):
        users = User.objects.all()
        print(users)
        serializer = PublicUserSerializer(users, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)
"""
class FundUser(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        errors = {}
        if "amount" not in request.data:
            errors["amount"] = ["This field is required"]
        user = request.user
        if user.user_type == 0:
            errors["user"] = ["influencers cannot fund their"]
        if errors:
            return Response(errors)
        amount = request.data.get("amount")
        receipt = add_balance(user, amount)
        if type(receipt) is ValueError:
            raise receipt
        balances = check_balance(user)
        return Response({"message":"blance updatad successfully", "balances":balances, "gas used":receipt["cumulativeGasUsed"]})

#get a list of all users
class ListUsers(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    
    def get(self, request, format=None):
        queryset =  User.objects.all()
        serializer = PublicUserSerializer(queryset, many = True)
        return Response(serializer.data)

class UserView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

class InfluencerSearch(generics.ListAPIView):
    queryset = User.objects.filter(user_type = 0)
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name", "ethereum_public_key"]
class DonorSearch(generics.ListAPIView):
    queryset = User.objects.filter(user_type = 1)
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name", "ethereum_public_key"]
class UserSearch(generics.ListAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicUserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ["email", "first_name", "last_name", "ethereum_public_key"]

class GroupSearch(generics.ListAPIView):
    queryset = CauseGroup.objects.all()
    serializer_class = PublicGroupSerializer
    permission_classes = [permissions.AllowAny]
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["id"]

class DonorBalanceView(APIView):
    def post(self, request, format=None):
        if "donor" not in request.data:
            return Response({"errors":"donor must be specified"})
        if User.objects.filter(pk = request.data["donor"]).count() != 1:
            return Response({"errors":"donor id not found"})
        donor = User.objects.get(pk = request.data["donor"])
        if donor.user_type != 1:
            return Response({"errors":"donor id must be of a donor, not influencer"})
        balance = check_balance(donor)
        return Response(balance)
class InfluecerBalanceView(APIView):
    def post(self, request, format=None):
        if "influencer" not in request.data:
            return Response({"errors":"influencer must be specified"})
        if User.objects.filter(pk = request.data["influencer"]).count() != 1:
            return Response({"errors":"influencer id not found"})
        influencer = User.objects.get(pk = request.data["influencer"])
        if influencer.user_type != 0:
            return Response({"errors":"influencer id must be of a influencer, not donor"})
        balance = check_balance_influencer(influencer)
        return Response(balance)

class ContractGroups(APIView):
    def post(self, request, format=None):
        errors = []
        if "influencer" not in request.data:
            errors.append("must specify influencer id")  
        if "group" not in request.data:
            group = 0 
        else:
            if CauseGroup.objects.filter(pk = request.data["group"]).count() !=1:
                return Response({"errors":"group id not found"})
            group = CauseGroup.objects.get(pk = request.data["group"])
            
        if len(errors) != 0:
            return Response({"errors":errors})
        if User.objects.filter(pk = request.data["influencer"]).count() != 1:
            errors.append("influencer with this id not found")
            return Response({"errors":errors})
        influencer = User.objects.get(pk = request.data["influencer"])
        if influencer.user_type != 0:
            errors.append("influencer id must be of influencer")

        events = groupCreations(influencer, group)   
        return Response(events)



class ContractDonations(APIView):
    def post(self, request, format=None):
        errors = []
        if "influencer" not in request.data:
            errors.append("influencer id not specified")
        if User.objects.filter(pk = request.data["influencer"]).count() != 1:
            errors.append("influencer with this id not found")
            return Response({"errors":errors})

        if len(errors) != 0:
            return Response({"errors":errors})
        influencer = User.objects.get(pk = request.data["influencer"])

        if "user" not in request.data:
            donor = 0
        else:
            if User.objects.filter(pk = request.data["user"]).count() != 1:
                errors.append("donor with this id not found")
                return Response({"errors":errors})

            donor = User.objects.get(pk = request.data["user"])
            if donor.user_type != 1:
                errors.append("user id must be of donor")
            
        if "cause" not in request.data:
            cause = 0
        else:
            if  Cause.objects.filter(pk = request.data["cause"]).count() != 1:
                errors.append("cause with this id not found")
                return Response({"errors":errors})
            cause = Cause.objects.get(pk = request.data["cause"])
            if cause.creator.id != influencer.id :
                errors.append("this cause id not from this influencer")
        if influencer.user_type != 0:
            errors.append("influecer id must be of influencer")
        if len(errors) != 0:
            return Response({"errors":errors})
            
        events  = contractDonations(donor, influencer, cause)
        return Response(events)



class RegisterGroup(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        if "info" not in request.data:
            return Response({"error":"you must specify a info array"})
        infodata = request.data.pop("info")
        request.data["creator"] = request.user.id
        group_serializer = PublicGroupSerializer(data =  request.data)
        valid1 = group_serializer.is_valid()
        if not valid1:
            return Response({"1":group_serializer.errors})
        group = group_serializer.save()
        sum = 0
        serials = []
        causes_ids = []
        splits = []
        for info in infodata:
            info["group"] = group.id
            sum += info["split"]
            info_serializer = PublicGroupInfoSerializer(data = info)
            valid2 = info_serializer.is_valid()
            if not valid2:
                return Response({"2":info_serializer.errors})
            serials.append(info_serializer)
        for serializer in serials:
            serializer.save()
            causes_ids.append(serializer.data["cause"])
            splits.append(serializer.data["split"])
        if sum != 10000:
            return Response({"error":"split sum incomplete"})
        print(createGroup(causes_ids, splits, group.id, request.user))
        return Response(info_serializer.data)
        

#APIview for registering a cause
class RegisterCause(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        serializer = CauseSerializer(data = request.data, context = {"request":request})
        validation = serializer.is_valid()
        if not validation:
            return Response(serializer.errors)
        assign_address_v3(serializer)
        cause = serializer.save()
        print(register_cause(cause))
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class CheckCause(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        errors = {}
        if "cause_id" not in request.data:
            errors["cause_id"] = ["This field is required"]
        if errors:
            return Response(errors)
        cause_id = request.data["cause_id"]
        causeObject = Cause.objects.filter(pk = cause_id)
        
        if not causeObject.exists():
            errors["cause_not_found"] = "no cause found with this id" 
        if errors:
            cause = ""
            
        cause = check_cause(user, causeObject.first())

        
        return Response(cause)
        
        
        

class CauseSearch(generics.ListAPIView):
    queryset = Cause.objects.all()
    permission_classes = [permissions.AllowAny]
    pagination_class=None
    serializer_class = PublicCauseSerializer
    search_fields = ["title", "description", "ethereum_public_key"]
    
class CauseSearchByInfluencerID(generics.ListAPIView):
    queryset = Cause.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicCauseSerializer
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["=creator__id"]
    
class CauseSearchByInfluencer(generics.ListAPIView):
    queryset = Cause.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicCauseSerializer
    pagination_class=None 
    filter_backends = [filters.SearchFilter]
    search_fields = ["creator__first_name", "creator__last_name", "creator__email"]
    

class CreateDonationToGroup(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        donor = request.user
        errors =[]
        if "group" not in request.data:
            errors.append("group id must be specified")
        if "amount" not in request.data:
            errors.append("amount must be specified")
        if len(errors) != 0:
            return Response({"errors":errors})
        amount = request.data["amount"]
        group_id = request.data["group"]
        if CauseGroup.objects.filter(pk = group_id).count() != 1:
            return Response({"error":"group id not found"})
        group = CauseGroup.objects.get(pk = group_id)
        donateToGroup(donor, group, amount)
        return Response({"success":"donation was successfull"})

class createDonation(APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, format=None):
        if Cause.objects.filter(pk = request.data.get('cause')).count()!=1:
            return Response({"error":"cause id not found"})
        user = request.user
        cause = Cause.objects.get(pk = request.data["cause"])
        donation_serializer = DonationSerializer(data = request.data, context = {"request":request})
        valid = donation_serializer.is_valid()
        if request.data.get('donor') != request.user.id:
            return Response({"error":"the donor id doesn't correspond to the authenticated user"})
        if not valid:
            return Response(donation_serializer.errors)
        logs = donate(validated_donation_serializer = donation_serializer,  _user = request.user)
        donation_serializer.save()

        return Response({"donation":donation_serializer.data},status=status.HTTP_201_CREATED) 
  
class UserDonations(APIView):
    def post(self, request, format=None):
        if "donor_id" not in request.data:
            return Response({"errors":"donor_id field is required"})
        donations = Donation.objects.filter(donor_id = request.data["donor_id"])
        print(donations)
        donations_data = []
        for donation in donations:
            donation_serializer = PublicDonationSerializer(donation , context = {"request":request})
            donations_data.append(donation_serializer.data)
        
        return Response(donations_data)
class getDonation(APIView):
      def get(self, request, format=None):
        if "id" not in request.data:
            return Response({"errors":"id field is required"})
        donation = Donation.objects.filter(pk = request.data["id"])
        if not donation.exists():
            return Response({"errors":"id not found"})
        donation_serializer = PublicDonationSerializer(donation.first() , context = {"request":request})
        creator_id = donation_serializer.data["cause"]["creator"]["id"]
        donor_id = donation_serializer.data["donor"]["id"]

        creator = User.objects.get(pk = creator_id)
        donor = User.objects.get(pk = donor_id)

        searchDonations(donor, creator)
        return Response(donation_serializer.data)

class DonationSearchByCause(generics.ListAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicDonationSerializer
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["cause__title", "cause__description"]

class DonationSearchByCauseID(generics.ListAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicDonationSerializer
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["=cause__id"]

class DonationSearchByDonor(generics.ListAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicDonationSerializer
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["donor__email", "donor__first_name", "donor__last_name"]
class DonationSearchByDonorID(generics.ListAPIView):
    queryset = Donation.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = PublicDonationSerializer
    pagination_class=None
    filter_backends = [filters.SearchFilter]
    search_fields = ["=donor__id"]

#this APIView is used to deploy contract
class DeployContract(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, format=None):
        user_type = request.data.get('user_type')
        contract_serializer = ContractSerializer(data = request.data)
        user_serializer = UserSerializer(request.user)
        validation = contract_serializer.is_valid()
        if not validation:
            return Response(contract_serializer.errors)
        contract_address = deploy_contract_v3(user_serializer.data["ethereum_private_key"], contract_serializer.data["user_type"])
        return Response({"contract_address": contract_address, "user_type":user_type})


class LoginView(FormView):
    form_class = LoginForm
    template_name = 'accounts/login.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None


        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView, self).form_invalid(form)


class LoginView_PostReg(FormView):
    form_class = LoginForm
    template_name = 'accounts/login_post_reg.html'
    success_url = '/'

    def form_valid(self, form):
        request = self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None


        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView, self).form_invalid(form)


# Available scripts:
# create_wallet_old, fund_wallet, deploy_contract, assign_address
# assign_address_v3, deploy_contract_v3, publish_data_v3, add_requester_v3, update_contract_v3
def dev_view(request):

    # For testing make sure the current user has uploaded at least one dataset 
    dev_user = request.user # obtain current user
    if len(dev_user.datasets_owned.all()) >= 1:
        dev_dataset = dev_user.datasets_owned.all()[0] # Use first dataset that was uploaded by current user

    # Assign address & pre-fund
    if(request.GET.get('assign_address_v3')):
        # Pass user into web3 script
        current_user = dev_user
        # Script does work and passes updated user object back
        current_user = assign_address_v3(current_user)
        print(current_user)
        print(current_user.ethereum_public_key)
        print("Address was assigned to current user.")

    # Deploy contract
    if(request.GET.get('deploy_contract_v3')):
        current_user = dev_user
        print(current_user.ethereum_private_key)
        contract_address = deploy_contract_v3(current_user.ethereum_private_key)
        print(current_user)
        print("Contract address:", contract_address)
        # associate dev_dataset with deployed contract
        dev_dataset.contract_address = contract_address
        print(dev_dataset.contract_address)


    # Publish Data of dev_dataset to Smart Contract
    if(request.GET.get('publish_data_v3')):
        current_user = dev_user
        current_contract = dev_dataset.contract_address
        # Publish metadata to contract
        tx_receipt = publish_data_v3(
                        provider_private_key = current_user.ethereum_private_key, 
                        contract_address     = current_contract, 
                        description          = dev_dataset.description, 
                        license              = dev_dataset.license)
        print("Transaction receipt:\n", tx_receipt)



    # Add data requester to Smart Contract
    if(request.GET.get('add_requester_v3')):
        current_user = dev_user
        current_contract = dev_dataset.contract_address
        # Add data requester
        tx_receipt = add_requester_v3(
                        requester_private_key= current_user.ethereum_private_key, 
                        contract_address     = current_contract,
                        license              = dev_dataset.license)
        print("Transaction receipt:\n", tx_receipt)


    # Update Smart Contract
    if(request.GET.get('update_contract_v3')):
        current_user = dev_user
        current_contract = dev_dataset.contract_address
        # Update contract
        tx_receipt = publish_data_v3(
                        provider_private_key = current_user.ethereum_private_key, 
                        contract_address     = current_contract, 
                        description          = dev_dataset.description)
        print("Transaction receipt:\n", tx_receipt)




# First iteration functions:
    if(request.GET.get('assign_address')):
        # Pass request into web3 script

        current_user = request.user
        current_user = assign_address(current_user)
        # Save already takes place while assigning address
        # current_user.save()
        print(current_user)
        print(current_user.ethereum_public_key)
        print("Address was assigned to current user.")


    if(request.GET.get('deploy_contract')):
        current_user = request.user
        contract_address = deploy_contract(current_user)
        print("Contract address:")
        print(contract_address)   

    if(request.GET.get('create_wallet')):
        create_wallet_old()

    if(request.GET.get('mybtn')):
        print("The input value is: ", int(request.GET.get('mytextbox')) ) # or any other function

    context = {}
    template = 'dev.html'
    return render(request, template, context)
    
"""