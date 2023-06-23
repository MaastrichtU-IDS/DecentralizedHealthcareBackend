class SingletonMeta(type):
    """
    singleton pattern
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Counter(metaclass=SingletonMeta):
    def __init__(self):
        self.count = 0

    def get_count(self):
        self.count = self.count + 1
        return self.count


def get_registration_data():

    # a template for registration data
    template = {
        "last_name": "test_user",
        "email": "email@email.com",
        "password": "password123",
        "create_wallet": True,
        "user_type": 0
    }

    registration_data = template
    counter = Counter()

    registration_data['email'] = "email" + str(
        counter.get_count()) + "@email.com"

    return registration_data