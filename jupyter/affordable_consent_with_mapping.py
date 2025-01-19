from cgi import test
import dis
from distutils.command import build
import enum
import json

# import web3
from datetime import datetime
from tkinter import CURRENT
from matplotlib import hatch, markers
from matplotlib.font_manager import font_scalings
from pyparsing import alphas
from requests import get
from web3 import Web3

# import py_solc_x as px
import solcx
from web3.contract import Contract
import os
import pandas as pd
import logging
from pathlib import Path 
from tqdm import tqdm
from zmq import Enum
import re

from web3.middleware import geth_poa_middleware


CURRENT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path("data")
os.chdir(CURRENT_DIR)
# print("CURRENT_DIR", CURRENT_DIR)
# Configure the logger
# import logging
logger = logging.getLogger("affordable_consent")
logger.setLevel(logging.DEBUG)  # Set to the lowest level to capture all logs

# Create handlers for each log level
error_handler = logging.FileHandler("logs/affordable_consent_error.log", mode="w")
warning_handler = logging.FileHandler("logs/affordable_consent_warning.log", mode="w")
info_handler = logging.FileHandler("logs/affordable_consent_info.log", mode="w")
critical_handler = logging.FileHandler("logs/affordable_consent_critical.log", mode="w")
all_handler = logging.FileHandler("logs/affordable_consent_all.log", mode="w")
console_handler = logging.StreamHandler()

# Set level for each handler
error_handler.setLevel(logging.ERROR)
warning_handler.setLevel(logging.WARNING)
info_handler.setLevel(logging.INFO)
console_handler.setLevel(logging.DEBUG)  # Console can show all logs
critical_handler.setLevel(logging.CRITICAL)

# Create formatters and add them to handlers
formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)s - %(funcName)20s() ] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
error_handler.setFormatter(formatter)
warning_handler.setFormatter(formatter)
info_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)
critical_handler.setFormatter(formatter)
all_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(error_handler)
logger.addHandler(warning_handler)
logger.addHandler(info_handler)
logger.addHandler(console_handler)
logger.addHandler(critical_handler)
logger.addHandler(all_handler)

# Example usage
logger.error("This is an error message")
logger.warning("This is a warning message")
logger.info("This is an info message")
logger.debug("This is a debug message")
logger.critical("This is a critical message")

consent_fp = Path("solidity", "InformedConsentWithMapping.sol")


# consent_fp_relative = r"jupyter\\data\\UnifiedConsentModel.sol"
with open(consent_fp) as file:
    contract_source_code = file.read()

# Compile & Store Compiled source code
# print(contract_source_code)
solcx_version = "0.8.0"
# solcx_version = '0.5.16'
solcx.install_solc(solcx_version)
# compiled_sol = solcx.compile_source(source=contract_source_code,
#   solc_binary="/snap/bin/solc")
compiled_sol = solcx.compile_files(
    source_files=consent_fp,
    # solc_binary='/usr/bin/solc',
    # optimize_runs=200,
    output_values=["abi", "bin", "bin-runtime"],
    optimize=True,
    solc_version=solcx_version,
    # evm_version="byzantium",
)

print(compiled_sol.keys())
contract_interface = compiled_sol["solidity/InformedConsentWithMapping.sol:ConsentCode"]
abi = contract_interface["abi"]
bytecode = contract_interface["bin"]
bytecode_runtime = contract_interface["bin-runtime"]


class TestEnum(Enum):
    local = (1, "Local")
    polygon = (2, "Polygon")

    def __init__(self, code, name):
        self._code = code
        self._name = name

    @property
    def code(self):
        return self._code

    @property
    def name(self):
        return self._name


class Env:
    def __init__(self, name, w3, deployed_contract, accounts):
        self.name = name
        self.w3 = w3
        self.contract = deployed_contract
        self.accounts = accounts

def deploy_contract_local():
    startTime = datetime.now()
    # Use Ganache for web3 instance
    w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545", request_kwargs={"timeout": 120}))

    # Set pre-funded ganache account #0 as sender
    w3.eth.defaultAccount = w3.eth.accounts[0]
    logger.info(f"account numbers {len(w3.eth.accounts)}")
    # The default `eth.defaultAccount` address is used as the default "from" property for request_1_address dictionaries if no other explicit "from" property is specified.
    # Create contract blueprint
    deployed_contract = w3.eth.contract(abi=abi, bytecode=bytecode)
    # Submit the request_1_address that deploys the contract
    provider_address = w3.eth.accounts[0]
    provider_address_sum = Web3.to_checksum_address(provider_address)
    balance_provider = w3.eth.get_balance(provider_address)
    # print("balance_provider", balance_provider)

    tx_hash = deployed_contract.constructor().transact(
        {
            "from": provider_address,
            "gas": int(5e6),
            "gasPrice": w3.to_wei(5, "ether"),
            # "gaslimit": int(1e9),
        }
    )

    ### Obtain Transcation Receipt

    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120, poll_latency=0.1)
    assert tx_receipt["status"] == 1

    # logger.info("tx_receipt status", tx_receipt["status"])
    # We obtain the block number under which it is deployed
    # global contract_block
    contract_block = w3.eth.block_number
    logger.info(f"The contract is deployed with block number {contract_block} .")
    # With obtain the final address of the contract

    # global contract_address
    contract_address = tx_receipt.contractAddress
    contract_code = w3.eth.get_code(contract_address)

    # print("The contract has the address", contract_address)
    # print("contract_code ", contract_code)

    gas_limit = int(2e7)

    ### Interact with contract
    # Create python instance of deployed contract
    # caddress = '0x3FEAfC9084e95BC5B07FBbBd197Af22422A46019'
    deployed_contract = w3.eth.contract(
        address=contract_address,
        abi=abi,
        # bytecode=bytecode,
    )
    # Extract default accounts created by ganache
    used_accounts = get_used_address()
    accounts = set(map(lambda x:str(x), w3.eth.accounts))
    accounts = list(accounts - used_accounts)
    # logger.info(f"actural accounts {len(accounts)}, used accounts {len(used_accounts)}")
    # print(f" actural {accounts.pop()}, used {used_accounts.pop()}")
    env = Env(TestEnum.local.name, w3, deployed_contract, accounts)
    return env

private_key = "cef3155c18c010de238f98470f9a092159405cb6cd5ab25261e3fcdff23cd810"

def deploy_contract_polygon(force_deploy=False):

    # Connect to Polygon (Mumbai Testnet)
    pad = "https://polygon-amoy.drpc.org"
    rapt = "https://rpc-amoy.polygon.technology"
    w3 = Web3(
        provider=Web3.HTTPProvider(rapt),
        # middlewares=[geth_poa_middleware],
    )
    # https://rpc-amoy.polygon.technology
    w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    # w3.eth.set_provider(Web3.givenProvider)
    # Check if connected to Polygon
    if not w3.is_connected():
        raise Exception("Failed to connect to Polygon network")

    account = w3.eth.account.from_key(private_key)
    w3.eth.default_account = account.address
    # w3.middleware_onion.add(SignAndSendRawMiddlewareBuilder.build(account))
    # w3.setProvider(window.ethereum);
    # w3.eth. (private_key)

    if force_deploy:
        # Set the account to deploy the contract from

        logger.info(f"Deploying contract from account: {account.address}")

        # Create contract blueprint
        compiled_contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        # Build transaction
        transaction = compiled_contract.constructor().build_transaction(
            {
                "from": account.address,
                "nonce": w3.eth.get_transaction_count(account.address),
                "gas": int(2e6),
                "gasPrice": w3.eth.gas_price,
            }
        )
        estimated_gas = w3.eth.estimate_gas(transaction)

        # Update the transaction with the estimated gas
        transaction["gas"] = estimated_gas

        print(f"Estimated Gas: {estimated_gas}")

        # Sign transaction
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

        # Send transaction
        tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

        # Wait for transaction receipt
        tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
        assert tx_receipt['status'] == 1
        contract_address = tx_receipt.contractAddress 
        polygon_config = {"contract_address": contract_address}
        json.dump(polygon_config, open("data/polygon.json", "w"))
    else:
        polygon_config = json.load(open("data/polygon.json", "r"))
        contract_address = polygon_config.get("contract_address", None)

    # contract_address = w3.to_checksum_address(contract_address)
    deployed_contract = w3.eth.contract(address=contract_address, abi=abi, bytecode=bytecode)
    logger.critical(f"Contract deployed at address: {contract_address}")
    # print(f"Contract deployed at address: {contract_address}")
    env = Env(TestEnum.polygon.name,w3, deployed_contract, [w3.to_checksum_address(account.address)])
    return env 


pattern = r"^[A-Z][0-9\*]{2}$"
pattern_compiled = re.compile(pattern)
def diseaseCode2IntHierarchy(code: str):
    #  the code is a string like A00,B11, etc.
    #  return the int code for chapter, group as a tuple
    # print(f"code is {code}")
    if not pattern_compiled.match(code):
        print(f"The string {code} not matches the pattern")
        return 0
    group_str = code[0]
    # if chapter_str == "*":
    #     return 2**8-1,2**128-1
    group_int = int(ord(group_str) - ord("A")) + 1
    category_str = code[1:3]
    if category_str == "**":
        return group_int, 2**100 - 1
    chapter_int = 1 << int(category_str)
    # represent group_int as 128 bits
    return group_int, chapter_int


def diseaseCode2Int(code: str) -> int:
    # r = fx.UInt16(0)
    # print(bin(r))
    # since A00.0 is a correct code, so plus 1 for each level
    if not pattern_compiled.match(code):
        print(f"The string {code} not matches the pattern")
        return 0
    chapter_str = code[0]
    group_str = code[1:3]
    category_str = code[-1]
    result = 0
    if chapter_str == "*":
        return 0
        # chapter_int = 0
    else:
        chapter_int = int(ord(code[0]) - ord("A")) + 1
        b_chapter = (chapter_int) << 11

    if group_str == "**" or group_str == "*":
        return b_chapter
    else:
        group_int = int(code[1:3]) + 1
        b_group = (group_int) << 4

    # if category_str == "*":
    #     return b_chapter + b_group
    # else:
    #     category_int = int(code[-1]) + 1
    # return b_chapter + b_group + category_int
    return b_chapter + b_group


