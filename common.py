BASE_PRICES = {
    "Sedan": 30000,
    "SUV": 40000,
    "Truck": 35000,
    "Minivan": 45000
}

OPTIONAL_FEATURES = {
    "1": {"name": "Enhanced Safety features", "price": 3000},
    "2": {"name": "Security", "price": 1000},
    "3": {"name": "Entertainment System", "price": 2000},
    "4": {"name": "Sunroof", "price": 2500},
}

class OptionalFeature:
    def __init__(self, name: str, price):
        self.__name = name
        self.__price = price

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price