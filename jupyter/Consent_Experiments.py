import json
from wsgiref.handlers import BaseCGIHandler

from matplotlib import spines
import pandas as pd
from tqdm import tqdm

from Consent_Model import (
    Base_Contract,
    Contract_Affordable,
    Contract_Baseline,
    Env,
    Provider,
    Requester,
    DUO,
    ADAM,
    TestEnum,
    RESULT_CODE,
    Environment,
    Contract
)
from Consent_Model import country_name_code_dict, disease_list, disease_dict, profile_list, profile_open, profile_medium, profile_strict,logger

import string
import random
import matplotlib.pyplot as plt
import numpy as np

class Experiment_Performance:
    def __init__(self, contract_baseline:Base_Contract, 
                 contract_affordable:Base_Contract,enable_online=False):
        self.enable_online = enable_online
        self.env = contract_affordable.env
        self.contract_baseline = contract_baseline
        self.contract_affordable = contract_affordable
        self.intervals = [0, 20, 40, 60, 80, 100]

    def start(self):
        self.test_area()
        self.test_disease(one_group=True)
        self.test_disease(one_group=False)

    def test_disease(self, one_group=False):
        provider1, requester1 = self._initialize_provider_requester("disease")
        # intevals = [0, 20, 40, 60, 80, 100]
        disease_data = []
        groups = [c for c in string.ascii_uppercase]
        disease_list_all = disease_dict["A"] if one_group else disease_list

        for interval in tqdm(self.intervals):
            disease_items = self._generate_items(disease_list_all, interval)
            provider1.disease_items = disease_items
            requester1.disease_items = disease_items
            self._prepare_entities(provider1, requester1)

            result_provider_baseline = self.contract_baseline.upload_disease(provider1)
            result_requester_baseline = self.contract_baseline.upload_disease(requester1)
            result_provider_affordable = self.contract_affordable.upload_disease(provider1)
            result_requester_affordable = self.contract_affordable.upload_disease(requester1)

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

        result_fp = f"result/{self.env.name}_disease_{'one' if one_group else 'whole'}.json"
        json.dump(disease_data, open(result_fp, "w"), indent=4)

    def test_area(self, label=""):
        provider1, requester1 = self._initialize_provider_requester("area")
        # intevals = [0, 20, 40, 60, 80, 100]
        data_result = []

        for interval in tqdm(self.intervals):
            countries = self._generate_items(list(country_name_code_dict.keys()), interval)
            provider1.country_names = countries
            requester1.country_names = countries
            self._prepare_entities(provider1, requester1)

            provider_affordable_result = self.contract_affordable.upload_area(provider1)
            requester_affordable_result = self.contract_affordable.upload_area(
                requester1
            )
            provider_baseline_result = self.contract_baseline.upload_area(provider1)
            requester_baseline_result = self.contract_baseline.upload_area(
                requester1 )

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
        json.dump(data_result, open(f"result/{self.env.name}_area{label}.json", "w"), indent=4)

    def _initialize_provider_requester(self, entity_type):
        provider = Provider(
            env=self.env,
            name=f"Provider_{entity_type}",
            description=f"Provider_{entity_type}",
        )
        requester = Requester(
            env=self.env,
            name=f"Requester_{entity_type}",
            description=f"Requester_{entity_type}",
        )
        return provider, requester

    def _generate_items(self, items_list, interval):
        choiced_number = int(interval / 100 * len(items_list))
        return random.choices(items_list, k=max(1, choiced_number))

    def _prepare_entities(self, provider, requester):
        if self.env.name == TestEnum.polygon.name:
            self.contract_affordable.delete_area(provider
                                                )
            self.contract_baseline.delete_area(provider)

            self.contract_affordable.delete_area(requester)
            self.contract_baseline.delete_area(requester)
        else:
            provider.address = self.env.accounts.pop()
            requester.address = self.env.accounts.pop()

    def plot_area(self, key_index_name="time_used", factor=1e6, y_label="Time usage (milliseconds)", label=""):
        result_polygon, result_local = self._load_and_filter_results(
            TestEnum.polygon.name, TestEnum.local.name, "area", label=label
        )
        gas_provider, gas_requester = self._prepare_plot_data(
            result_polygon,
            result_local,
            key_index_name,
            "_polygon",
            "_local",
            # label=label,
        )
        task = f"area_{key_index_name}_{label}"
        self._plot_columns(gas_provider, gas_requester, task, "Precentage of countries (%)", y_label, factor)

    def plot_disease(self, key_index_name="time_used", factor=1e6, y_label="Time Usage (milliseconds)", label=""):
        result_one_polygon, result_one_local = self._load_and_filter_results(
            TestEnum.polygon.name, TestEnum.local.name, "disease_one", label=label
        )
        result_whole_polygon, result_whole_local = self._load_and_filter_results(
            TestEnum.polygon.name, TestEnum.local.name, "disease_whole", label=label
        )
        provider_whole, requester_whole = self._prepare_plot_data(
            result_whole_polygon, result_whole_local, key_index_name, "_polygon", "_local"
        )
        provider_one, requester_one = self._prepare_plot_data(
            result_one_polygon, result_one_local, key_index_name, "_polygon", "_local"
        )
        self._plot_columns(
            provider_whole,
            requester_whole,
            f"disease_whole_{key_index_name}_{label}",
            "Precentage of diseases (%)",
            y_label,
            factor,
        )
        self._plot_columns(provider_one, requester_one, f"disease_one_{key_index_name}_{label}", "Precentage of diseases (%)", y_label, factor)

    def _load_and_filter_results(self, polygon_name, local_name, result_type, label=""):
        result_polygon = json.load(open(f"result/{polygon_name}_{result_type}{label}.json", "r"))
        result_local = json.load(open(f"result/{local_name}_{result_type}{label}.json", "r"))
        # used_intervals = [0, 20, 40, 60, 80, 100]
        result_polygon = [d for d in result_polygon if d["interval"] in self.intervals]
        result_local = [d for d in result_local if d["interval"] in self.intervals]

        assert len(result_polygon) == len(result_local), f"Length mismatch: {len(result_polygon)} vs {len(result_local)}"
        return result_polygon, result_local

    def _prepare_plot_data(self, result_polygon, result_local, key_index_name, polygon_label, local_label):
        provider_data = self.plot_transform(result_local, "provider", key_index_name, local_label) | \
                        self.plot_transform(result_polygon, "provider", key_index_name, polygon_label)
        requester_data = self.plot_transform(result_local, "requester", key_index_name, local_label) | \
                         self.plot_transform(result_polygon, "requester", key_index_name, polygon_label)
        return provider_data, requester_data

    def _plot_columns(self, provider_data, requester_data, task, x_label, y_label, factor):
        self.plot_column(provider_data, task, "provider", x_label, y_label, factor)
        self.plot_column(requester_data, task, "requester", x_label, y_label, factor)

    def plot_column(self, data, task, role, x_label, y_label, factor=1e3):
        import matplotlib.pyplot as plt
        patterns = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
        data_frame = pd.DataFrame(data)
        fig, ax1 = plt.subplots(figsize=(18, 4), dpi=600)
        width = 3.5
        alpha = 1.0
        data_font_size = None
        baseline_local_x = data_frame["interval"] - 1.8 * width
        affordable_local_x = data_frame["interval"] - 0.7 * width
        baseline_polygon_x = data_frame["interval"] + 0.7 * width
        affordable_polygon_x = data_frame["interval"] + 1.8 * width

        keys = data.keys() - ["interval"]
        for k in keys:
            data_frame[k] /= factor

        baseline_local_bars = self._plot_bar(ax1, baseline_local_x, data_frame["baseline_local"], "Baseline (Ganache)", "lightcoral", alpha, width)
        
        # for spine in ax1.spines.values():
        #     spine.set_visible(True)
        affordable_local_bars = self._plot_bar(ax1, affordable_local_x, data_frame["affordable_local"], "Proposed (Ganache)", "yellow", alpha, width)
        baseline_polygon_bars = self._plot_bar(ax1, baseline_polygon_x, data_frame["baseline_polygon"], "Baseline (Amoy)", "royalblue", alpha, width)
        affordable_polygon_bars = self._plot_bar(ax1, affordable_polygon_x, data_frame["affordable_polygon"], "Proposed (Amoy)", "turquoise", alpha, width)

        y_max = max([data_frame[k].max() for k in keys])
        ax1.set_ylim(0, y_max * 1.2)
        ax1.set_xlabel(x_label)
        ax1.set_ylabel(y_label)
        ax1.tick_params(axis='y')
        ax1.legend(loc='upper left', ncol=4)

        self._add_bar_labels(ax1, baseline_local_bars, data_font_size)
        self._add_bar_labels(ax1, affordable_local_bars, data_font_size)
        self._add_bar_labels(ax1, baseline_polygon_bars, data_font_size)
        self._add_bar_labels(ax1, affordable_polygon_bars, data_font_size)

        plt.savefig(f"figure/column_{task}_{role}.pdf")

    def _plot_bar(self, ax, x, y, label, color, alpha, width):
        return ax.bar(x, y, width=width, label=label, color=color, alpha=alpha,  edgecolor="black")

    def _add_bar_labels(self, ax, bars, font_size):
        for bar in bars:
            yval = bar.get_height()
            xval = bar.get_x() + bar.get_width() / 2
            ax.text(xval, yval, int(yval), ha="center", va="bottom", fontsize=font_size)

    def plot_transform(self, data_list, role, column, label=""):
        return {
            f"baseline{label}": [d["baseline"][role][column] for d in data_list],
            f"affordable{label}": [d["affordable"][role][column] for d in data_list],
            "interval": [d["interval"] for d in data_list],
        }

    def plot(self,label=""):
        self.plot_area(label=label)
        self.plot_disease(label=label)

        self.plot_area(
            key_index_name="gas_used",
            factor=1e3,
            y_label="Gas usage (Gwei)",
            label=label,
        )
        self.plot_disease(key_index_name="gas_used", factor=1e3, y_label="Gas usage", label=label)


