import json

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
)
from Consent_Model import country_name_code_dict, disease_list, disease_dict, profile_list, profile_open, profile_medium, profile_strict,logger

import string
import random

class Experiment_Performance:
    def __init__(self, env):
        self.env = env 

    def start(self):
        self.test_area()
        self.test_disease()

    def test_disease(self, one_group=False):
        provider1 = Provider(
            self.env,
            name="Provider_disease",
            description="Provider1",
            # address=random.choice(accounts),
        )
        requester1 = Requester(
            self.env,
            name="Requester_disease",
            description="Requester1",
            # address=random.choice(accounts),
        )

        # intevals = [0, 1, 5, 10, 20, 30, 40, 50, 60, 70,80,90,100]
        # intevals = [80]
        # intevals = [1]
        intevals = [0, 20, 40, 60, 80, 100]

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
            
            if self.env.name == TestEnum.polygon.name:
                provider1.delete_disease()
                requester1.delete_disease()
            else:
                provider1.address = self.env.accounts.pop()
                requester1.address = self.env.accounts.pop()
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

        result_fp = f"result/{self.env.name}_disease_{'one' if one_group else 'whole'}.json"

        json.dump(disease_data, open(result_fp, "w"), indent=4)

    def test_area(self, env, label=""):

        # intevals = [0,  10, 20, 30, 40, 50, 60, 70, 80, 90,100]
        provider1 = Provider(
            env=self.env,
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
        intevals = [0, 20, 40, 60, 80, 100]

        for interval in tqdm(intevals):
            precentage = interval / 100
            length = int(len(country_name_code_dict) * precentage)
            countries = list(country_name_code_dict.keys())[:length]
            provider1.country_names = countries
            requester1.country_names = countries
            # provider1.address = accounts.pop()
            # requester1.address = accounts.pop()
            # record_used_address(provider1.address)
            # record_used_address(requester1.address)

            # gas_update_area_group_code = provider1.update_area_group_relation()
            if env.name == TestEnum.polygon.name:
                provider1.delete_area()
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

    def plot_area_time(self, label = "", key_index_name="time_used", factor=1e6, y_label="Time usage (milliseconds)"):

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


    def plot_disease_time(self,
        key_index_name="time_used", factor=1e6, y_label="Time Usage (milliseconds)"
    ):
        # task = f"{test_mode.name}_disease"
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

    def plot_column(self, data, task, role,x_label,y_label,factor=1e3):
        import matplotlib.pyplot as plt
        patterns = ["/", "\\", "|", "-", "+", "x", "o", "O", ".", "*"]
        data_frame = pd.DataFrame(data)
        fig, ax1 = plt.subplots(figsize=(16, 4),dpi = 600)
        width = 4
        alpha = 0.9
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
        plt.savefig(f"figs/column_{task}_{role}.svg")


            
    def plot_transform(self, data_list, role, column, label=""):
        return {
            f"baseline{label}": [d["baseline"][role][column] for d in data_list],
            f"affordable{label}": [d["affordable"][role][column] for d in data_list],
            "interval": [d["interval"] for d in data_list],
        }


    def plot(self):

        self.plot_area_time()
        self.plot_disease_time()


class Experiment_Simulation:
        
    class Scenarios:
        def __init__(self, env, proportion: list, size, requesters: list) -> None:
            self.proportion = proportion
            self.size = size
            self.env = env

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
                provider.upload()
                provider_list.append(provider)
            return provider_list

        def start(self):
            result_map = {}
            for provider in tqdm(self.provider_list):
                for requester in self.requester_list:
                    access_result = requester.request_access(provider)
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
                        for error_code in access_result:
                            error_str = error_code.name
                            if error_str in result_map[provider.level]["error"]:
                                result_map[provider.level]["error"][error_str] += 1
                            else:
                                result_map[provider.level]["error"][error_str] = 1

            return result_map
    PROFILES_DICT = {
        profile_strict: {
            "simple_items": [DUO.OpenToHMBResearch, DUO.OpenToDiseaseSpecific,DUO.GeographicSpecificRestriction],
            "group_code": 2,
            "country_code": 20,
            "disease_items": ["A**","B**"],
            "disease_groups": 0.2,
            "months": 6,
        },
        profile_medium: {
            "simple_items": [DUO.OpenToHMBResearch, DUO.GeographicSpecificRestriction],
            "group_code": 2,
            "country_code": 20,
            "disease_items": ["A**","B**"],
            "disease_groups": 0.5,
            "months": 12,
        },
        profile_open: {
            "simple_items":  DUO.OpenToHMBResearch,
            "group_code": 1.0,
            "country_code": 1.0,
            "disease_items": 1.0,
            "disease_groups": 0.8,
            "months": 2**8 - 1,
        },
    }

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
        # logger.info(json.dumps(result_dict, indent=2))

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

        success_rates = [
            category_dict[category]["success"]*100 / category_dict[category]["total"]
            for category in profile_list
        ]

        # Create a bar chart
        x = np.arange(len(profile_list))  # the label locations
        width = 0.4  # the width of the bars

        fig, ax = plt.subplots(figsize=(5, 4))
        bars = ax.bar(x, success_rates, width, label="Success Rate", alpha=alpha)

        # Add some text for labels, title and custom x-axis tick labels, etc.
        ax.set_xlabel("Categories")
        ax.set_ylabel("Success Rate")
        # ax.set_title('Success Rate by Category')
        ax.set_xticks(x)
        ax.set_ylim(0, max(success_rates) + 10)
        ax.set_xticklabels(profile_list)
        # ax.legend()

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
            scenario_dict[cat]["success"]*100 / scenario_dict[cat]["total"] for cat in scenarios
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
        # ax.set_ylim(0, 0.175)
        ax.set_ylim(0, max(success_rates) + 10)
        ax.set_xticklabels(scenarios)
        # ax.legend()

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

        # Display the chart
        plt.savefig("figs/simulation_scenario.pdf")


class Experiment_Case_Study:
    def __init__(self,  contract : Base_Contract):
        self.env = contract.env
        self.contract = contract
        self.init_person()
        self.result_map = {
            RESULT_CODE.GeographicSpecificRestriction: r"\faFlag[regular]",
            RESULT_CODE.OpenToDiseaseSpecific: r"\faCapsules",
            RESULT_CODE.TimeLimitOnUse: r"\faCalendar*[regular]",
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

        r = self.contract.update_area_group_relation()
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
                    access_str.append(self.result_map.get(error,self.error_other))

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
    environment = Environment()
    local_baseline = Contract_Baseline(environment.deploy_contract_local(environment.interface_baseline))
    local_affordable =Contract_Affordable(environment.deploy_contract_local(environment.interface_affordable) )
    # polygon_env = deploy_contract_polygon(force_deploy=False)
    # print(f"accounts {accounts[0]}")
    # test_scenarios(provider_number=10, requester_number=10)
    # date_format = "%S:%M:%H %d-%m-%Y"

    Experiment_Case_Study(local_baseline).start()

    # experiment_simulation =  Experiment_Simulation(local_env,provider_number=30,requester_number = 60)
    # # experiment_simulation.start()
    # experiment_simulation.plot_simulation_category()
    # experiment_simulation.plot_simulation_scenario()

    # logger.info(f"area start date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # # test_area(env=local_env, label="_zero")
    # test_area(env=polygon_env, label="_zero")
    # logger.info(f"area end date (second:minute:hour day-month-year): {datetime.now().strftime(date_format)}")
    # time.sleep(10)
    # plot_area(env=local_env, label="_zero",key_index_name="gas_used",factor = 1e3)
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

    # plot_disease_time(key_index_name="time_used",factor=1e6, y_label="Time usage ($millisecond$)")
    # plot_disease_time(key_index_name="gas_used",factor=1e3, y_label="Gas usage ($10^{3}$)")

    # plot_time()

    # test_polygon()

    # test_case_study( )