def int2DiseaseCode(code: int) -> str:
    if code == 0:
        return "*00.0"
    chapter_int = code >> 11
    chapter_str = chr(chapter_int + ord("A") - 1)
    group_int = (code >> 4) & 0b1111111
    group_str = str(group_int - 1).zfill(2)
    category_int = code & 0b1111
    category_str = str(category_int - 1)
    return f"{chapter_str}{group_str}.{category_str}"

import random

from enum import Enum, auto
import random
class ADAM(Enum):
    UseForMethodsDevelopment = 1
    UseForReferenceOrControlMaterial = 2
    UseForPopulationsResearch = 4
    UseForAncestryResearch = 8
    UseForHMBResearch = 16
    UseForFundamentalBioResearch = 32
    UseForGeneticsResearch = 64
    UseForDrugDevelopmentResearch = 128
    UseForAnyDiseaseResearch = 256
    UseForAgeCategoriesResearch = 512
    UseForGenderCategoriesResearch = 1024
    UseForDecisionSupport = 2048
    UseForDiseaseSupport = 4096
    UseByAcademicProfessionals = 8192
    UseByClinicalProfessionals = 16384
    UseByProfitMakingProfessionals = 32768
    UseByNonProfessionals = 65536
    UseBySpecifiedCountries = 131072
    UseForProfitPurpose = 262144
    # UseForNonProfitPurpose = 524288
    TimelineRestrictions = 1048576
    FormalApprovalRequired = 2097152
    CollaborationRequired = 4194304
    PublicationRequired = 8388608
    DataSecurityMeasures = 16777216
    DataDestructionRequired = 33554432
    LinkingOfAccessedRecords = 67108864
    RecontactingDataSubjects = 134217728
    IntellectualPropertyClaims = 268435456
    UseOfAccessedResources = 536870912
    FeesForAccess = 1073741824

ADAM_order_list = [ADAM.UseForMethodsDevelopment, ADAM.UseForReferenceOrControlMaterial, ADAM.UseForPopulationsResearch, ADAM.UseForAncestryResearch, ADAM.UseForHMBResearch, ADAM.UseForFundamentalBioResearch, ADAM.UseForGeneticsResearch, ADAM.UseForDrugDevelopmentResearch, ADAM.UseForAnyDiseaseResearch, ADAM.UseForAgeCategoriesResearch, ADAM.UseForGenderCategoriesResearch, ADAM.UseForDecisionSupport, ADAM.UseForDiseaseSupport, ADAM.UseByAcademicProfessionals, ADAM.UseByClinicalProfessionals, ADAM.UseByProfitMakingProfessionals, ADAM.UseByNonProfessionals, ADAM.UseBySpecifiedCountries, ADAM.UseForProfitPurpose, 
                #    ADAM.UseForNonProfitPurpose, 
                   ADAM.TimelineRestrictions, ADAM.FormalApprovalRequired, ADAM.CollaborationRequired, ADAM.PublicationRequired, ADAM.DataSecurityMeasures, ADAM.DataDestructionRequired, ADAM.LinkingOfAccessedRecords, ADAM.RecontactingDataSubjects, ADAM.IntellectualPropertyClaims, ADAM.UseOfAccessedResources, ADAM.FeesForAccess]

class DUO(Enum):
    Allow_All = 1
    OpenToGeneralResearchAndClinicalCare = 2
    OpenToHMBResearch = 4
    OpenToPopulationAndAncestryResearch = 8
    OpenToDiseaseSpecific = 16
    OpenToGeneticStudiesOnly = 32
    ResearchSpecificRestrictions = 64
    OpenToResearchUseOnly = 128
    GeneralMethodResearch = 256
    GeographicSpecificRestriction = 512
    OpenToNonProfitUseOnly = 1024
    PublicationRequired = 2048
    CollaborationRequired = 4096
    EthicsApprovalrequired = 8192
    TimeLimitOnUse = 16384
    CostOnUse = 32768
    DataSecurityMeasuresRequired = 65536

DUO_order_list = [DUO.Allow_All, DUO.OpenToGeneralResearchAndClinicalCare, DUO.OpenToHMBResearch, DUO.OpenToPopulationAndAncestryResearch, DUO.OpenToDiseaseSpecific, DUO.OpenToGeneticStudiesOnly, DUO.ResearchSpecificRestrictions, DUO.OpenToResearchUseOnly, DUO.GeneralMethodResearch, DUO.GeographicSpecificRestriction, DUO.OpenToNonProfitUseOnly, DUO.PublicationRequired, DUO.CollaborationRequired, DUO.EthicsApprovalrequired, DUO.TimeLimitOnUse, DUO.CostOnUse, DUO.DataSecurityMeasuresRequired]


role_provider = 1
role_requester = 2

# %%
from re import L
import time


import random
import icd10


def expand_code_range(code_range):
    # Split the range into start and end codes
    start_code, end_code = code_range.split("-")

    # Extract letters and numbers
    start_letter, start_number = start_code[0], int(start_code[1:])
    end_letter, end_number = end_code[0], int(end_code[1:])
    # print(f"start_letter {start_letter}, start_number {start_number}")
    # print(f"end_letter {end_letter}, end_number {end_number}")

    # Initialize variables
    codes = []
    current_letter = start_letter
    current_number = start_number

    # Loop until the current code matches the end code
    while current_letter <= end_letter:
        while current_number <= 99:  # Maximum number in the range
            # Add the current code to the list
            codes.append(f"{current_letter}{current_number:02}")
            if current_letter == end_letter and current_number == end_number:
                break  # Stop if the end code is reached
            current_number += 1  # Increment the number part

        # Reset for the next letter if not yet at the end
        # if current_letter < end_letter:
        current_letter = chr(ord(current_letter) + 1)  # Move to the next letter
        current_number = 0  # Reset number to 0 for the next letter

    return codes


# disease_list = []
disease_dict = {}
for c in icd10.chapters:
    codes = expand_code_range(c[1])
    for code in codes:
        letter = code[0]
        if letter not in disease_dict:
            disease_dict[letter] = []
        disease_dict[letter].append(code)

disease_list = [item for sublist in disease_dict.values() for item in sublist]

country_name_code_dict = json.load(open("data/countries_enrich.json", "r"))

for k in country_name_code_dict.keys():
    country_name_code_dict[k]["position_index"] = 2 ** country_name_code_dict[k]["index"]

group_index_dict = json.load(open("data/group_index.json", "r"))
country_index_dict = json.load(open("data/country_index.json", "r"))
# allowed_group_names = {"EUROPEAN_UNION"}

group_order_index_dict = {
    name: index for index, name in enumerate(group_index_dict.keys())
}

country_code_name_dict = {v["index"]: k for k, v in country_name_code_dict.items()}

all_countries_name = list(country_name_code_dict.keys())

all_group_names = list(group_index_dict.keys())

def decode_country_code(country_code: int):
    countries = []
    for name, index in country_index_dict.items():
        if index & country_code:
            countries.append(name)
    return countries

def decode_group_code(group_code: int):
    groups = []
    for k, v in group_index_dict.items():
        if v & group_code:
            groups.append(k)
    return groups

class TransactionResult:
    def __init__(self, status=0, gas_used = 0, transaction_hash="", time_used=0,result=None, gas_price=0):
        self.status = status
        self.gas_used = gas_used
        self.transaction_hash = transaction_hash
        self.time_used = time_used
        self.result = result
        self.gas_price = gas_price

    def to_dict(self):
        return {
            "status": self.status,
            "gas_used": self.gas_used,
            "transaction_hash": self.transaction_hash,
            "time_used": self.time_used,
            "result": self.result
        }

    # @property
    def __json__(self):
        return json.dumps(self.__dict__())

    def __str__(self):
        return f"status {self.status}, gas_used {self.gas_used}, transaction_hash {self.transaction_hash}, time_used {self.time_used}, result {self.result}"

