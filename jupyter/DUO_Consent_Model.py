import json

# import web3
from datetime import datetime
from typing import Dict

from web3 import Web3

# import py_solc_x as px
import solcx
from web3.contract import Contract
import os
import logging
from pathlib import Path
import re
import enum
from enum import Enum
import yaml
import random
from web3.middleware import ExtraDataToPOAMiddleware


CURRENT_DIR = Path(__file__).resolve().parent
DATA_DIR = Path("data")
os.chdir(CURRENT_DIR)

private_config = yaml.safe_load(open("data/private_config.yaml", "r"))
private_key = private_config.get("private_key", None)

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


profile_strict = "Restrictive"
profile_medium = "Moderate"
profile_open = "Open"

profile_list = [
    profile_open,
    profile_medium,
    profile_strict,
]


ROLE_PROVIDER = 1
ROLE_REQUESTER = 2


# consent_fp_relative = r"jupyter\\data\\UnifiedConsentModel.sol"
# with open(consent_fp) as file:
#     contract_source_code = file.read()

# Compile & Store Compiled source code
# print(contract_source_code)
solcx_version = "0.8.0"
# solcx_version = '0.5.16'
solcx.install_solc(solcx_version)
# compiled_sol = solcx.compile_source(source=contract_source_code,
#   solc_binary="/snap/bin/solc")


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


# disease_list = []
disease_dict = {}
disease_list = []
for c in icd10.chapters:
    codes = expand_code_range(c[1])
    disease_list.extend(codes)
    for code in codes:
        #
        letter = code[0]
        if letter not in disease_dict:
            disease_dict[letter] = []
        disease_dict[letter].append(code)

        # disease_list = [item for sublist in disease_dict.values() for item in sublist]
        # print(f"disease_list length {len(disease_list)}")

        # country_name_code_dict = json.load(open("data/countries_enrich.json", "r"))

        # for k in country_name_code_dict.keys():
        #     country_name_code_dict[k]["position_index"] = (
        #         2 ** country_name_code_dict[k]["index"]
        #     )

group_country_dict = json.load(open("data/group_country.json", "r"))

group_index_dict = {v["abbreviation"]: v["index"] for v in group_country_dict}
country_index_dict = json.load(open("data/country_index.json", "r"))
# allowed_group_names = {"EUROPEAN_UNION"}

country_code_name_dict = {v: k for k, v in country_index_dict.items()}

all_countries_name = list(country_index_dict.keys())

all_group_names = list(group_index_dict.keys())