class Experiment_Simulation:

    class Scenarios:
        def __init__(self, contract:Base_Contract, proportion: list, size, requesters: list) -> None:
            self.proportion = proportion
            self.size = size
            self.env = contract.env
            self.contract = contract

            self.levels = [profile_open for _ in range(int(proportion[0] * size))] + [  
                profile_medium for _ in range(int(proportion[1] * size))] + [
                profile_strict for _ in range(int(proportion[2] * size))    ]

            random.shuffle(self.levels)
            # logger.info("levels", self.levels)
            self.provider_list = self.initial_scenarios()
            self.requester_list = requesters

        def initial_scenarios(self):
            provider_list = []
            for i, level in enumerate(self.levels):
                provider = Provider(
                    name=f"provider_{i}",
                    description=f"provider_{i}",
                    env = self.env,
                    # address=accounts.pop(),
                    level = level,
                    profile=Experiment_Simulation.PROFILES_DICT[level],
                    random_init=True,
                )
                self.contract.upload(provider)
                provider_list.append(provider)
            return provider_list

        def start(self):
            result_map = {}
            for provider in tqdm(self.provider_list):
                for requester in self.requester_list:
                    access_result = self.contract.access(provider,requester=requester)
                    if provider.level not in result_map:
                        result_map[provider.level] = {
                            "total": 0,
                            "success": 0,
                            "error": {},
                        }
                    result_map[provider.level]["total"] += 1
                    if not access_result:
                        result_map[provider.level]["success"] += 1
                    else:
                        for error_name in access_result:
                            # error_str = error_name.name
                            if error_name in result_map[provider.level]["error"]:
                                result_map[provider.level]["error"][error_name] += 1
                            else:
                                result_map[provider.level]["error"][error_name] = 1

            return result_map
    PROFILES_DICT = {
        profile_strict: {
            "simple_items": [DUO.HMBResearch, DUO.DiseaseSpecific, DUO.GeographicSpecific],
            "group_code": 2,
            "country_code": 20,
            "disease_items": ["A**","B**"],
            "disease_groups": 0.2,
            "months": 6,
        },
        profile_medium: {
            "simple_items": [DUO.HMBResearch, DUO.GeographicSpecific],
            "group_code": 2,
            "country_code": 20,
            "disease_items": ["A**","B**"],
            "disease_groups": 0.5,
            "months": 12,
        },
        profile_open: {
            "simple_items":  DUO.HMBResearch,
            "group_code": 1.0,
            "country_code": 1.0,
            "disease_items": 1.0,
            "disease_groups": 0.8,
            "months": 2**8 - 1,
        },
    }

    def __init__(self, contract:Base_Contract,requester_number = 200,
        provider_number = 100):
        self.env = contract.env
        self.contract = contract
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
            self.contract.upload(requester)
            self.requester_list.append(requester)

        # print(random.random())
        self.contract.update_area_group_relation(self.requester_list[0])
        # self.requester_list[0].update_area_group_relation()

    def start(self):
        scenarios_1 = Experiment_Simulation.Scenarios(
            contract=self.contract,
            proportion=[1, 0, 0],
            size=self.provider_number,
            requesters=self.requester_list,
        )
        scenarios_2 = Experiment_Simulation.Scenarios(
            contract=self.contract,
            proportion=[0.5, 0.25, 0.25],
            size=self.provider_number,
            requesters=self.requester_list,
        )
        scenarios_3 = Experiment_Simulation.Scenarios(
            contract=self.contract,
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
        # logger.info(json.dumps(result_dict, indent=2))

        json.dump(result_dict, open(self.result_fp, "w"), indent=4)

    def _plot_simulation(self, data, y_label, file_name):

        alpha = 1
        x_labels = list(data.keys())
        # Extract data points
        success_rates = [
            data[label]["success"] * 100 / data[label]["total"] for label in x_labels
        ]

        # Create a bar chart
        x = np.arange(len(x_labels))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(
            x,
            success_rates,
            width,
            label="Success Rate",
            alpha=alpha,
            color="royalblue",
            edgecolor="black",
        )

        # Add some text for labels, title and custom x-axis tick labels, etc.
        # ax.set_xlabel("Categories" if title is None else title)
        ax.set_ylabel(y_label)
        ax.set_xticks(x)
        ax.set_ylim(0, max(success_rates) + 10)
        ax.set_xticklabels(x_labels)

        # Add labels to the bars
        def add_labels(bars):
            for bar in bars:
                height = bar.get_height()
                ax.annotate(
                    f"{height:.2f}%",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                )

        add_labels(bars)

        # Save the chart
        plt.savefig(file_name)

    def plot_simulation_category(self):
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

        self._plot_simulation(
            data=category_dict,
            # x_labels=profile_list,
            y_label="Success Rate (%)",
            file_name="figure/simulation_category.pdf",
            # title="Categories",
        )

    def plot(self):
        self.plot_simulation_category()
        self.plot_simulation_scenario()

    def plot_simulation_scenario(self):
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
        x_labels = list(scenario_dict.keys())
        # x_labels = [label.capitalize() for label in x_labels]

        self._plot_simulation(
            data=scenario_dict,
            # x_labels=x_labels,
            y_label="Success Rate (%)",
            file_name="figure/simulation_scenario.pdf",
            # title="Scenarios",
        )


class Experiment_Case_Study:
    def __init__(self,  contract : Base_Contract):
        self.env = contract.env
        self.contract = contract
        self.init_person()
        self.result_map = {
            RESULT_CODE.GeographicSpecificRestriction.name: r"\faFlag[regular]",
            RESULT_CODE.OpenToDiseaseSpecific.name: r"\faCapsules",
            RESULT_CODE.TimeLimitOnUse.name: r"\faCalendar*[regular]",
            # RESULT_CODE.GeographicSpecificRestriction: r"\circletfillhl",
        }
        self.error_other = r"\circletfillhl"

    def init_person(self):
        provider1 = Provider(
            name="Provider 1",
            env = self.env,
            description=r"Provider.\ref{provider:a}",
            bool_items={DUO.Allow_All},
            # country_names=["*"],
            # disease_items=["*"],
        )
        provider2 = Provider(
            name="Provider 2",
            env=self.env,
            description=r"Provider.\ref{provider:b}",
            bool_items={DUO.OpenToDiseaseSpecific},
            # country_names=["*"],
            disease_items=["A**", "B01"],
        )

        provider3 = Provider(
            name="Provider 3",
            env=self.env,
            description=r"Provider.\ref{provider:c}",
            bool_items={DUO.GeographicSpecificRestriction},
            country_names=["USA"],
            group_names=["EUROPEAN_UNION"],
            # disease_items=["*"],
        )

        provider4 = Provider(
            name="Provider 4",
            env=self.env,
            description=r"Provider.\ref{provider:d}",
            bool_items={DUO.TimeLimitOnUse},
            # country_names=["*"],
            start_year=2024,
            start_month=6,
            start_day=1,
            months=6,
            # disease_items=["*"],
        )
        provider5 = Provider(
            name="Provider 5",
            env=self.env,
            description=r"Provider.\ref{provider:e}",
            bool_items={DUO.OpenToGeneticStudiesOnly},
            # country_names=["*"],
            # disease_items=["*"],
        )
        requester1 = Requester(
            name="Requester 1",
            env=self.env,
            description="Requester1",
            bool_items={ADAM.TimelineRestrictions,ADAM.UseByAcademicProfessionals},
            start_year=2024,
            start_month=6,
            start_day=1,
            months=6
        )

        requester2 = Requester(
            name="Requester 2",
            env=self.env,
            description="Requester2",
            bool_items={ADAM.UseForSpecificDiseaseResearch,ADAM.UseByAcademicProfessionals},
            disease_items=["A01"],
            # country_names=["*"],
        )

        requester3 = Requester(
            name="Requester 3",
            env=self.env,
            description="Requester3",
            bool_items={ADAM.UseForSpecificDiseaseResearch,ADAM.UseByAcademicProfessionals},
            disease_items=["B02"],
            # country_names=["*"],
        )

        requester4 = Requester(
            name="Requester 4",
            env=self.env,
            description="Requester4",
            bool_items={ADAM.UseBySpecifiedCountries,ADAM.UseByAcademicProfessionals},
            country_names=["USA"],
            # disease_items=["*"],
        )

        requester5 = Requester(
            name="Requester 5",
            env=self.env,
            description="Requester5",
            bool_items={ADAM.UseBySpecifiedCountries,ADAM.UseByAcademicProfessionals},
            country_names=["NLD"],
            # disease_items=["*"],
        )

        requester6 = Requester(
            name="Requester 6",
            env=self.env,
            description="Requester6",
            bool_items={ADAM.UseBySpecifiedCountries,ADAM.UseByAcademicProfessionals},
            country_names=["USA", "THA"],
            # disease_items=["*"],
        )

        requester7 = Requester(
            name="Requester 7",
            env=self.env,
            description="Requester7",
            bool_items={ADAM.UseBySpecifiedCountries, ADAM.UseByAcademicProfessionals},
            # country_names = [],
            group_names=["EUROPEAN_UNION"],
            # disease_items=["*"],
        )

        requester8 = Requester(
            name="Requester 8",
            env=self.env,
            description="Requester8",
            bool_items={ADAM.TimelineRestrictions, ADAM.UseByAcademicProfessionals},
            start_year=2024,
            start_month=1,
            start_day=1,
            months=6,
            # country_names=["*"],
            # disease_items=["*"],
        )

        requester9 = Requester(
            name="Requester 9",
            env=self.env,
            description="Requester9",
            bool_items={ADAM.UseForGeneticsResearch, ADAM.UseByAcademicProfessionals},
            # country_names=["*"],
            # disease_items=["*"],
        )

        r = self.contract.update_area_group_relation(provider1)
        # v,c,g = provider1.contract.functions.DisplayCountryGroupRelation().call()
        print("update_area_group_code ", r)

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
            self.contract.upload(requester)
            # logger.info(
            #     f"requester {requester.name} address {requester.address}, purpose item missed {requester.bool_items - requester.get_purpose_items()} added {requester.get_purpose_items()-requester.bool_items}"
            # )
            # print(w3.eth.block_number)

        for provider in self.provider_list:
            self.contract.upload(provider)
            # provider.upload()
            # logger.info(
            #     f"provider {provider.name} address {provider.address}, purpose item missed {provider.bool_items - provider.get_purpose_items()} added {provider.get_purpose_items()-provider.bool_items}"
            # )

        # logger.debug(f"requester7 area {requester7.display_area_affordable()}" )
        # logger.debug(f"provider3 area {provider3.display_area_affordable()}")

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
                access_result = self.contract.access(provider,  requester)
                access_str = []
                for error in access_result:
                    access_str.append(self.result_map.get(error.name,error.name))

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

    environment = Environment()
    local_baseline = Contract_Baseline(environment.deploy_contract_local(environment.interface_baseline))
    local_affordable =Contract_Affordable(environment.deploy_contract_local(environment.interface_affordable) )


    # Experiment_Case_Study(local_affordable).start()

    experiment_simulation =  Experiment_Simulation(local_affordable,provider_number=100,requester_number = 300)
    experiment_simulation.start()
    experiment_simulation.plot()


    # performance = Experiment_Performance(contract_affordable=local_affordable, contract_baseline=local_baseline)
    # performance.start()
    # performance.plot()
