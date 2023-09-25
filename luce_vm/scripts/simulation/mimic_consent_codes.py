import random


class ConsentCodeSimulator:
    def __init__(self):
        self.primary_categories = [
            "NRES", "GRU(CC)", "HMB(CC)", "DS-[XX](CC)", "POA"
        ]
        self.secondary_categories = ["RS-[XX]", "RUO", "NMDS", "GSO"]
        self.requirements = [
            "NPU", "PUB", "IRB", "GS-[XX]", "MOR-[XX]", "TS-[XX]", "US", "PS",
            "IS"
        ]

    def get_valid_consent_codes(self):

        valid_codes = {}
        is_valid = False
        while not is_valid:
            consent_code = self.generate_consent_code()
            is_valid = self.validate_consent_code(consent_code['Primary'],
                                                  consent_code['Secondary'],
                                                  consent_code['Requirements'])
        return consent_code

    def random_num_secondary_categories(self):
        return random.randint(0, len(self.secondary_categories))

    def random_num_requirements(self):
        return random.randint(0, len(self.requirements))

    def select_primary_category(self):
        return random.choice(self.primary_categories)

    def select_secondary_categories(self, num_categories):
        return random.sample(self.secondary_categories, num_categories)

    def select_requirements(self, num_requirements):
        return random.sample(self.requirements, num_requirements)

    def generate_consent_code(self):
        primary = self.select_primary_category()
        num_secondary = self.random_num_secondary_categories()
        num_requirements = self.random_num_requirements()
        secondaries = self.select_secondary_categories(num_secondary)
        requirements = self.select_requirements(num_requirements)

        return {
            'Primary': primary,
            'Secondary': secondaries,
            'Requirements': requirements
        }

    def validate_consent_code(self, primary, secondaries, requirements):
        # No Restrictions (NRES) Rule: When "No restrictions" is the primary category, no secondary categories or requirements should be allowed, as it defeats the purpose of "no restrictions."
        if primary == 'NRES' and (len(secondaries) > 0
                                  or len(requirements) > 0):
            return False

        # Disease-Specific (DS) Rule: When selecting a disease-specific primary category, there should be at least one requirement, as disease-specific data usually have stringent constraints.
        if primary.startswith('DS-') and len(requirements) == 0:
            return False

        # Research Use Only (RUO) Rule: If "Research use only" is chosen as a secondary category, "General research use and clinical care" should not be the primary category, since clinical care is not just for research.
        if primary == 'GRU(CC)' and 'RUO' in secondaries:
            return False

        # Genetic Studies Only (GSO) Rule: If this is a secondary category, "Publication required" should be a requirement to ensure ethical usage of genetic data.
        if 'GSO' in secondaries and 'PUB' not in requirements:
            return False

        # Not-for-profit use only (NPU) Rule: If this is a requirement, "General research use and clinical care" should not be the primary category, as clinical care might involve for-profit healthcare providers.
        if primary == 'GRU(CC)' and 'NPU' in requirements:
            return False

        # ... (add more rules as necessary)

        return True  # Return True if all validation rules pass


# Create an instance of this class
simulator = ConsentCodeSimulator()

# Generate a consent code with 2 secondary categories and 3 requirements
consent_code = simulator.generate_consent_code()

print(f"Generated Consent Code: {consent_code}")

# Validate the consent code
is_valid = simulator.validate_consent_code(consent_code['Primary'],
                                           consent_code['Secondary'],
                                           consent_code['Requirements'])

print(f"Is Valid: {is_valid}")

# Generate a valid consent code
valid_consent_code = simulator.get_valid_consent_codes()
print(f"Valid Consent Code: {valid_consent_code}")
