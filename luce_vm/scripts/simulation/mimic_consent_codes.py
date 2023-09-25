import random


class ConsentCodeSimulator:
    def __init__(self):
        self.primary_categories = [
            "NRES", "GRU(CC)", "HMB(CC)", "DS-[XX](CC)", "POA"
        ]

        self.secondary_categories = ["RS-[XX]", "RUO", "NMDS", "GSO"]
        self.requirements = [
            "NPU", "PUB", "COL-[XX]", "IRB", "GS-[XX]", "MOR-[XX]", "TS-[XX]",
            "US", "PS", "IS"
        ]

        # To define any logical constraints or dependencies among codes
        self.constraints = {
            # If "NRES" is chosen, exclude all secondary categories and requirements,
            # as "No restrictions" implies complete openness with no additional conditions.
            "NRES": {
                "exclude": self.secondary_categories + self.requirements
            },

            # If "RUO" (Research use only) is chosen as a secondary category, exclude any
            # contradictory categories or requirements that imply non-research use or commercial use.
            "RUO": {
                "exclude": ["CommercialUseRequirement"]
            },  # Replace with actual codes implying commercial use.

            # "NPU" (Not-for-profit use only) would logically exclude any requirements
            # or conditions related to profit-oriented or commercial use.
            "NPU": {
                "exclude": ["CommercialUseRequirement"]
            },  # Replace with actual codes implying commercial use.

            # "PUB" (Publication required) may have conditional complementarity with "MOR-[XX]"
            # (Publication moratorium/embargo). They can be selected together if the moratorium
            # period is respected, meaning results cannot be published until after the specified date.
            "PUB": {
                "complement": ["MOR-[XX]"]
            },

            # If a disease-specific category "DS-[XX](CC)" is chosen, exclude any contradictory
            # secondary categories or requirements that imply broader or different disease applicability.
            "DS-[XX](CC)": {
                "exclude": ["ContradictoryCategory"]
            },  # Replace with actual contradictory categories.

            # More concrete constraints based on specific definitions, implications,
            # and interactions of each consent code should be added here.
        }

    def generate_random_combination(self):
        primary = random.choice(self.primary_categories)

        possible_secondaries = [
            sec for sec in self.secondary_categories
            if not self.check_constraint(primary, sec)
        ]
        secondaries = random.sample(possible_secondaries,
                                    k=random.randint(
                                        0, len(possible_secondaries)))

        possible_requirements = [
            req for req in self.requirements
            if not any(self.check_constraint(s, req) for s in secondaries)
        ]
        requirements = random.sample(possible_requirements,
                                     k=random.randint(
                                         0, len(possible_requirements)))

        return {
            "primary": primary,
            "secondary": secondaries,
            "requirements": requirements,
        }

    def check_constraint(self, primary, secondary_or_requirement):
        if primary in self.constraints:
            return secondary_or_requirement in self.constraints[primary].get(
                'exclude', [])
        return False

    def validate_combination(self, combination):
        primary = combination['primary']

        for secondary in combination['secondary']:
            if self.check_constraint(primary, secondary):
                return False

        for requirement in combination['requirements']:
            if any(
                    self.check_constraint(s, requirement)
                    for s in combination['secondary']):
                return False

        return True

    def simulate(self):
        valid_combinations = []
        invalid_combinations = []

        for _ in range(10000):  # Replace with desired number of simulations
            combination = self.generate_random_combination()
            if self.validate_combination(combination):
                valid_combinations.append(combination)
            else:
                invalid_combinations.append(combination)

        return valid_combinations, invalid_combinations


simulator = ConsentCodeSimulator()
valid_combinations, invalid_combinations = simulator.simulate()

print("Number of valid combinations: ", len(valid_combinations))
print("Number of invalid combinations: ", len(invalid_combinations))
