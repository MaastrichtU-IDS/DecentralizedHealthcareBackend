from django.shortcuts import render, get_object_or_404, redirect

# Generic update view
from django.views.generic.edit import UpdateView
from datastore.models import Dataset
from datastore.forms import DatasetModelForm

# Import Python web3 script
from utils.web3_scripts import assign_address_v3, deploy_contract_v3, publish_data_v3, add_requester_v3, update_contract_v3

def browse_view(request):
    head_title = "LUCE"
    # Get all datasets
    qs = Dataset.objects.all()
    qs = qs.published() # only show published datasets
    context = {"head_title": head_title, 
                "dataset_list": qs}
    template = 'data/browse.html'
    return render(request, template, context)


def my_data_view(request):
    head_title = "LUCE"
    qs = Dataset.objects.all()
    # Only datasets owned by current user
    qs = qs.filter(created_by=request.user)
    context = {"head_title": head_title, 
                "dataset_list": qs}
    template = 'data/my_data.html'
    return render(request, template, context)

def my_access_view(request):
    head_title = "LUCE"
    qs = Dataset.objects.all()
    # Only datasets current user has access to
    qs = qs.filter(access_granted=request.user)
    context = {"head_title": head_title, 
                "dataset_list": qs}
    template = 'data/my_access.html'
    return render(request, template, context)


def detail_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    context = {"dataset": obj,
                "user": request.user}
    template = 'data/detail.html'
    return render(request, template, context)  



def upload_view(request):
    form = DatasetModelForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # Obtain data from form
        obj = form.save(commit=False)
        # Add user attributes
        obj.owner = request.user
        obj.created_by = request.user
        obj.owner_address = request.user.ethereum_public_key

        # Save to database
        obj.save()

        # -> Data has been submitted and stored
        # Display a new, empty form
        form = DatasetModelForm()

        # Redirect to subsequent page
        return redirect(obj.get_absolute_url() + "/upload_success")
    context = {
            'form': form
                }
    template = 'data/upload.html'
    return render(request, template, context)

def upload_success_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    context = {"dataset": obj,
                "user": request.user}
    template = 'data/upload_success.html'
    return render(request, template, context)  


def update_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    form = DatasetModelForm(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        print("Form is valid")
        # Obtain data from form
        obj = form.save(commit=False)

        # Deploy new smart contract & retrieve contract address
        # contract_address = deploy_contract(request.user)
        # obj.contract_address = contract_address

        if obj.published:
            # Update ethereum contract
            tx_receipt = update_contract_v3(
                            provider_private_key = request.user.ethereum_private_key,
                            contract_address     = obj.contract_address,
                            description          = obj.description)

        # Save to database
        obj.save()

        return redirect('/data/'+ str(dataset_id) + '/update_success')
    else:
        print(form)
        print("Form is not valid")
    context = {
            'form': form,
            'dataset': obj,
                }
    template = 'data/update.html'
    return render(request, template, context)

def update_success_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    context = {"dataset": obj,
                "user": request.user}
    template = 'data/update_success.html'
    return render(request, template, context)  


def delete_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    if request.method == "POST":
        obj.delete()
        return redirect("/")
    context = {"dataset": obj}
    template = 'data/delete.html'
    return render(request, template, context)

def publish_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    if request.method == "POST":
        # Logic for publishing
        obj.published = True

        # Deploy smart contract & retrieve contract address
        contract_address = deploy_contract_v3(request.user.ethereum_private_key)
        
        # Add contract address to dataset
        obj.contract_address = contract_address

        # Publish metadata to smart contract
        tx_receipt = publish_data_v3(
                        provider_private_key = request.user.ethereum_private_key,
                        contract_address     = obj.contract_address,
                        description          = obj.description,
                        license              = obj.license)

        # Save dataset
        obj.save()

        # Redirect to subsequent view
        return redirect(obj.get_absolute_url() + "/publish_success")
    context = {"dataset": obj}
    template = 'data/publish.html'
    return render(request, template, context)

def publish_success_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    context = {"dataset": obj,
                "user": request.user}
    template = 'data/publish_success.html'
    return render(request, template, context)  

def request_access_view(request, dataset_id):
    obj = get_object_or_404(Dataset, id=dataset_id)
    if request.method == "POST":
        # Logic for access request
        # Add requester to smart contract
        tx_receipt = add_requester_v3(
                        requester_private_key= request.user.ethereum_private_key,
                        contract_address     = obj.contract_address,
                        license              = obj.license)

        # Grat access in Django db 
        obj.access_granted.add(request.user)
        obj.save()
        return redirect("/my_access/")
    context = {"dataset": obj}
    template = 'data/request_access.html'
    return render(request, template, context)
    