class Person:
    def __init__(
        self,
         env  ,
        name="",
        description="",
        address=None,
        bool_items=None,
        country_names=['*'],
        group_names=[],
        disease_items=['*'],
        start_year=2021,
        start_month=1,
        start_day=1,
        months=12,
        **kwargs,
    ):

        self.name = name
        self.estimate_gas = False
        self.print_time = False
        self.w3 = env.w3
        self.env = env 

        if address is not None:

            self.address = address

            # balance = w3.eth.get_balance(address)
        else:
            self.address = env.accounts.pop()

            # print(f"balance of {address} is {balance}")

        self.bool_items = bool_items

        self.description = description

        self.contract = env.contract

        # 'gasPrice': w3.eth.gas_price*0.1,

        # print(f"person_dict {self.person_dict}")
        self.debug = False
        self.disease_items = disease_items
        self.disease_groups= []
        self.country_names = country_names
        self.group_names = group_names
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.months = months

    def random_init(self, profile_dict):
        # if risk_level is not None:
        self.months = profile_dict["months"]

        # while True:
        #     disease_list = disease_dict[random.choice(string.ascii_uppercase)]
        #     if len(disease_list) > 0:
        #         break
        if profile_dict["disease_items"] == 1:
            self.disease_items = ["*"]
        else:
            while True:
                disease_list = disease_dict[random.choice(string.ascii_uppercase)]
                if len(disease_list) > 0:
                    break

            self.disease_items = random.choices(
                disease_list,
                k=int(profile_dict["disease_items"] * len(disease_list)),
            )
            self.disease_groups = random.choices(
                string.ascii_uppercase, k=int(profile_dict["disease_items"] * 26)
            )

        self.country_names = random.sample(
            all_countries_name,
            k=int(profile_dict["country_code"] * len(all_countries_name)),
        )

        self.group_names = random.sample(
            all_group_names,
            k=int(profile_dict["group_code"] * len(all_group_names)),
        )

    # display_simple_items
    def display_simple_items(self):

        func = self.contract.functions.DisplaySimpleItems(self.role, self.address)

        if self.estimate_gas:

            gas = func.estimate_gas()

            logging.info(f"Estimated gas cost for displaySimpleItems: {gas}")

        result = func.call()

        boolItems = PurposeItems()

        boolItems.decode_from_int(result)

        print(f"{self.name} displaySimpleItems is {boolItems.show_true_items()}")

    def delete_area(self):
        country_codes = [country_name_code_dict[c]["index"] for c in self.country_names]

        # print("UploadCountryItems", country_codes)
        if hasattr(self, "group_names"):
            group_codes = [group_index_dict[g] for g in self.group_names]
        else:
            group_codes = []

        func = self.contract.functions.delete_area_baseline(
            self.role,
            self.address,
            group_codes,
            country_codes,
        )
        # self.send_transaction(func)

        return self.send_transaction(func)

    def upload_area_baseline(self):

        country_codes = [
            country_name_code_dict[c]["index"] for c in self.country_names
        ]

        # print("UploadCountryItems", country_codes)
        if hasattr(self, "group_names"):
            group_codes = [group_index_dict[g] for g in self.group_names]
        else:
            group_codes = []
        # group_codes = [group_order_index_dict[g] for g in self.group_names]
        # logger.info(f"country_codes {country_codes} group_codes {group_codes}")
        # if test_mode == TestEnum.polygon:

        func = self.contract.functions.UploadAreaBaseline(
            self.role,
            self.address,
            group_codes,
            country_codes,
        )

        # print("UploadAreaCode role", self.role)

        return self.send_transaction(func)

    def update_area_group_relation(self):

        country_group_dict = {}

        for country_name, country_dict in country_name_code_dict.items():

            groups = country_dict["groups"]

            if len(groups) == 0:

                continue

            for g in groups:

                if g not in group_index_dict:
                    continue

                g_index = group_index_dict[g]

                if g_index not in country_group_dict:

                    country_group_dict[g_index] = 0

                country_group_dict[g_index] |= country_dict["index"]

        country_group_data = list(country_group_dict.values())

        country_group_index = list(country_group_dict.keys())

        # print("country_group_dict", country_group_dict)

        func = self.contract.functions.UpdateCountryGroupRelation(
            country_group_data, country_group_index
        )

        # func.transact(self.person_dict)

        return self.send_transaction(func, label="update_area_group_relation")

    def update_area_group_code_baseline(self, part_number=20):

        def split(a, n):

            k, m = divmod(len(a), n)

            return tuple(
                a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
            )

        country_group_dict = {}

        for c in self.country_names:

            if c not in self.country_name_code_dict:

                print(f"{c} not in country_dict")

                return

            country_dict = self.country_name_code_dict[c]

            country_group_dict[country_dict["index"]] = [
                self.group_order_index_dict[g] for g in country_dict["groups"]
            ]

        country_code_list = list(country_group_dict.keys())

        country_group_index_list = list(country_group_dict.values())

        country_number = len(country_code_list)

        # print("country_group_dict", country_group_dict)

        country_code_list_part = split(country_code_list, part_number)

        country_group_index_list_part = split(country_group_index_list, part_number)

        gas = 0

        for i in range(part_number):

            func = self.contract.functions.UpdateAreaBaseline(
                country_code_list_part[i], country_group_index_list_part[i]
            )

            func_gas = func.estimate_gas()

            gas += func_gas
        return gas

    def upload_area_affordable(self) -> TransactionResult:

        if "*" in self.country_names:

            func = self.contract.functions.UploadAreaAffordable(
                self.role, self.address, True, 0, 0
            )
            # logger.debug("allow all countries")

            return self.send_transaction(func)

        country_codes = [
            country_index_dict[c] for c in self.country_names
        ]
        if hasattr(self, "group_names") and self.group_names is not None and len(self.group_names) > 0:

            group_codes = [group_index_dict[g] for g in self.group_names]
            group_code = sum(group_codes)
        else:
            # logger.debug(f"do not have group_names")
            group_code = 0
        country_code = sum(country_codes)

        # decoded_countries = decode_country_code(country_code)
        # missed_countries = set(self.country_names) - set(decoded_countries)
        # if len(missed_countries) > 0:
        #     logger.error(f"missed_countries {missed_countries}")
        # print("country_group_data length", len(country_group_data))

        # logger.info(
        #     f"upload_area_affordable role {self.role}, address {self.address}, group_code {group_code}, country_code {country_code}"
        # )
        # print(f"upload_area_affordable role {self.role}, address {self.address}, group_code {group_code}, country_code {country_code}")

        func = self.contract.functions.UploadAreaAffordable(
            self.role, self.address, False, group_code, country_code
        )

        # print("UploadAreaCode role", self.role)

        return self.send_transaction(func)

    def display_area_affordable(self):
        group_code, country_code, version, Allow_all_area = (
            self.contract.functions.DisplayAreaAffordable(self.role, self.address).call()
        )
        countries = decode_country_code(country_code)
        groups = decode_group_code(group_code)

        return groups, countries

    def display_area_codes(self):
        (
            Group_Code,
            Country_Codes,
            Country_Group_Codes,
        ) = self.contract.functions.DisplayAreaCode(self.role, self.address).call()

        # groupp_code is a int of the sum of the value of group_index_dict, decode it according to the group_index_dict

        group_names = []

        for k, v in self.group_index_dict.items():

            if v & Group_Code:

                group_names.append(k)

        # print("displayAreaCodes", Country_Codes)

        # print("Country_Group_Codes", Country_Group_Codes)

        country_names = [self.country_code_name_dict[c] for c in Country_Codes]

        result = {"group_names": group_names, "country_codes": country_names}

        logging.info(f"displayAreaCodes is {result}")

    def upload_purpose_items(self):
        raise NotImplementedError("upload_purpose_items")

    def upload(self):
        self.upload_purpose_items()

        self.upload_area_affordable()

        self.upload_disease_affordable()
        self.upload_date()

    def delete_disease(self):
        func = self.contract.functions.delete_disease_baseline(
            self.role, self.address, [diseaseCode2Int(d) for d in self.disease_items]
        )
        return self.send_transaction(func)

    def upload_disease_baseline(self):

        disease_codes = [diseaseCode2Int(d) for d in self.disease_items]

        func = self.contract.functions.UploadDiseaseBaseline(
            self.role, self.address, disease_codes
        )

        return self.send_transaction(func)

    def upload_disease_affordable(self):

        if "*" in self.disease_items:

            func = self.contract.functions.UploadDiseaseAffordable(
                self.role, self.address, True, 0, []
            )
            # logger.debug("allow all disease")

            return self.send_transaction(func)

        disease_codes = [diseaseCode2IntHierarchy(d) for d in self.disease_items]
        # print(f"name {self.name}  disease_codes {disease_codes} ")
        disease_dict = {}

        for group_code, chapter_code in disease_codes:
            if group_code not in disease_dict:
                disease_dict[group_code] = 0

            disease_dict[group_code] |= chapter_code

        # disease_group_codes, disease_chapter_codes = (
        #     list(self.disease_dict.keys()),
        #     list(self.disease_dict.values()),
        # )
        disease_group_codes = [1 << (ord(d) - ord("A") + 1) for d in self.disease_groups]
        disease_group_code = sum(disease_group_codes)

        disease_combined_codes = [(1<< (group_code+100)) + chapter_code for group_code,chapter_code in disease_dict.items()]
        # print(f"name {self.name} disease_dict {disease_dict}")
        # print(f"name {self.name} disease_group_code {disease_group_code} disease_combined_codes {disease_combined_codes}")
        max_code = 1<<128
        for code in disease_combined_codes:
            if code > max_code:
                print(
                    f"code {code} larger than 2**128 disease_dict {disease_dict}, self.disease_items {self.disease_items}"
                )
            # print(f"code {code} disease_code {int2DiseaseCode(code)}")
        # logger.info(f"disease_group_code {disease_group_code} disease_combined_codes {disease_combined_codes}")
        func = self.contract.functions.UploadDiseaseAffordable(
            self.role,
            self.address,
            False,
            disease_group_code,
            disease_combined_codes
        )

        return self.send_transaction(func)

    def refresh_state(self):
        func = self.contract.functions.RefreshState(self.address)
        return self.send_transaction(func)

    def display_disease_items(self):

        disease_codes = self.contract.functions.DisplayDiseaseCode(
            self.role, self.address
        ).call()

        disease_names = []

        for d in disease_codes:

            disease_names.append(int2DiseaseCode(d))

        result = {"disease_names": disease_names}

        logging.info(f"displayDiseaseItems is {result}")

    def upload_date(self):

        try:

            func = self.contract.functions.UploadDate(
                self.role,
                self.address,
                self.start_year,
                self.start_month,
                self.start_day,
                self.months,
            )

        except Exception as e:
            print(f"error in upload_date {e}")
            logger.error(
                f"error in upload_date, role {self.role}, address {self.address}, start_year {self.start_year}, start_month {self.start_month}, start_day {self.start_day}, months {self.months}"
            )

        return self.send_transaction(func)

        # return self.forward(func)

    def display_date(self):

        (
            Start_Year,
            Start_Month,
            Start_Day,
            Months,
        ) = self.contract.functions.DisplayDate(self.role, self.address).call()

        print(
            f"displayDate: Start_Year is {Start_Year}, Start_Month is {Start_Month}, Start_Day is {Start_Day}, Months {Months}"
        )

        return Start_Year, Start_Month, Start_Day, Months

    def display_disease_herarchical(self):
        categories, codes, allow_all = (
            self.contract.functions.DisplayDiseaseCodeHierarchy(
                self.role, self.address
            ).call()
        )
        return categories, codes, allow_all

    def send_transaction(self, func, call=False, label=""):
        # if self.estimate_gas:
        #     gas = func.estimate_gas()
        #     return TransactionResult(gas_used=gas)
        # else:
        person_dict = {
            "from": self.address,
            # "nonce": w3.eth.get_transaction_count(self.address) + 1,
            "to": self.contract.address,
            # "value": w3.to_wei(0.1, "ether"),
            # "gas": w3.eth.gas_price,
            # "gas": w3.to_wei(10, "gwei"),
            # "gas": 1000000,
            # "chainId": 80002,
            "gasPrice": self.w3.to_wei(10, "gwei"),
        }
        dynamic_fee_transaction = {
            "from": self.address,
            "type": 2,  # Explicitly specify EIP-1559 transaction type
            "gas": 25_000_000,  # Ensure gas limit is reasonable
            "maxFeePerGas": self.w3.to_wei(40, "gwei"),  # Reasonable max fee per gas
            "maxPriorityFeePerGas": self.w3.to_wei(
                30, "gwei"
            ),  # Reasonable max priority fee per gas
            "nonce": self.w3.eth.get_transaction_count(
                self.address
            ),  # Correct nonce calculation
            "chainId": 80002,
        }
        receipt = None
        if call:
            start_time = time.time_ns()
            receipt = func.call()
            end_time = time.time_ns()
            time_diff = end_time - start_time
            return TransactionResult(time_used=time_diff, result=receipt)
        elif self.env.name == TestEnum.polygon.name:
            start_time = time.time_ns()
            build_transaction = func.build_transaction(dynamic_fee_transaction)
            signed_txn = self.w3.eth.account.sign_transaction(
                build_transaction, private_key=private_key
            )
            start_time = time.time_ns()
            # logger.info(f"signed_txn {signed_txn}")
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            end_time = time.time_ns()

        elif self.env.name == TestEnum.local.name:
            start_time = time.time_ns()
            tx_hash = func.transact(person_dict)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            end_time = time.time_ns()

        # logger.info(f"receipt {receipt}")
        gas_used = receipt["gasUsed"]
        gas_price = receipt["effectiveGasPrice"]
        time_diff = (end_time - start_time)
        return TransactionResult(gas_used=gas_used, time_used=time_diff, gas_price=gas_price, transaction_hash=receipt["transactionHash"].hex(), status=receipt["status"])

    def __str__(self):
        return f"Person: {self.name},  {self.description}, {self.role}"