class Environment:
    def __init__(self):
        consent_affordable_fp = Path("solidity", "DUOConsentAffordable.sol")
        consent_baseline_fp = Path("solidity", "DUOConsentBaseline.sol")

        self.interface_affordable = self.compile_solidity(consent_affordable_fp)
        self.interface_baseline = self.compile_solidity(consent_baseline_fp)

    def compile_solidity(self, file_path: Path):
        compiled_sol = solcx.compile_files(
            file_path,
            solc_version=solcx_version,
            output_values=["abi", "bin", "bin-runtime"],
            optimize=True,
        )
        interface = compiled_sol[f"{file_path.as_posix()}:ConsentCode"]
        abi = interface["abi"]
        bytecode = interface["bin"]
        bytecode_runtime = interface["bin-runtime"]
        # logger.info(f"consent keys {interface.keys()}")
        return interface

    def deploy_contract_local(self, consent_interface: Dict, force_deploy=False):
        startTime = datetime.now()
        # Use Ganache for web3 instance
        w3 = Web3(
            Web3.HTTPProvider("HTTP://127.0.0.1:8545", request_kwargs={"timeout": 120})
        )

        # Set pre-funded ganache account #0 as sender
        w3.eth.defaultAccount = w3.eth.accounts[0]
        logger.info(f"account numbers {len(w3.eth.accounts)}")
        # The default `eth.defaultAccount` address is used as the default "from" property for request_1_address dictionaries if no other explicit "from" property is specified.
        # Create contract blueprint
        deployed_contract = w3.eth.contract(
            abi=consent_interface["abi"], bytecode=consent_interface["bin"]
        )
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

        tx_receipt = w3.eth.wait_for_transaction_receipt(
            tx_hash, timeout=120, poll_latency=0.1
        )
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
            abi=consent_interface["abi"],
            # bytecode=bytecode,
        )
        # Extract default accounts created by ganache
        # used_accounts = get_used_address()
        # accounts = set(map(lambda x:str(x), w3.eth.accounts))
        # accounts = list(accounts - used_accounts)
        # logger.info(f"actural accounts {len(accounts)}, used accounts {len(used_accounts)}")
        # print(f" actural {accounts.pop()}, used {used_accounts.pop()}")

        env = Env(
            TestEnum.local.name,
            w3,
            deployed_contract,
            w3.eth.accounts,
            provider_address,
        )
        return env

    def deploy_contract_polygon(self, consent_interface: Dict, force_deploy=False):

        # Connect to Polygon (Mumbai Testnet)
        pad = "https://polygon-amoy.drpc.org"
        rapt = "https://rpc-amoy.polygon.technology"
        w3 = Web3(
            provider=Web3.HTTPProvider(rapt),
            # middlewares=[geth_poa_middleware],
        )
        # https://rpc-amoy.polygon.technology
        w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)
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
            compiled_contract = w3.eth.contract(
                abi=consent_interface["abi"], bytecode=consent_interface["bin"]
            )

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
            signed_txn = w3.eth.account.sign_transaction(
                transaction, private_key=private_key
            )

            # Send transaction
            tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

            # Wait for transaction receipt
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            assert tx_receipt["status"] == 1
            contract_address = tx_receipt.contractAddress
            polygon_config = {"contract_address": contract_address}
            json.dump(polygon_config, open("data/polygon.json", "w"))
        else:
            polygon_config = json.load(open("data/polygon.json", "r"))
            contract_address = polygon_config.get("contract_address", None)

        # contract_address = w3.to_checksum_address(contract_address)
        deployed_contract = w3.eth.contract(
            address=contract_address,
            abi=consent_interface["abi"],
            bytecode=consent_interface["bin"],
        )
        logger.critical(f"Contract deployed at address: {contract_address}")
        # print(f"Contract deployed at address: {contract_address}")
        env = Env(
            TestEnum.polygon.name,
            w3,
            deployed_contract,
            [w3.to_checksum_address(account.address)],
        )
        return env


class RESULT_CODE(enum.Enum):
    Success = 0
    FirstCategory = 1
    GeneralResearch = 1 << 1
    ClinicalCare = 1 << 2
    HMBResearch = 1 << 3
    PopulationAndAncestryResearchOnly = 1 << 4
    PopulationAndAncestryResearchNon = 1 << 5
    DiseaseSpecific = 1 << 6
    GeneticStudiesOnly = 1 << 7
    NonGeneralMethodResearch = 1 << 8
    GeographicSpecific = 1 << 9
    NonProfitUseOnly = 1 << 10
    NonCommercialUseOnly = 1 << 11
    PublicationRequired = 1 << 12
    PublicationMoratorium = 1 << 13
    CollaborationRequired = 1 << 14
    EthicsApprovalRequired = 1 << 15
    TimeLimitOnUse = 1 << 16
    ReturnToResource = 1 << 17
    ResearchSpecificRestriction = 1 << 18
    DataUsePermission = 1 << 19
    UserSpecificRestriction = 1 << 20
    ProjectSpecificRestriction = 1 << 21
    InstitutionSpecificRestriction = 1 << 22


class TransactionResult:
    def __init__(
        self,
        status=0,
        gas_used=0,
        transaction_hash="",
        time_used=0,
        result=None,
        gas_price=0,
    ):
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
            "result": self.result,
        }

    # @property
    def __json__(self):
        return json.dumps(self.__dict__())

    def __str__(self):
        return f"status {self.status}, gas_used {self.gas_used}, transaction_hash {self.transaction_hash}, time_used {self.time_used}, result {self.result}"


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
    def __init__(self, name, w3, deployed_contract: Contract, accounts, manager=None):
        self.name = name
        self.w3 = w3
        self.contract = deployed_contract
        self.accounts = accounts
        self.manager = manager


