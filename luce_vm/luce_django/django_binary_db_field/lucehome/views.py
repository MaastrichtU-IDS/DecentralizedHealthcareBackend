from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.http import is_safe_url

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

# Import Python web3 scripts
from utils.web3_scripts import create_wallet_old, fund_wallet, deploy_contract, assign_address
# Import newest versions of web3 scripts
from utils.web3_scripts import assign_address_v3, deploy_contract_v3, publish_data_v3, add_requester_v3, update_contract_v3


def home_page(request):
    head_title = "LUCE"
    # Get first five datasets
    qs = Dataset.objects.all()[:5]
    context = {"head_title": head_title, 
                "dataset_list": qs}
    template = 'home.html'
    return render(request, template, context)


# Class-Based Views for registration and login:
class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = '/register_login'

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
    