import string

profile_strict = "strict"
profile_medium = "medium"
profile_open = "open"


class Provider(Person):

    # def __init__(self):

    #     # super().__init__(*args,**kwargs)

    profiles = {
        "strict": {
            "simple_items": 0.2,
            "group_code": 0.2,
            "country_code": 0.2,
            "disease_items": 0.2,
            "disease_groups": random.uniform(0, 0.2),
            "months": 6,
        },
        "medium": {
            "simple_items": 0.5,
            "group_code": 0.5,
            "country_code": 0.5,
            "disease_items": 0.5,
            "disease_groups": random.uniform(0, 0.5),
            "months": 12,
        },
        "open": {
            "simple_items": 0.8,
            "group_code": 0.8,
            "country_code": 0.8,
            "disease_items": 0.8,
            "disease_groups": random.uniform(0, 0.8),
            "months": 2**8 - 1,
        },
    }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.role = role_provider

        # risk_level = kwargs.get("risk_level", None)
        random_init = kwargs.get("random_init", False)
        if random_init:
            self.profile = kwargs.get("profile", "medium")

            profile_dict = self.profiles[self.profile]
            self.random_init(profile_dict)

            self.bool_items = set()
            for item in DUO:
                if random.random() < profile_dict['simple_items']:
                    self.bool_items.add(item)

            if self.profile == profile_open:
                self.start_year = 2020
            else:
                self.start_year = random.randint(2023, 2025)

            self.start_month = random.randint(1, 12)

            self.start_day = random.randint(1, 28)

            logger.info(
                f"{self.name}  country_names {self.country_names} group_names {self.group_names} disease_items {self.disease_items} start_year {self.start_year} start_month {self.start_month} start_day {self.start_day} months {self.months} bool_items {self.bool_items}"
            )

    def upload_purpose_items(self):
        simple_value = [True if item in self.bool_items else False for item in DUO_order_list]

        # logging.info(
        #     f"name {self.name} role {self.role}, address {self.address}, bool_items {simple_value}"
        # )

        upload_func = self.contract.functions.uploadPurposeProvider(
            self.address, simple_value
        )

        return self.send_transaction(upload_func)

    def get_purpose_items(self):
        duo_list = self.contract.functions.GetPurposeItemsProvider(self.address).call()
        result_set = set()
        for result_item, duo_item in zip(duo_list, DUO_order_list):
            if result_item:
                result_set.add(duo_item)
        return result_set


# p = Person("test", "test", contract, address=w3.eth.accounts[1])


# recipe = p.update_area_group_code()


# assert recipe["status"] == 1

# %% [markdown]
# ## Requester
#

# %%
# import dis


# area_error_code = 1
# disease_error_code = 2
# date_error_code = 4
# simple_error_code = 8

# area_error = "area_error"
# disease_error = "disease_error"
# date_error = "date_error"
# purpose_error = "_error"


class AccessError(Enum):
    AREA_ERROR = (1, "area_error")
    DISEASE_ERROR = (2, "disease_error")
    DATE_ERROR = (4, "date_error")
    PURPOSE_ERROR = (8, "purpose_error")

    @property
    def code(self):
        return self.value[0]

    @property
    def message(self):
        return self.value[1]

    def __str__(self):
        return self.message


class Requester(Person):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = role_requester
        random_init = kwargs.get("random_init", False)
        if random_init:
  
            # logger.info(f"{self.name} bool_items is {self.bool_items.to_int()}")
            profile_dict = {
                "simple_items": random.uniform(0, 0.2),
                "group_code": random.uniform(0, 0.05),
                "country_code": random.uniform(0, 0.05),
                "disease_items": random.uniform(0, 0.03),
                "disease_groups": random.uniform(0, 0.05),
                "months": random.randint(1, 24),
            }
            # profile_dict = self.profiles[self.profile]
            # self.random_init(profile_dict)
            self.random_init(profile_dict)

            self.bool_items = set()
            for item in DUO:
                if random.random() < profile_dict['simple_items']:
                    self.bool_items.add(item)

            self.start_year = random.randint(2024, 2025)
            self.start_month = random.randint(1, 12)
            self.start_day = random.randint(1, 28)
            # self.months = random.randint(1, 24)
            # generate icd-10 codes
            # logger.info(                f"{self.name}  country_names {self.country_names} group_names {self.group_names} disease_items {self.disease_items} start_year {self.start_year} start_month {self.start_month} start_day {self.start_day} months {self.months} bool_items {self.bool_items}" )

   

    def _check_role(self, provider: Provider):

        if provider.role != role_provider:

            raise Exception("requestAccess: provider is not a Provider")

        if self.role != role_requester:

            raise Exception("requestAccess: requester is not a Requester")

    def upload_purpose_items(self):
        simple_value = [True if item in self.bool_items else False for item in ADAM_order_list]
        # logging.info(
        #     f"name {self.name} role {self.role}, address {self.address}, bool_items {simple_value}"
        # )

        upload_func = self.contract.functions.uploadPurposeRequester(
            self.address, simple_value
        )

        return self.send_transaction(upload_func)

    def get_purpose_items(self):
        duo_list = self.contract.functions.GetPurposeItemsRequester(self.address).call()
        result_set = set()
        for result_item, duo_item in zip(duo_list, ADAM_order_list):
            if result_item:
                result_set.add(duo_item)
        return result_set

    def request_access(self, provider: Provider):

        if provider.role != role_provider:

            print("requestAccess: provider is not a Provider")
            return

        if self.role != role_requester:

            print("requestAccess: requester is not a Requester")
            return

        func = self.contract.functions.AccessData(provider.address, self.address)

        result = self.send_transaction(func, True).result 
        result_set = set()
        for error in AccessError:
            if result & error.code:
                result_set.add(error.message)
        return result_set

    def access_disease(self, provider: Provider):

        if provider.role != role_provider:

            print("requestAccess: provider is not a Provider")
            return

        if self.role != role_requester:

            print("requestAccess: requester is not a Requester")
            return

        func = self.contract.functions.CheckDisease(provider.address, self.address)

        return self.send_transaction(func, True)

    def access_disease_hierarchy(self, provider: Provider):

        if provider.role != role_provider:

            print("requestAccess: provider is not a Provider")
            return

        if self.role != role_requester:

            print("requestAccess: requester is not a Requester")
            return

        func = self.contract.functions.CheckDiseaseHierarchy(
            provider.address, self.address
        )

        return self.send_transaction(func, True)

    def access_area_baseline(self, provider: Provider):

        if provider.role != role_provider:

            print("requestAccess: provider is not a Provider")
            return

        if self.role != role_requester:

            print("requestAccess: requester is not a Requester")
            return

        func = self.contract.functions.CheckAreaBaseline(provider.address, self.address)

        return self.send_transaction(func, True)

    def access_area_simple(self, provider: Provider):

        self._check_role(provider)

        func = self.contract.functions.CheckAreaSimple(provider.address, self.address)

        return self.send_transaction(func, True)

    def access_boolean_items(self, provider: Provider):

        self._check_role(provider)

        func = self.contract.functions.CheckBooleanItems(provider.address, self.address)

        result = func.call()

        # result = func.call({"from": provider_address_sum})

        # print(f"access_boolean_items is {result}")

        # print(self.contract.functions.CheckBooleanItems)

        # func.call(block_identifier="latest")
        return result

def record_used_address(address):
    with open("data/used_address.txt", "a") as f:
        f.write(f"{address}\n")

def get_used_address():
    if not os.path.exists("data/used_address.txt"):
        logger.info("used_address.txt does not exist")
        return set()
    with open("data/used_address.txt", "r") as f:
        used_address = f.readlines()
        
    return set(map(lambda x: x.strip(), used_address))