class Person:

    def __init__(
        self,
        env,
        name="",
        description="",
        address=None,
        bool_items=None,
        country_names=None,
        group_names=None,
        disease_items=None,
        start_year=2021,
        start_month=1,
        start_day=1,
        hold_month=12,
        profile_dict=None,
        level=profile_open,
        user_restrictions=None,
        institution_restrictions=None,
        project_restrictions=None,
        role=ROLE_PROVIDER,
        # **kwargs,
    ):

        self.name = name
        self.estimate_gas = False
        self.print_time = False
        # self.w3 = env.w3
        self.env = env
        self.level = level

        if address is not None:

            self.address = address

            # balance = w3.eth.get_balance(address)
        else:
            self.address = env.accounts.pop()

            # print(f"balance of {address} is {balance}")

        self.purpose = bool_items

        self.description = description

        self.contract = env.contract

        # 'gasPrice': w3.eth.gas_price*0.1,

        # print(f"person_dict {self.person_dict}")
        self.debug = False
        self.disease_items = disease_items
        self.disease_groups = []
        self.country_names = country_names
        self.group_names = group_names
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.hold_month = hold_month
        self.role = role

        self.user_restrictions = user_restrictions
        self.institution_restrictions = institution_restrictions
        self.project_restrictions = project_restrictions
        self.profile_dict = profile_dict

        if profile_dict is not None:
            self.random_init(profile_dict)

    def _init_purpose(self, purpose_setting):
        if self.purpose is None:
            self.purpose = set()

        if isinstance(purpose_setting, float):
            if purpose_setting == 1.0:
                self.purpose = set(DUO)
            else:
                for item in DUO:
                    if random.random() < purpose_setting:
                        self.purpose.add(item)
        elif isinstance(purpose_setting, list):
            self.purpose = set(purpose_setting)
        elif isinstance(purpose_setting, DUO):
            self.purpose.add(purpose_setting)
        elif isinstance(purpose_setting, dict):
            for key, value in purpose_setting.items():
                if random.random() < value:
                    self.purpose.add(key)
        else:
            raise Exception("purpose_setting is not a list or DUO")

    def _init_disease(self, disease_setting):
        if self.disease_items is None:
            self.disease_items = set()

        if isinstance(disease_setting, float):
            if disease_setting == 1.0:
                self.disease_items = ["*"]
            else:
                self.disease_items = random.sample(
                    disease_list,
                    k=int(disease_setting * len(disease_list)),
                )
                self.disease_groups = random.sample(
                    string.ascii_uppercase, k=int(disease_setting * 26)
                )
        elif isinstance(disease_setting, str):
            self.disease_items = [disease_setting]
        elif isinstance(disease_setting, list):
            self.disease_items = disease_setting
        elif isinstance(disease_setting, int):
            self.disease_items = random.choices(
                disease_list,
                k=disease_setting,
            )
        else:
            raise Exception("Invalid disease_setting type")

    def _init_date(self, date_setting):
        if isinstance(date_setting["start_year"], tuple):
            self.start_year = random.randint(*date_setting["start_year"])
        else:
            self.start_year = date_setting["start_year"]

        if isinstance(date_setting["start_month"], tuple):
            self.start_month = random.randint(*date_setting["start_month"])
        else:
            self.start_month = date_setting["start_month"]

        if isinstance(date_setting["start_day"], tuple):
            self.start_day = random.randint(*date_setting["start_day"])
        else:
            self.start_day = date_setting["start_day"]

        if isinstance(date_setting["hold_month"], tuple):
            self.hold_month = random.randint(*date_setting["hold_month"])
        else:
            self.hold_month = date_setting["hold_month"]

    def _init_geography(self, geography_setting):
        if self.country_names is None:
            self.country_names = set()
        if self.group_names is None:
            self.group_names = set()

        country_setting = geography_setting["country"]
        if isinstance(country_setting, float):
            if country_setting == 1.0:
                self.country_names = ["*"]
            else:
                self.country_names = random.sample(
                    all_countries_name,
                    k=int(country_setting * len(all_countries_name)),
                )
        elif isinstance(country_setting, str):
            self.country_names = [country_setting]

        elif isinstance(country_setting, list):
            self.country_names = country_setting
        elif isinstance(country_setting, int):
            self.country_names = random.sample(
                all_countries_name,
                k=country_setting,
            )
        else:
            raise Exception("Invalid country_setting type")

        group_setting = geography_setting["group"]
        if isinstance(group_setting, float):
            self.group_names = random.sample(
                all_group_names,
                k=int(group_setting * len(all_group_names)),
            )
        elif isinstance(group_setting, int):
            self.group_names = random.sample(
                all_group_names,
                k=group_setting,
            )
        else:
            raise Exception("Invalid group_setting type")

    def random_init(self, profile_dict):

        self.purpose = set()
        purpose_setting = profile_dict["purpose"]
        self._init_purpose(purpose_setting)

        date_setting = profile_dict["date"]
        self._init_date(date_setting)

        disease_setting = profile_dict["disease"]
        self._init_disease(disease_setting)

        country_setting = profile_dict["geography"]
        self._init_geography(country_setting)

    # def update_area_group_code_baseline(self, part_number=20):

    #     def split(a, n):

    #         k, m = divmod(len(a), n)

    #         return tuple(
    #             a[i * k + min(i, m) : (i + 1) * k + min(i + 1, m)] for i in range(n)
    #         )

    #     country_group_dict = {}

    #     for c in self.country_names:

    #         if c not in self.country_name_code_dict:

    #             print(f"{c} not in country_dict")

    #             return

    #         country_dict = self.country_name_code_dict[c]

    #         country_group_dict[country_dict["index"]] = [
    #             self.group_order_index_dict[g] for g in country_dict["groups"]
    #         ]

    #     country_code_list = list(country_group_dict.keys())

    #     country_group_index_list = list(country_group_dict.values())

    #     country_number = len(country_code_list)

    #     # print("country_group_dict", country_group_dict)

    #     country_code_list_part = split(country_code_list, part_number)

    #     country_group_index_list_part = split(country_group_index_list, part_number)

    #     gas = 0

    #     for i in range(part_number):

    #         func = self.contract.functions.UpdateAreaBaseline(
    #             country_code_list_part[i], country_group_index_list_part[i]
    #         )

    #         func_gas = func.estimate_gas()

    #         gas += func_gas
    #     return gas

    # def display_area_codes(self):
    #     (
    #         Group_Code,
    #         Country_Codes,
    #         Country_Group_Codes,
    #     ) = self.contract.functions.DisplayAreaCode(self.role, self.address).call()

    #     # groupp_code is a int of the sum of the value of group_index_dict, decode it according to the group_index_dict

    #     group_names = []

    #     for k, v in self.group_index_dict.items():

    #         if v & Group_Code:

    #             group_names.append(k)

    #     # print("displayAreaCodes", Country_Codes)

    #     # print("Country_Group_Codes", Country_Group_Codes)

    #     country_names = [self.country_code_name_dict[c] for c in Country_Codes]

    #     result = {"group_names": group_names, "country_codes": country_names}

    #     logging.info(f"displayAreaCodes is {result}")

    # def refresh_state(self):
    #     func = self.contract.functions.RefreshState(self.address)
    #     return self.send_transaction(func)


