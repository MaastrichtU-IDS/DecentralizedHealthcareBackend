from datetime import datetime

from fastapi import APIRouter, Body, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, validator
from sqlalchemy.exc import IntegrityError, OperationalError
from sqlmodel import Field, Session, SQLModel, select
from brownie import accounts

from luce.config import settings, engine
from luce.users import User

from pydantic import BaseModel, Field
from typing import List, Optional

# Example for nested structures. You need to define these based on your actual model fields.
class Restrictions(BaseModel):
    no_restrictions: bool
    open_to_general_research_and_clinical_care: bool
    # Add other fields...

class GeneralResearchPurpose(BaseModel):
    use_for_methods_development: bool
    # Add other fields...

# Define similar classes for HMBResearchPurpose, ClinicalPurpose, etc.

# class ResearchPurpose(BaseModel):
#     general_research_purpose: GeneralResearchPurpose
#     HMB_research_purpose: HMBResearchPurpose
#     clinical_purpose: ClinicalPurpose
#     # Add other fields...

class ConsentContract(BaseModel):
    contract_address: str
    user_id: Optional[int]  # Assuming this is a foreign key to a user
    restrictions: Restrictions
    # Add other fields...

class DataContract(BaseModel):
    id: int
    user_id: int  # Assuming this is a foreign key to a user
    description: str
    licence: str
    contract_address: str
    consent_contract: ConsentContract
    # Add other fields...


class LuceRegistryContract(SQLModel, table=True):
    contract_address: Optional[str] = Field(default=None, primary_key=True)
    user: str = Field(foreign_key="user.email")

    def deploy(self):
        from brownie.project.BrownieProject import LUCERegistry

        # account[0] as the administrator
        contract = LUCERegistry.deploy({'from': accounts[0]})
        receipt = contract.tx
        if receipt.status == 1:
            self.contract_address = receipt.contract_address
            print("Deploy LUCERegistry contract succeeded")
        else:
            print("Deploy LUCERegistry contract failed")

        return receipt.status

    # def deploy_contract(self):
    #     tx_receipt = web3.deploy_registry(self.user)
    #     if type(tx_receipt) is list:
    #         return tx_receipt
    #     self.contract_address = tx_receipt["contractAddress"]
    #     return tx_receipt

    def is_registered(self, user, usertype):
        if usertype == 'requester':
            return self.is_registered_as_requester(user)

    def is_registered_as_requester(self, user):
        from brownie.project.BrownieProject import LUCERegistry
        result = LUCERegistry.at(self.contract_address).checkUser(
            user.ethereum_public_key)
        return result

        # isregistered = web3.is_registered(self, user, usertype)
        # return isregistered

    # def register_provider(self, user, estimate):
    #     tx = web3.register_provider(self, user, estimate)
    #     return tx

    def register_requester(self, user, license, estimate):
        from brownie.project.BrownieProject import LUCERegistry

        print("register_requester")
        print(license)

        sender = accounts.add(private_key=user.ethereum_private_key)
        result = LUCERegistry.at(self.contract_address).registerNewUser(
            user.ethereum_public_key, license, {'from': sender})
        return result


router = APIRouter()

# LUCE registry

class CreateLuceRegistry(BaseModel):
    estimate: bool = False

@router.post("/contract/deployRegistry", name="Deploy LUCE registry",
    description="Deploy LUCE registry",
    response_model=dict,
)
def deploy_luce_registry(createLuceRegistry: CreateLuceRegistry = Body(...)) -> dict:
    with Session(engine) as session:
        statement = select(User).where(User.email == settings.admin_email)
        user = session.exec(statement).first()
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")


    return createLuceRegistry.model_dump()


# Regular contracts

class CreateDataset(SQLModel, table=False):
    link: str = Field(primary_key=True)
    description: str


class Dataset(CreateDataset, table=True):
    created_at: datetime = datetime.now()

@router.post("/contract/dataUpload", name="Upload a dataset",
    description="Upload a dataset to the LUCE blockchain",
    response_model=dict,
)
def post_data_upload(createDataset: CreateDataset = Body(...)) -> dict:
    return createDataset.dict()