def test_disease(env,one_group=False):
    provider1 = Provider(
        env,
        name="Provider_disease",
        description="Provider1",
        # address=random.choice(accounts),

    )
    requester1 = Requester(
        env,
        name="Requester_disease",
        description="Requester1",
        # address=random.choice(accounts),
  
    )

    # intevals = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70,80,90,100]
    # intevals = [80]
    # intevals = [1]
    intevals = [0,20,40,60,80,100]

    disease_data = []
    groups = [c for c in string.ascii_uppercase]
    if one_group:
        disease_list_all = disease_dict["A"]
    else:
        disease_list_all = disease_list

    for interval in tqdm(intevals):
        # disease_items = generate_disease_items(groups=groups, number=interval)
        choiced_number = int(interval / 100 * len(disease_list_all))    
        disease_items = random.choices(disease_list_all, k=max(1, choiced_number))
        # disease_items = disease_list_all[0] if len(disease_items) == 0 else disease_items
        provider1.disease_items = disease_items
        requester1.disease_items = disease_items
        if env.name == TestEnum.polygon.name:
            provider1.delete_disease()
            requester1.delete_disease()
        else:
            provider1.address = env.accounts.pop()
            requester1.address = env.accounts.pop()
            record_used_address(provider1.address)
            record_used_address(requester1.address)

        result_provider_baseline = provider1.upload_disease_baseline()
        result_requester_baseline = requester1.upload_disease_baseline()
        # gas_access = requester1.request_access(provider1)

        result_provider_affordable = provider1.upload_disease_affordable()
        result_requester_affordable = requester1.upload_disease_affordable()
        # gas_access_disease = requester1.access_disease(provider1)
        # gas_access_binary = requester1.access_disease_hierarchy(provider1)

        disease_data.append(
            {
                "interval": interval,
                "affordable": {
                    "provider": result_provider_affordable.to_dict(),
                    "requester": result_requester_affordable.to_dict(),
                },
                "baseline": {
                    "provider": result_provider_baseline.to_dict(),
                    "requester": result_requester_baseline.to_dict(),
                },
            }
        )

    result_fp = (
        f"result/{env.name}_disease_{'one' if one_group else 'whole'}.json"
    )

    json.dump(disease_data, open(result_fp, "w"), indent=4)


def plot_disease(one_group=False, test_mode=TestEnum.local):
    task = f'{test_mode.name}_disease_{"one" if one_group else "whole"}'
    result_fp = f"result/{task}.json"
    result_one_group = json.load(open(f"result/{test_mode.name}_disease_one.json", "r"))
    result_whole_group = json.load(open(f"result/{test_mode.name}_disease_whole.json", "r"))
    disease_data = result_whole_group
    provider_data = {
        "baseline": [d["gas_provider_baseline"]["gas_used"] for d in disease_data],
        "affordable": [d["gas_provider_affordable"]["gas_used"] for d in disease_data],
        "interval": [d["interval"] for d in disease_data],
    }
    requester_data = {
        "baseline": [d["gas_requester_baseline"]["gas_used"] for d in disease_data],
        "affordable": [d["gas_requester_affordable"]["gas_used"] for d in disease_data],
        "interval": [d["interval"] for d in disease_data],
    }
    plot_line_combined(data = provider_data, task= task, role = "provider", x_label="Precentage of diseases (%)", y_label="Gas Usage (10^3)")
    plot_line_combined(data = requester_data, task= task, role="requester", x_label="Precentage of diseases (%)", y_label="Gas Usage (10^3)")


def plot_disease_all(key_index_name="time_used",factor = 1e3 ):
    task = f'{test_mode.name}_disease'
    # result_fp = f"result/{task}.json"
    result_one_local = json.load(
        open(f"result/{TestEnum.local.name}_disease_one.json", "r")
    )
    result_whole_local = json.load(
        open(f"result/{TestEnum.local.name}_disease_whole.json", "r")
    )
    result_one_polygon = json.load(open(f"result/{TestEnum.polygon.name}_disease_one.json", "r"))
    result_whole_polygon = json.load(open(f"result/{TestEnum.polygon.name}_disease_whole.json", "r"))
    used_interval = [0,  20,  40,  60,  80, 100]
    result_one_local = [d for d in result_one_local if d["interval"] in used_interval]
    result_whole_local = [d for d in result_whole_local if d["interval"] in used_interval]
    result_one_polygon = [d for d in result_one_polygon if d["interval"] in used_interval]
    result_whole_polygon = [d for d in result_whole_polygon if d["interval"] in used_interval]

    affordable_provider_one_local = plot_transform(result_one_local, "provider", key_index_name, label="_local")
    affordable_requester_one_local = plot_transform(result_one_local, "requester", key_index_name,label="_local")
    affordable_provider_whole_local = plot_transform(result_whole_local, "provider", key_index_name, label="_local")
    affordable_requester_whole_local = plot_transform(result_whole_local, "requester", key_index_name, label="_local")
    affordable_provider_one_polygon = plot_transform(result_one_polygon, "provider", key_index_name, label="_polygon")
    affordable_requester_one_polygon = plot_transform(
        result_one_polygon, "requester", key_index_name, label="_polygon"
    )
    affordable_provider_whole_polygon = plot_transform(
        result_whole_polygon, "provider", key_index_name, label="_polygon"
    )
    affordable_requester_whole_polygon = plot_transform(
        result_whole_polygon, "requester", key_index_name, label="_polygon"
    )

    baseline_provider_one_local = plot_transform(result_one_local, "provider", key_index_name, label="_local")
    baseline_requester_one_local = plot_transform(result_one_local, "requester", key_index_name, label="_local")

    baseline_provider_whole_local = plot_transform(
        result_whole_local, "provider", key_index_name, label="_local"
    )
    baseline_requester_whole_local = plot_transform(
        result_whole_local, "requester", key_index_name, label="_local"
    )
    baseline_provider_one_polygon = plot_transform(result_one_polygon, "provider", key_index_name, label="_polygon")
    baseline_requester_one_polygon = plot_transform(
        result_one_polygon, "requester", key_index_name, label="_polygon"
    )
    baseline_provider_whole_polygon = plot_transform(
        result_whole_polygon, "provider", key_index_name, label="_polygon"
    )
    baseline_requester_whole_polygon = plot_transform(
        result_whole_polygon, "requester", key_index_name, label="_polygon"
    )

    # provider_data = {**baseline_provider_whole_local, **affordable_provider_whole_local, **baseline_provider_whole_polygon, **affordable_provider_whole_polygon}
    # requester_data = {**affordable_requester_one_local, **baseline_requester_one_local, **affordable_requester_one_polygon, **baseline_requester_one_polygon}
    provider_whole = {**baseline_provider_whole_local, **affordable_provider_whole_local, **baseline_provider_whole_polygon, **affordable_provider_whole_polygon}
    requester_whole = {**affordable_requester_whole_local, **baseline_requester_whole_local, **affordable_requester_whole_polygon, **baseline_requester_whole_polygon}
    provider_one = {**baseline_provider_one_local, **affordable_provider_one_local, **baseline_provider_one_polygon, **affordable_provider_one_polygon}
    requester_one = {**affordable_requester_one_local, **baseline_requester_one_local, **affordable_requester_one_polygon, **baseline_requester_one_polygon}
    y_label = "Gas Usage ($1 \\times 10^3$)"

    plot_column(
        data=provider_whole,
        task=f"all_whole_disease_{key_index_name}",
        role="provider",
        x_label="Precentage of diseases (%)",
        y_label=y_label,factor=factor,
    )
    plot_column(
        data=requester_whole,
        task=f"all_whole_disease_{key_index_name}",
        role="requester",
        x_label="Precentage of diseases (%)",
        y_label=y_label,
        factor=factor,
    )
    plot_column(
        data=provider_one,
        task=f"all_one_disease_{key_index_name}",
        role="provider",
        x_label="Precentage of diseases (%)",
        y_label=y_label,factor=factor,
    )
    plot_column(
        data=requester_one,
        task=f"all_one_disease_{key_index_name}",
        role="requester",
        x_label="Precentage of diseases (%)",
        y_label=y_label,factor=factor,
    )


def plot_disease_time(key_index_name="time_used", factor=1e6, y_label = "Time Usage (milliseconds)"):
    task = f"{test_mode.name}_disease"
    # result_fp = f"result/{task}.json"
    result_one_local = json.load(
        open(f"result/{TestEnum.local.name}_disease_one.json", "r")
    )
    result_whole_local = json.load(
        open(f"result/{TestEnum.local.name}_disease_whole.json", "r")
    )
    result_one_polygon = json.load(
        open(f"result/{TestEnum.polygon.name}_disease_one.json", "r")
    )
    result_whole_polygon = json.load(
        open(f"result/{TestEnum.polygon.name}_disease_whole.json", "r")
    )
    used_interval = [0, 20, 40, 60, 80, 100]
    result_one_local = [d for d in result_one_local if d["interval"] in used_interval]
    result_whole_local = [
        d for d in result_whole_local if d["interval"] in used_interval
    ]
    result_one_polygon = [
        d for d in result_one_polygon if d["interval"] in used_interval
    ]
    result_whole_polygon = [
        d for d in result_whole_polygon if d["interval"] in used_interval
    ]

    affordable_provider_one_local = plot_transform(
        result_one_local, "provider", key_index_name, label="_local"
    )
    affordable_requester_one_local = plot_transform(
        result_one_local, "requester", key_index_name, label="_local"
    )
    affordable_provider_whole_local = plot_transform(
        result_whole_local, "provider", key_index_name, label="_local"
    )
    affordable_requester_whole_local = plot_transform(
        result_whole_local, "requester", key_index_name, label="_local"
    )
    affordable_provider_one_polygon = plot_transform(
        result_one_polygon, "provider", key_index_name, label="_polygon"
    )
    affordable_requester_one_polygon = plot_transform(
        result_one_polygon, "requester", key_index_name, label="_polygon"
    )
    affordable_provider_whole_polygon = plot_transform(
        result_whole_polygon, "provider", key_index_name, label="_polygon"
    )
    affordable_requester_whole_polygon = plot_transform(
        result_whole_polygon, "requester", key_index_name, label="_polygon"
    )

    baseline_provider_one_local = plot_transform(
        result_one_local, "provider", key_index_name, label="_local"
    )
    baseline_requester_one_local = plot_transform(
        result_one_local, "requester", key_index_name, label="_local"
    )

    baseline_provider_whole_local = plot_transform(
        result_whole_local, "provider", key_index_name, label="_local"
    )
    baseline_requester_whole_local = plot_transform(
        result_whole_local, "requester", key_index_name, label="_local"
    )
    baseline_provider_one_polygon = plot_transform(
        result_one_polygon, "provider", key_index_name, label="_polygon"
    )
    baseline_requester_one_polygon = plot_transform(
        result_one_polygon, "requester", key_index_name, label="_polygon"
    )
    baseline_provider_whole_polygon = plot_transform(
        result_whole_polygon, "provider", key_index_name, label="_polygon"
    )
    baseline_requester_whole_polygon = plot_transform(
        result_whole_polygon, "requester", key_index_name, label="_polygon"
    )

    # provider_data = {**baseline_provider_whole_local, **affordable_provider_whole_local, **baseline_provider_whole_polygon, **affordable_provider_whole_polygon}
    # requester_data = {**affordable_requester_one_local, **baseline_requester_one_local, **affordable_requester_one_polygon, **baseline_requester_one_polygon}
    provider_whole = {
        **baseline_provider_whole_local,
        **affordable_provider_whole_local,
        **baseline_provider_whole_polygon,
        **affordable_provider_whole_polygon,
    }
    requester_whole = {
        **affordable_requester_whole_local,
        **baseline_requester_whole_local,
        **affordable_requester_whole_polygon,
        **baseline_requester_whole_polygon,
    }
    provider_one = {
        **baseline_provider_one_local,
        **affordable_provider_one_local,
        **baseline_provider_one_polygon,
        **affordable_provider_one_polygon,
    }
    requester_one = {
        **affordable_requester_one_local,
        **baseline_requester_one_local,
        **affordable_requester_one_polygon,
        **baseline_requester_one_polygon,
    }
    # y_label = "Time Usage (milliseconds)"

    plot_column(
        data=provider_whole,
        task=f"all_whole_disease_{key_index_name}",
        role="provider",
        x_label="Precentage of diseases (%)",
        y_label=y_label,
        factor=factor,
    )
    plot_column(
        data=requester_whole,
        task=f"all_whole_disease_{key_index_name}",
        role="requester",
        x_label="Precentage of diseases (%)",
        y_label=y_label,
        factor=factor,
    )
    plot_column(
        data=provider_one,
        task=f"all_one_disease_{key_index_name}",
        role="provider",
        x_label="Precentage of diseases (%)",
        y_label=y_label,
        factor=factor,
    )
    plot_column(
        data=requester_one,
        task=f"all_one_disease_{key_index_name}",
        role="requester",
        x_label="Precentage of diseases (%)",
        y_label=y_label,
        factor=factor,
    )