class Base_Contract:
    def __init__(self, env: Env):
        self.env = env
        self.w3 = env.w3
        self.contract = env.contract
        self.functions = env.contract.functions

    def update_area_group_relation(self, person):
        pass

    def upload_area(self):
        raise NotImplementedError("upload_area")

    def upload_disease(self, person: Person) -> TransactionResult:
        raise NotImplementedError("upload_disease")

    def upload_date(self, person: Person) -> TransactionResult:

        try:

            func = self.functions.UploadDate(
                person.role,
                person.address,
                person.start_year,
                person.start_month,
                person.start_day,
                person.hold_month,
            )

        except Exception as e:
            print(f"error in upload_date {e}")
            logger.error(
                f"error in upload_date, role {person.role}, address {person.address}, start_year {person.start_year}, start_month {person.start_month}, start_day {person.start_day}, hold_month {person.hold_month}"
            )

        # logger.info(
        #     f"upload_date, role {person.role}, address {person.address}, start_year {person.start_year}, start_month {person.start_month}, start_day {person.start_day}, hold_month {person.hold_month}"
        # )

        return self.send_transaction(func, person)

    def upload_purpose(self, person: Person) -> TransactionResult:
        if person.role == ROLE_PROVIDER:
            # Check if at least one of three items is in person.purpose
            required_items = {DUO.GeneralResearch, DUO.DiseaseSpecific, DUO.HMBResearch}
            # if not any(item in person.purpose for item in required_items):
            #     raise ValueError(
            #         "At least one of GeneralResearch, DiseaseSpecific, or HMBResearch must be in purpose"
            #     )
        elif person.role == ROLE_REQUESTER:
            # Check if at least one of two items is in person.purpose
            required_items = {
                DUO.DiseaseSpecific,
                DUO.GeographicSpecific,
                DUO.TimeLimitOnUse,
            }
            # if not any(item in person.purpose for item in required_items):
            #     raise ValueError(
            #         "At least one of DiseaseSpecific, GeographicSpecific, or TimeLimitOnUse must be in purpose"
            #     )
            person.purpose.discard(DUO.GeneralResearch)
            person.purpose.discard(DUO.HMBResearch)

        purpose_unload = [True if item in person.purpose else False for item in DUO]
        # logging.info(
        #     f"name {self.name} role {self.role}, address {self.address}, bool_items {simple_value}"
        # )

        upload_func = self.contract.functions.upload_purpose(
            person.role, person.address, purpose_unload
        )

        return self.send_transaction(upload_func, person)

    def get_purpose(self, person: Person):
        purpose = self.contract.functions.get_purpose(
            person.role, person.address
        ).call()
        result = [item for item, value in zip(DUO, purpose) if value]
        return result

    def _upload_extension_provider(self, person: Person) -> TransactionResult:
        func = self.functions.upload_extension(
            person.role,
            person.address,
            person.user_restrictions,
            person.project_restrictions,
            person.institution_restrictions,
        )
        return self.send_transaction(func, person)

    def delete_area(self):
        raise NotImplementedError("delete_area")

    def delete_disease(self):
        raise NotImplementedError("delete_disease")

    def send_transaction(
        self, func, person: Person = None, call=False, label="", sender_address=None
    ):
        # if self.estimate_gas:
        #     gas = func.estimate_gas()
        #     return TransactionResult(gas_used=gas)
        # else:
        if person is not None and sender_address is None:
            sender_address = person.address

        person_dict = {
            "from": sender_address,
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
            "from": sender_address,
            "type": 2,  # Explicitly specify EIP-1559 transaction type
            "gas": 25_000_000,  # Ensure gas limit is reasonable
            "maxFeePerGas": self.w3.to_wei(40, "gwei"),  # Reasonable max fee per gas
            "maxPriorityFeePerGas": self.w3.to_wei(
                30, "gwei"
            ),  # Reasonable max priority fee per gas
            "nonce": self.w3.eth.get_transaction_count(
                sender_address
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
        else:
            raise ValueError(f"Invalid env name: {self.env.name}")

        # logger.info(f"receipt {receipt}")
        gas_used = receipt["gasUsed"]
        gas_price = receipt["effectiveGasPrice"]
        time_diff = end_time - start_time
        return TransactionResult(
            gas_used=gas_used,
            time_used=time_diff,
            gas_price=gas_price,
            transaction_hash=receipt["transactionHash"].hex(),
            status=receipt["status"],
        )

    def upload(self, person: Person) -> TransactionResult:
        self.upload_purpose(person)

        # logger.info(f"purpose {person.purpose}")
        if DUO.GeographicSpecific in person.purpose:
            self.upload_area(person)
        if DUO.DiseaseSpecific in person.purpose:
            self.upload_disease(person)
        if DUO.TimeLimitOnUse in person.purpose:
            self.upload_date(person)

        if (
            DUO.UserSpecificRestriction in person.purpose
            or DUO.ProjectSpecificRestriction in person.purpose
            or DUO.InstitutionSpecificRestriction in person.purpose
        ):
            self._upload_extension_provider(person)

    def access(self, provider: Person, requester: Person) -> set:
        if provider.role == ROLE_PROVIDER and requester.role == ROLE_REQUESTER:
            func = self.functions.access_data(provider.address, requester.address)
        else:
            raise ValueError(f"Invalid role: {provider.role} {requester.role}")

        result = self.send_transaction(func, provider, call=True, label="access").result
        # print(f"access result {result}")
        result_set = set()
        if result == 0:
            return result_set
        for r in RESULT_CODE:
            if r.value & result:
                result_set.add(r.name)
        return result_set


class Contract_Affordable(Base_Contract):
    def __init__(self, env):
        super().__init__(env)

    def update_area_group_relation(self) -> TransactionResult:

        country_group_dict = {}

        for item in group_country_dict:
            countries = item["members"]
            countries_value = sum([country_index_dict[c] for c in countries])
            group_index = item["index"]
            country_group_dict[group_index] = countries_value

        country_group_data = list(country_group_dict.values())

        country_group_index = list(country_group_dict.keys())

        # print("country_group_dict", country_group_dict)

        func = self.contract.functions.UpdateCountryGroupRelation(
            country_group_data, country_group_index
        )

        # func.transact(self.person_dict)

        return self.send_transaction(
            func,
            None,
            label="update_area_group_relation",
            sender_address=self.env.manager,
        )

    def upload_area(self, person: Person) -> TransactionResult:

        # if "*" in self.country_names:

        # #     func = self.contract.functions.UploadAreaAffordable(
        # #         self.role, self.address, True, 0, 0
        # #     )
        # #     # logger.debug("allow all countries")

        # #     return self.send_transaction(func)

        if person.country_names is not None:
            country_codes = [country_index_dict[c] for c in person.country_names]
            country_code = sum(country_codes)
        else:
            country_code = 0

        if person.group_names is not None and len(person.group_names) > 0:
            group_codes = [group_index_dict[g] for g in person.group_names]
            group_code = sum(group_codes)
        else:
            # logger.debug(f"do not have group_names")
            group_code = 0

        # logger.info(
        #     f"name {person.name} country_codes {country_code}, {bin(country_code)}   group_code {group_code} {bin(group_code)}"
        # )
        func = self.contract.functions.UploadArea(
            person.role, person.address, group_code, country_code
        )
        return self.send_transaction(func, person, label="upload_area")

    def display_area(self):
        group_code, country_code = self.contract.functions.DisplayAreaAffordable(
            self.role, self.address
        ).call()
        countries = decode_country_code(country_code)
        groups = decode_group_code(group_code)

        return groups, countries

    def upload_disease(self, person: Person) -> TransactionResult:

        # if "*" in self.disease_items:

        #     func = self.contract.functions.UploadDiseaseAffordable(
        #         self.role, self.address, True, 0, []
        #     )
        #     # logger.debug("allow all disease")

        #     return self.send_transaction(func)

        disease_codes = [diseaseCode2IntHierarchy(d) for d in person.disease_items]
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
        disease_group_codes = [
            1 << (ord(d) - ord("A") + 1) for d in person.disease_groups
        ]
        disease_group_code = sum(disease_group_codes)

        disease_combined_codes = [
            (1 << (group_code + 100)) + chapter_code
            for group_code, chapter_code in disease_dict.items()
        ]
        # print(f"name {self.name} disease_dict {disease_dict}")
        # print(
        #     f"name {person.name} disease_group_code {disease_group_code} ({bin(disease_group_code)}) "
        #     f"disease_combined_codes {[f'{code} ({bin(code)})' for code in disease_combined_codes]}"
        # )
        max_code = 1 << 128
        for code in disease_combined_codes:
            if code > max_code:
                print(
                    f"code {code} larger than 2**128 disease_dict {disease_dict}, self.disease_items {person.disease_items}"
                )
            # print(f"code {code} disease_code {int2DiseaseCode(code)}")
        # logger.info(f"{self.name} disease_group_code {disease_group_code} disease_combined_codes {disease_combined_codes}")
        func = self.contract.functions.UploadDisease(
            person.role,
            person.address,
            disease_group_code,
            disease_combined_codes,
        )

        return self.send_transaction(func, person)

    def delete_area(self, person: Person) -> TransactionResult:
        function = self.contract.delete_area(person.role, person.address)
        return self.send_transaction(function, person)

    def delete_disease(self, person: Person):
        function = self.contract.delete_disease(person.role, person.address)
        return self.send_transaction(function, person)


class Contract_Baseline(Base_Contract):
    def __init__(self, env):
        super().__init__(env)

    def upload_area(self, person: Person) -> TransactionResult:

        country_codes = [
            country_name_code_dict[c]["index"] for c in person.country_names
        ]

        # print("UploadCountryItems", country_codes)
        if hasattr(person, "group_names"):
            group_codes = [group_index_dict[g] for g in person.group_names]
        else:
            group_codes = []

        func = self.contract.functions.UploadArea(
            person.role,
            person.address,
            group_codes,
            country_codes,
        )

        # print("UploadAreaCode role", self.role)

        return self.send_transaction(func, person)

    def upload_disease(self, person: Person) -> TransactionResult:
        disease_codes = [diseaseCode2Int(d) for d in person.disease_items]

        func = self.contract.functions.UploadDisease(
            person.role, person.address, disease_codes
        )

        return self.send_transaction(func, person)

    def delete_area(self, person: Person) -> TransactionResult:
        country_codes = [country_name_code_dict[c]["index"] for c in self.country_names]

        # print("UploadCountryItems", country_codes)
        if hasattr(self, "group_names"):
            group_codes = [group_index_dict[g] for g in self.group_names]
        else:
            group_codes = []

        func = self.contract.functions.delete_area(
            self.role,
            self.address,
            group_codes,
            country_codes,
        )
        # self.send_transaction(func)

        return self.send_transaction(func, person)

    def delete_disease(self, person):
        func = self.contract.functions.delete_disease(
            self.role, self.address, [diseaseCode2Int(d) for d in self.disease_items]
        )
        return self.send_transaction(func, person)

    # def access(self):
    #     return self.access()


pattern = r"^[A-Z][0-9\*]{2}$"
pattern_compiled = re.compile(pattern)


def diseaseCode2IntHierarchy(code: str):
    # A01
    #  the code is a string like A00,B11, etc.
    #  return the int code for chapter, group as a tuple
    # print(f"code is {code}")
    # if not pattern_compiled.match(code):
    #     print(f"The string {code} not matches the pattern")
    #     return 0
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


class DUO(Enum):
    NoRestriction = 1
    GeneralResearch = 1 << 2
    ClinicalCare = 1 << 3
    HMBResearch = 1 << 4
    PopulationAndAncestryResearchOnly = 1 << 5
    PopulationAndAncestryResearchNon = 1 << 6
    DiseaseSpecific = 1 << 7
    GeneticStudiesOnly = 1 << 8
    NonGeneralMethodResearch = 1 << 9
    GeographicSpecific = 1 << 10
    NonProfitUseOnly = 1 << 11
    NonCommercialUseOnly = 1 << 12
    PublicationRequired = 1 << 13
    PublicationMoratorium = 1 << 14
    CollaborationRequired = 1 << 15
    EthicsApprovalRequired = 1 << 16
    TimeLimitOnUse = 1 << 17
    ReturnToResource = 1 << 18
    ResearchSpecificRestriction = 1 << 19
    UserSpecificRestriction = 1 << 20
    ProjectSpecificRestriction = 1 << 21
    InstitutionSpecificRestriction = 1 << 22


# DUO_order_list = [
#     DUO.Allow_All,
#                   DUO.OpenToGeneralResearchAndClinicalCare, DUO.OpenToHMBResearch, DUO.OpenToPopulationAndAncestryResearch, DUO.OpenToDiseaseSpecific, DUO.OpenToGeneticStudiesOnly, DUO.ResearchSpecificRestrictions, DUO.OpenToResearchUseOnly, DUO.GeneralMethodResearch, DUO.GeographicSpecificRestriction, DUO.OpenToNonProfitUseOnly, DUO.PublicationRequired, DUO.CollaborationRequired, DUO.EthicsApprovalrequired, DUO.TimeLimitOnUse, DUO.CostOnUse, DUO.DataSecurityMeasuresRequired]


import string


class Provider(Person):

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.role = ROLE_PROVIDER

        # risk_level = kwargs.get("risk_level", None)
        # random_init = kwargs.get("random_init", False)
        self.contract: Base_Contract = kwargs.get("contract", None)

    def get_purpose_items(self):
        duo_list = self.contract.functions.GetPurposeItemsProvider(self.address).call()
        result_set = set()
        for result_item, duo_item in zip(duo_list, DUO):
            if result_item:
                result_set.add(duo_item)
        return result_set


class Requester(Person):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role = ROLE_REQUESTER
        # random_init = kwargs.get("random_init", False)

        # if random_init:

        #     # logger.info(f"{self.name} bool_items is {self.bool_items.to_int()}")
        #     profile_dict = {
        #         "simple_items": random.uniform(0.0, 0.5),
        #         "group_code": random.uniform(0, 0.05),
        #         "country_code": random.uniform(0, 0.05),
        #         "disease_items": random.uniform(0, 0.05),
        #         "disease_groups": random.uniform(0, 0.05),
        #         "months": random.randint(1, 24),
        #     }
        #     # profile_dict = self.profiles[self.profile]
        #     # self.random_init(profile_dict)
        #     self.random_init(profile_dict)

        #     self.bool_items = set()
        #     for item in DUO:
        #         if random.random() < profile_dict["simple_items"]:
        #             self.bool_items.add(item)
        #     if profile_dict["group_code"] > 0 or profile_dict["country_code"] > 0:
        #         self.bool_items.add(DUO.GeographicSpecific)
        #     if profile_dict["disease_items"] > 0:
        #         self.bool_items.add(DUO.DiseaseSpecific)

        #     self.start_year = random.randint(2024, 2025)
        #     self.start_month = random.randint(1, 12)
        #     self.start_day = random.randint(1, 28)
        # self.months = random.randint(1, 24)
        # generate icd-10 codes
        # logger.info(                f"{self.name}  country_names {self.country_names} group_names {self.group_names} disease_items {self.disease_items} start_year {self.start_year} start_month {self.start_month} start_day {self.start_day} months {self.months} bool_items {self.bool_items}" )

    def _check_role(self, provider: Provider):

        if provider.role != ROLE_PROVIDER:

            raise Exception("requestAccess: provider is not a Provider")

        if self.role != ROLE_REQUESTER:

            raise Exception("requestAccess: requester is not a Requester")

    def get_purpose_items(self):
        duo_list = self.contract.functions.GetPurposeItemsRequester(self.address).call()
        result_set = set()
        for result_item, duo_item in zip(duo_list, DUO):
            if result_item:
                result_set.add(duo_item)
        return result_set

    def request_access(self, provider: Provider):

        if provider.role != ROLE_PROVIDER:

            print("requestAccess: provider is not a Provider")
            return

        if self.role != ROLE_REQUESTER:

            print("requestAccess: requester is not a Requester")
            return

        func = self.contract.functions.AccessData(provider.address, self.address)

        result = self.send_transaction(func, True).result
        # logger.info(f"request_access result {result}")
        result_set = set()
        for error in RESULT_CODE:
            if result & error.value > 0:
                result_set.add(error)
        # logger.debug(f"request_access provider {provider.name}, provider bools {provider.bool_items}, requester {self.name}, requester bools {self.bool_items}, result_set {result_set}")
        return result_set


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
    country_index = {k: 1 << v["index"] for k, v in country_name_code_dict.items()}

    json.dump(country_index, open(country_index_file, "w"), indent=4)