def test_area(env ,label = ""):

    # intevals = [0,  10, 20, 30, 40, 50, 60, 70, 80, 90,100]
    provider1 = Provider(
        env=env,
        name="Provider_area",
        description="Provider1",
        # address = random.choice(accounts),
    )
    requester1 = Requester(
        env=env,
        name="Requester_area",
        description="Requester1",
        #  address =  random.choice(accounts),
    )
    data_baseline = []
    data_result = []
    intevals = [0,  20,  40,  60, 80,  100]

    for interval in tqdm(intevals):
        precentage = interval / 100
        length = int(len(country_name_code_dict)*precentage)
        countries = list(country_name_code_dict.keys())[:length]
        provider1.country_names = countries
        requester1.country_names = countries
        # provider1.address = accounts.pop()
        # requester1.address = accounts.pop()
        # record_used_address(provider1.address)
        # record_used_address(requester1.address)

        # gas_update_area_group_code = provider1.update_area_group_relation()
        if env.name == TestEnum.polygon.name:
            provider1.delete_area( )
            requester1.delete_area()
        else:
            provider1.address = env.accounts.pop()
            requester1.address = env.accounts.pop()

        provider_affordable_result = provider1.upload_area_affordable()
        requester_affordable_result = requester1.upload_area_affordable()
        # # gas_access_simple = requester1.access_area_simple(provider1)
        provider_baseline_result = provider1.upload_area_baseline()
        requester_baseline_result = requester1.upload_area_baseline()

        data_result.append(
            {
                "interval": interval,
                "affordable": {
                    "provider": provider_affordable_result.to_dict(),
                    "requester": requester_affordable_result.to_dict(),
                },
                "baseline": {
                    "provider": provider_baseline_result.to_dict(),
                    "requester": requester_baseline_result.to_dict(),
                },
            }
        )
    json.dump(data_result, open(f"result/{env.name}_area{label}.json", "w"), indent=4)

def plot_transform(data_list, role, column, label=""):
    return {
        f"baseline{label}": [d["baseline"][role][column] for d in data_list],
        f"affordable{label}": [d["affordable"][role][column] for d in data_list],
        "interval": [d["interval"] for d in data_list],
    }


def plot_area(env, label = "", key_index_name="time_used", factor=1e6, y_label="Time cost ($1 \\times 10^{6}$)"):

    # plt.show()
    # result = json.load(open(f"result/{env_name.name}_area{label}.json", "r"))

    result_polygon = json.load(open(f"result/{TestEnum.polygon.name}_area{label}.json", "r"))
    intevals = [0,  20,  40,  60, 80,  100]
    result_polygon = list(filter(lambda x: x["interval"] in intevals, result_polygon))
    result_local = json.load(open(f"result/{TestEnum.local.name}_area{label}.json", "r"))
    result_local = list(filter(lambda x: x["interval"] in intevals, result_local))

    gas_provider_local = plot_transform(
        result_local, "provider", key_index_name, "_local"
    )
    gas_requester_local =plot_transform(result_local, "requester", key_index_name,"_local")
    gas_provider_polygon = plot_transform(
        result_polygon, "provider", key_index_name, "_polygon"
    )
    gas_requester_polygon = plot_transform(result_polygon, "requester", key_index_name,"_polygon")

    task = f"all_area_{key_index_name}{label}"
    gas_provider = gas_provider_local|gas_provider_polygon
    gas_requester = gas_requester_local | gas_requester_polygon
   
    plot_column(
        gas_provider,
        task,
        f"provider",
        "Precentage of countries (%)",
        "Time cost ($ 1 \\times 10^{3}$)",
        factor = factor,
    )
    plot_column(
        gas_requester,
        task,
        "requester",
        "Precentage of countries (%)",
        "Time cost ($ 1 \\times 10^{3}$)",
        factor=factor,
        # label=label,
    )

def plot_area_time(label = "", key_index_name="time_used", factor=1e6, y_label="Time usage (milliseconds)"):

    result_polygon = json.load(
        open(f"result/{TestEnum.polygon.name}_area{label}.json", "r")
    )
    intevals = [0, 20, 40, 60, 80, 100]
    result_polygon = list(filter(lambda x: x["interval"] in intevals, result_polygon))
    result_local = json.load(
        open(f"result/{TestEnum.local.name}_area{label}.json", "r")
    )
    result_local = list(filter(lambda x: x["interval"] in intevals, result_local))

    gas_provider_local = plot_transform(
        result_local, "provider", key_index_name, "_local"
    )
    gas_requester_local = plot_transform(
        result_local, "requester", key_index_name, "_local"
    )
    gas_provider_polygon = plot_transform(
        result_polygon, "provider", key_index_name, "_polygon"
    )
    gas_requester_polygon = plot_transform(
        result_polygon, "requester", key_index_name, "_polygon"
    )

    task = f"all_area_{key_index_name}{label}"
    gas_provider = gas_provider_local | gas_provider_polygon
    gas_requester = gas_requester_local | gas_requester_polygon

    plot_column(
        gas_provider,
        task,
        f"provider",
        "Precentage of countries (%)",
        y_label,
        factor=factor,
    )
    plot_column(
        gas_requester,
        task,
        "requester",
        "Precentage of countries (%)",
        # "Time cost ($ 1 \\times 10^{3}$)",
        y_label,
        factor=factor,
        # label=label,
    )


def plot_column(data, task, role,x_label,y_label,factor=1e3):
    import matplotlib.pyplot as plt
    patterns = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
    data_frame = pd.DataFrame(data)
    fig, ax1 = plt.subplots(figsize=(16, 4))
    width = 4
    alpha = 0.5
    data_font_size = None
    baseline_local_x = data_frame["interval"] - 1.5*width
    affordable_local_x = data_frame["interval"] - 0.5*width
    baseline_polygon_x = data_frame["interval"] + 0.5*width 
    affordable_polygon_x = data_frame["interval"] + 1.5*width

    # factor = 1e3
    keys = data.keys() - ["interval"]
    for k in keys:
        data_frame[k] /= factor
        # data_frame[k].round(1)
    # for k in keys:
    #     bars = ax1.bar(
    #         data_frame["interval"],
    #         data_frame[k] / factor,
    #         width=width,
    #         label=f"{k}",
    #     )
    #     for i, bar in enumerate(bars):
    #         yval = bar.get_height()
    #         xval = bar.get_x() + bar.get_width() * 0.9
    #         ax1.text(xval, yval, int(yval), ha="right", va="bottom")
    baseline_local_bars = ax1.bar(
        baseline_local_x,
        data_frame["baseline_local"],
        width=width,
        label=f"Baseline (Ganache)",
        color="red",
        # hatch=patterns[4],
        alpha=alpha,
    )
    affordable_local_bars = ax1.bar(
        affordable_local_x,
        data_frame["affordable_local"],
        width=width,
        label=f"Proposed (Ganache)",
        color="yellow",
        # hatch=patterns[5],
        alpha=alpha,
    )
    baseline_amoy_bars = ax1.bar(
        baseline_polygon_x,
        data_frame["baseline_polygon"],
        width=width,
        label=f"Baseline (Amoy)",
        color="blue",
        # hatch=patterns[6],
        alpha=alpha,
    )
    affordable_amoy_bars = ax1.bar(
        affordable_polygon_x,
        data_frame["affordable_polygon"],
        width=width,
        label=f"Proposed (Amoy)",
        color="green",
        # hatch=patterns[7],
        alpha=alpha,
    )
    # ax1.set_ylabel("Gas Used (Bar)")
    y_max = max([data_frame[k].max() for k in keys])
    # x_max = data_plot["interval"].max()
    ax1.set_ylim(0, y_max * 1.2)
    # ax1.xlim(0, x_max + 15)

    # ax1.set_ylim(0, 100)
    ax1.set_xlabel(x_label)
    ax1.set_ylabel(y_label)
    ax1.tick_params(axis='y')
    ax1.legend(loc='upper left',ncol=4)

    for i, bar in enumerate(baseline_local_bars):
        yval = bar.get_height()
        # if i == 0:
        #     yval_location = yval +  100
        xval = bar.get_x()  + bar.get_width() /2
        # xval = bar.get_x()
        ax1.text(
            xval, yval, int(yval), ha="center", va="bottom", fontsize=data_font_size
        )

    for i,bar in enumerate(affordable_local_bars):
        yval = bar.get_height()
        # if i == 0:
        #     x_loc = bar.get_x()
        #     y_loc = 0
        #     ha = "right"
        # else:
        x_loc = bar.get_x() + bar.get_width()/2
        y_loc = yval
        ha="center"

        ax1.text(x_loc, y_loc, int(yval), ha=ha, va="bottom", fontsize=data_font_size)

    for i,bar in enumerate(baseline_amoy_bars):
        yval = bar.get_height()
        xval = bar.get_x() + bar.get_width()/2
        ax1.text(
            xval, yval, int(yval), ha="center", va="bottom", fontsize=data_font_size
        )

    for i, bar in enumerate(affordable_amoy_bars):
        yval = bar.get_height()
        x_loc = bar.get_x() + bar.get_width() /2
        y_loc = yval
        ha = "center"

        ax1.text(x_loc, y_loc, int(yval), ha=ha, va="bottom", fontsize=data_font_size)
    plt.savefig(f"figs/column_{task}_{role}.pdf")

def plot_line(data, task, role,x_label,y_label):
    data_frame = pd.DataFrame(data)
    factor = 1e3
    import matplotlib.pyplot as plt

    intervals = data_frame["interval"]
    data_plot = pd.DataFrame()
    data_plot["interval"] = intervals
    keys = data_frame.columns.to_list()
    keys.remove("interval")
    # print(keys)
    for k in keys:
        data_plot[k] = (data_frame[k] / factor).round(1)

    ax = data_plot.plot.line(
        x="interval",
        y=keys,
        style=["o-", "*-"],
        xlabel=x_label,
        # ylabel=y_label,
        label=keys,
        # title="Gas cost for uploading area code of providers",
        # annotate=True,
    )

    y_max = max(data_plot["baseline"].max(),data_plot["affordable"].max())
    x_max = data_plot["interval"].max()
    plt.ylim(0, y_max*1.4)
    plt.xlim(0, x_max+15)
    x_shift= -5
    y_shift = y_max* 0.02

    # for index, row in data_frame.iterrows():
    index= -1
    plt.annotate(
        data_plot["baseline"].iloc[index],
        xy=(intervals.iloc[index], data_plot["baseline"].iloc[index]),
        xytext=(
            intervals.iloc[index] + x_shift,
            data_plot["baseline"].iloc[index] + y_shift,
        ),
    )
    plt.annotate(
        data_plot["affordable"].iloc[index],
        xy=(intervals.iloc[index], data_plot["affordable"].iloc[index]),
        xytext=(
            intervals.iloc[index] + x_shift,
            data_plot["affordable"].iloc[index] + y_shift,
        ),
    )
    plt.text(
            -0.05,
            1.02,
            y_label,
            ha="left",
            va="center",
            transform=ax.transAxes,
            # fontsize=12,
        )
    plt.savefig(f"figs/performance_{task}_{role}.pdf")


def plot_line_combined(data, task, role, x_label, y_label):
    data_frame = pd.DataFrame(data)
    factor = 1e3
    import matplotlib.pyplot as plt

    intervals = data_frame["interval"]
    data_plot = pd.DataFrame()
    data_plot["interval"] = intervals
    keys = data_frame.columns.to_list()
    keys.remove("interval")
    # print(keys)
    for k in keys:
        data_plot[k] = (data_frame[k] / factor).round(1)
    # data_plot["baseline"] = (data_frame["baseline"] / factor).round(1)
    # data_plot["affordable"] = (data_frame["affordable"] / factor).round(1)
    # data_plot["gas_update_area_group_code"] = data_frame["gas_update_area_group_code"] / factor
    # data_frame_simple["gas_provider"] = data_frame_simple["gas_provider"] / factor
    line_styles = ["-", "--", "-.", ":"]
    markers = [".", "o", "v", "^", "<", ">", "1", "2", "3", "4", "8", "s", "p", "P", "*", "h", "H", "+", "x", "X", "D", "d", "|", "_"]

    # line_styles = [ "-.", ":"]
    markers = ["1", "2", "3", "4"]
    # line_styles = ["-", "--", "-.", ":"]
    # env_dict = {}
    # for k in keys:
    #     _, env = k.split("-")
    #     if env not in env_dict:
    #         env_dict[env] = []
    #     env_dict[env].append(k)

    styles = [
        f"{line_style}{marker}"
        for line_style, marker in zip(
            random.sample(line_styles, k=len(keys),counts=[2,2,2,2]),
            random.sample(markers, k=len(keys)),
        )
    ]
    styles = ["o-", "8-.", "v-", "+:"]
    colors = ["r", "g", "b", "black"]
    fig, ax = plt.subplots(figsize=(6, 10))  # Width: 10 inches, Height: 6 inches

    ax = data_plot.plot.line(
        x="interval",
        y=keys,
        style=styles,
        xlabel=x_label,
        # ylabel=y_label,
        label=keys,
        color= colors,
        ax=ax,
        # title="Gas cost for uploading area code of providers",
        # annotate=True,
    )
    # ax.set_ylabel(
    #     f"Gas Usage ({factor})", rotation=0, labelpad=50, ha="left", va="top"
    # )
    # ax.yaxis.set_label_coords(-0.1, 1.05)
    y_max = max([data_plot[k].max() for k in keys])
    x_max = data_plot["interval"].max()
    plt.ylim(0, y_max * 1.08)
    plt.xlim(0, x_max + 15)
    x_shift = -5
    y_shift = y_max * 0.02

    # for index, row in data_frame.iterrows():
    index = -1
    for k in keys:
        plt.annotate(
            data_plot[k].iloc[index],
            xy=(intervals.iloc[index], data_plot[k].iloc[index]),
            xytext=(
                intervals.iloc[index] + x_shift,
                data_plot[k].iloc[index] + y_shift,
            ),
            
        )
    plt.text(
        -0.05,
        1.02,
        y_label,
        ha="left",
        va="center",
        transform=ax.transAxes,
        # fontsize=12,
    )
    plt.savefig(f"figs/performance_combined_{task}_{role}.pdf")


def analysis_countries_group():
    file_name = "data/countries_enrich.json"
    country_name_code_dict = json.load(open(file_name, "r"))
    group_counts = {}
    for k, v in country_name_code_dict.items():
        groups = v["groups"]
        for g in groups:
            if g not in group_counts:
                group_counts[g] = 0
            group_counts[g] += 1
        # print(k, v)
    # print(country_name_code_dict)

    count_list = sorted(list(group_counts.items()), key=lambda x: x[1], reverse=True)
    print(count_list)


def generate_group_index():
    groups = [
        "EUROPEAN_UNION",
        "ASIAN_PACIFIC_ECONOMIC_COOPERATION",
        "G20",
        "G7",
        "OPEC",
        "ASEAN",
        "NAFTA",
        "MERCOSUR",
        "OECD",
        "ARAB_GROUP",
    ]
    group_index = {g: 2**i for i, g in enumerate(groups)}
    json.dump(group_index, open("data/group_index.json", "w"), indent=4)

def generate_country_index():
    file_name = "data/countries_enrich.json"
    country_index_file = "data/country_index.json"
    country_name_code_dict = json.load(open(file_name, "r"))
    country_index = {k: 1<<v["index"] for k, v in country_name_code_dict.items()}

    json.dump(country_index, open(country_index_file, "w"), indent=4)


profile_list = [
    profile_open,
    profile_medium,
    profile_strict,
]


class Scenarios:
    def __init__(self, env, proportion: list, size, requesters: list) -> None:
        self.proportion = proportion
        self.size = size
        self.env = env

        self.levels = [
            profile_list[i]
            for i, p in enumerate(proportion)
            for _ in range(int(p * size))
        ]
        random.shuffle(self.levels)
        logger.info("levels", self.levels)
        self.provider_list = self.initial_scenarios()
        self.requester_list = requesters

    def initial_scenarios(self):
        provider_list = []
        for i in self.levels:
            provider = Provider(
                name=f"provider_{i}",
                description=f"provider_{i}",
                env = self.env,
                # address=accounts.pop(),
                profile=i,
                random_init=True,
            )
            provider.upload()
            provider_list.append(provider)
        return provider_list

    def start(self):
        result_map = {}
        for provider in tqdm(self.provider_list):
            for requester in self.requester_list:
                access_result = requester.request_access(provider)
                if provider.profile not in result_map:
                    result_map[provider.profile] = {
                        "total": 0,
                        "success": 0,
                        "error": {
                        },
                    }
                result_map[provider.profile]["total"] += 1
                if not access_result:
                    result_map[provider.profile]["success"] += 1
                else:
                    for error_str in access_result:
                        if error_str in result_map[provider.profile]["error"]:
                            result_map[provider.profile]["error"][error_str] += 1
                        else:
                            result_map[provider.profile]["error"][error_str] = 1

        return result_map


class Experiment_Simulation:
    def __init__(self, env,requester_number = 200,
        provider_number = 100):
        self.env = env
        # requester_number = 200
        # provider_number = 100
        self.requester_list = []
        self.provider_number = provider_number
        self.result_fp = "result/result_simulation.json"

        for i in range(requester_number):
            requester = Requester(
                name=f"requester_{i}",
                description=f"requester_{i}",
                env = self.env,
                # address=local_env.accounts.pop(),
                random_init=True,
            )
            requester.upload()
            self.requester_list.append(requester)

        # print(random.random())
        self.requester_list[0].update_area_group_relation()

    def start(self):
        scenarios_1 = Scenarios(
            env=self.env,
            proportion=[1, 0, 0],
            size=self.provider_number,
            requesters=self.requester_list,
        )
        scenarios_2 = Scenarios(env = self.env, proportion=[0.5, 0.25, 0.25], size=self.provider_number, requesters = self.requester_list)
        scenarios_3 = Scenarios(
            env=self.env,
            proportion=[0.2, 0.4, 0.4],
            size=self.provider_number,
            requesters=self.requester_list,
        )

        result_map_2 = scenarios_2.start()
        logger.critical(json.dumps(result_map_2))
        result_map_3 = scenarios_3.start()
        logger.critical(json.dumps(result_map_3))
        result_map_1 = scenarios_1.start()
        logger.critical(json.dumps(result_map_1))

        result_dict = {
            "scenario_1": result_map_1,
            "scenario_2": result_map_2,
            "scenario_3": result_map_3,
        }
        logger.critical(json.dumps(result_dict))

        json.dump(result_dict, open(self.result_fp, "w"), indent=4)

    def plot_simulation_category(self):
        import matplotlib.pyplot as plt
        import numpy as np

        alpha = 0.8

        # Define the data
        data = json.load(open(self.result_fp, "r"))
        category_dict = dict()

        for k, v in data.items():
            for category, value in v.items():
                total = value["total"]
                success = value["success"]
                error = value["error"]
                if category not in category_dict:
                    category_dict[category] = {
                        "total": 0,
                        "success": 0,
                        "error": {},
                    }

                category_dict[category]["total"] += total
                category_dict[category]["success"] += success
                for k, v in error.items():
                    if k not in category_dict[category]["error"]:
                        category_dict[category]["error"][k] = 0
                    category_dict[category]["error"][k] += v

        # Extract data points
        categories = list(category_dict.keys())
        # categories = ["open", "medium", "consevative"]
        # categories = ["open", "moderate", "consevative"]
        success_rates = [
            category_dict[category]["success"] / category_dict[category]["total"]
            for category in categories
        ]

        # Create a bar chart
        x = np.arange(len(categories))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(x, success_rates, width, label="Success Rate", alpha=alpha)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel("Categories")
        ax.set_ylabel("Success Rate")
        # ax.set_title('Success Rate by Category')
        ax.set_xticks(x)
        ax.set_ylim(0, 0.175)
        categories_label = ["open", "moderate", "consevative"]
        ax.set_xticklabels(categories_label)
        ax.legend()

        # Add labels to the bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(
                    f"{height:.2%}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )

        add_labels(bars)

        # Display the chart
        plt.savefig("figs/simulation_category.pdf")

    def plot_simulation_scenario(self):
        import matplotlib.pyplot as plt
        import numpy as np

        alpha = 0.8
        # Define the data
        data = json.load(open(self.result_fp, "r"))
        scenario_dict = dict()
        for k, v in data.items():
            total = sum([value["total"] for value in v.values()])
            success = sum([value["success"] for value in v.values()])
            error = {k: v for value in v.values() for k, v in value["error"].items()}
            scenario_dict[k] = {
                "total": total,
                "success": success,
                "error": error,
            }

        # Extract data points
        scenarios = list(scenario_dict.keys())
        success_rates = [
            scenario_dict[cat]["success"] / scenario_dict[cat]["total"] for cat in scenarios
        ]

        # Create a bar chart
        x = np.arange(len(scenarios))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(x, success_rates, width, label="Success Rate", alpha=alpha)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel("Scenarios")
        ax.set_ylabel("Success Rate")
        # ax.set_title("Success Rate by Scenarios")
        ax.set_xticks(x)
        ax.set_ylim(0, 0.175)
        ax.set_xticklabels(scenarios)
        ax.legend()

        # Add labels to the bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(
                    f"{height:.2%}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )

        add_labels(bars)

        # Display the chart
        plt.savefig("figs/simulation_scenario.pdf")


class Experiment_Case_Study:
    def __init__(self, env):
        self.env = env
        self.init_person()
        self.result_map = {
            AccessError.AREA_ERROR.message: r"\faFlag[regular]",
            AccessError.DISEASE_ERROR.message: r"\faCapsules",
            AccessError.DATE_ERROR.message: r"\faCalendar*[regular]",
            AccessError.PURPOSE_ERROR.message: r"\circletfillhl",
        }

    def init_person(self):
        provider1 = Provider(
            name="Provider 1",
            env = self.env,
            description=r"Provider.\ref{provider:a}",
            bool_items={item for item in DUO},
            country_names=["*"],
            disease_items=["*"],
        )
        provider2 = Provider(
            name="Provider 2",
            env=self.env,
            description=r"Provider.\ref{provider:b}",
            bool_items={DUO.Allow_All},
            country_names=["*"],
            disease_items=["A**", "B00"],
        )

        provider3 = Provider(
            name="Provider 3",
            env=self.env,
            description=r"Provider.\ref{provider:c}",
            bool_items={item for item in DUO},
            country_names=["USA"],
            group_names=["EUROPEAN_UNION"],
            disease_items=["*"],
        )

        provider4 = Provider(
            name="Provider 4",
            env=self.env,
            description=r"Provider.\ref{provider:d}",
            bool_items={item for item in DUO},
            country_names=["*"],
            start_year=2024,
            start_month=6,
            start_day=1,
            months=6,
            disease_items=["*"],
        )
        provider5 = Provider(
            name="Provider 5",
            env=self.env,
            description=r"Provider.\ref{provider:e}",
            bool_items={DUO.OpenToGeneralResearchAndClinicalCare},
            country_names=["*"],
            disease_items=["*"],
        )
        requester1 = Requester(
            name="Requester 1",
            env=self.env,
            description="Requester1",
            bool_items={item for item in ADAM},
            start_year=2024,
            start_month=6,
            start_day=1,
            months=6,
            country_names=["*"],
            disease_items=["*"],
        )

        requester2 = Requester(
            name="Requester 2",
            env=self.env,
            description="Requester2",
            bool_items={item for item in ADAM},
            disease_items=["A01"],
            country_names=["*"],
        )

        requester3 = Requester(
            name="Requester 3",
            env=self.env,
            description="Requester3",
            bool_items={item for item in ADAM},
            disease_items=["B02"],
            country_names=["*"],
        )

        requester4 = Requester(
            name="Requester 4",
            env=self.env,
            description="Requester4",
            bool_items={item for item in ADAM},
            country_names=["USA"],
            disease_items=["*"],
        )

        requester5 = Requester(
            name="Requester 5",
            env=self.env,
            description="Requester5",
            bool_items={item for item in ADAM},
            country_names=["NLD"],
            disease_items=["*"],
        )

        requester6 = Requester(
            name="Requester 6",
            env=self.env,
            description="Requester6",
            bool_items={item for item in ADAM},
            country_names=["USA", "THA"],
            disease_items=["*"],
        )

        requester7 = Requester(
            name="Requester 7",
            env=self.env,
            description="Requester7",
            bool_items={item for item in ADAM},
            group_names=["EUROPEAN_UNION"],
            disease_items=["*"],
        )

        requester8 = Requester(
            name="Requester 8",
            env=self.env,
            description="Requester8",
            bool_items=set(),
            start_year=2024,
            start_month=1,
            start_day=1,
            months=6,
            country_names=["*"],
            disease_items=["*"],
        )

        requester9 = Requester(
            name="Requester 9",
            env=self.env,
            description="Requester9",
            bool_items={ADAM.UseByAcademicProfessionals},
            country_names=["*"],
            disease_items=["*"],
        )

        r = provider1.update_area_group_relation()
        # v,c,g = provider1.contract.functions.DisplayCountryGroupRelation().call()
        # print("update_area_group_code ", r)

        self.provider_list = [provider1, provider2, provider3, provider4, provider5]
        self.requester_list = [
            requester1,
            requester2,
            requester3,
            requester4,
            requester5,
            requester6,
            requester7,
            requester8,
            requester9,
        ]
        for i, requester in enumerate(self.requester_list):
            requester.description = f"Requester.\\ref{{requester:{i+1}}}"
            requester.upload()
            logger.info(
                f"requester {requester.name} address {requester.address}, purpose item missed {requester.bool_items - requester.get_purpose_items()} added {requester.get_purpose_items()-requester.bool_items}"
            )
            # print(w3.eth.block_number)

        for provider in self.provider_list:
            provider.upload()
            logger.info(
                f"provider {provider.name} address {provider.address}, purpose item missed {provider.bool_items - provider.get_purpose_items()} added {provider.get_purpose_items()-provider.bool_items}"
            )

    def start(self):

        result_list = []
        header_list = [""]
        for provider in self.provider_list:
            header_list.append(provider.description)

        result_list.append("&".join(header_list) + r"\\")
        for ir, requester in enumerate(self.requester_list):
            row_list = []
            row_list.append(requester.description)
            for ip, provider in enumerate(self.provider_list):
                access_result = requester.request_access(provider)
                access_str = []
                for error in access_result:
                    access_str.append(self.result_map[error])

                if len(access_str) == 0:
                    access_result = "\cmark"
                else:
                    access_result = " ".join(access_str)
                row_list.append(access_result)
                # requester.access_area_simple(provider)
                # requester.access_disease(provider)
            result_list.append("&".join(row_list) + r"\\")

        print("\n".join(result_list))


if __name__ == "__main__":

    # test_mode = TestEnum.polygon

    local_env = deploy_contract_local()
    # polygon_env = deploy_contract_polygon(force_deploy=False)
    # print(f"accounts {accounts[0]}")
    # test_scenarios(provider_number=10, requester_number=10)
    # plot_simulation_category()
    # plot_simulation_scenario()
    # date_format = "%S:%M:%H %d-%m-%Y"

    # Experiment_Case_Study(local_env).start()
    experiment_simulation =  Experiment_Simulation(local_env,provider_number=100,requester_number=200)
    experiment_simulation.start()
    experiment_simulation.plot_simulation_category()
    experiment_simulation.plot_simulation_scenario()

    # logger.info(f"area start date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # # test_area(env=local_env, label="_zero")
    # test_area(env=polygon_env, label="_zero")
    # logger.info(f"area end date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # time.sleep(10)
    # # plot_area(env=test_mode, label="_zero",key_index_name="gas_used",factor = 1e3)
    # # plot_area_time(label="_zero")
    # # plot_area_time(label="_zero", key_index_name="gas_used",factor=1e3,y_label="Gas usage ($10^{3}$)")
    # logger.info(f"disease whole group start date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # # test_disease(local_env,one_group=False)
    # # test_disease(local_env,one_group=True)
    # test_disease(polygon_env, one_group=False)
    # logger.info(f"disease whole group end date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # time.sleep(10)

    # logger.info(f"disease one group start date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # test_disease(polygon_env, one_group=True)
    # logger.info(f"disease one group end date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")

    # plot_disease_time()
    # plot_disease_time(key_index_name="gas_used",factor=1e3, y_label="Gas usage ($10^{3}$)")

    # plot_time()

    # test_polygon()

    # test_case_study( )
