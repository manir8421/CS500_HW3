from typing import Optional

from common import OptionalFeature

class Vehicle:
    def __init__(self, id: str, vehicle_type: str, model: str, color: str, model_year: int, base_price: float, optional_features: Optional[list[OptionalFeature]] = None):
        self.id = id
        self.__vehicle_type = vehicle_type
        self.__model = model
        self.__color = color
        self.__model_year = model_year
        self.__base_price = base_price
        self.__optional_features = optional_features if optional_features else []

    @property
    def vehicle_type(self):
        return self.__vehicle_type

    @property
    def model(self):
        return self.__model

    @property
    def color(self):
        return self.__color

    @property
    def model_year(self):
        return self.__model_year
    
    @property
    def base_price(self):
        return self.__base_price

    @property
    def optional_features(self):
        return self.__optional_features

    def add_optional_feature(self, feature: OptionalFeature):
        self.__optional_features.append(feature)

    def calculate_final_price(self):
        return self.base_price + sum(feature.price for feature in self.optional_features)

    def __str__(self):
        features_str = "; ".join([f"({feature.name}, Price: ${feature.price})" for feature in self.optional_features]) if self.optional_features else "No additional features"
        total_price = self.calculate_final_price()
        return (f"\nID: {self.id}\nTotal Price: ${total_price}\nVehicle Type: {self.vehicle_type}, Model: {self.model}, Color: {self.color}, "
                f"Model Year: {self.model_year}, Base Price: ${self.base_price}\n"
                f"[{features_str}]")

class Truck(Vehicle):
    def __init__(self, bed_type: str | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__bed_type = bed_type

    @property
    def bed_type(self):
        return self.__bed_type

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Bed Type: {self.bed_type}"
    
class SUV(Vehicle):
    def __init__(self, roof_type: str | None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__roof_type = roof_type

    @property
    def roof_type(self):
        return self.__roof_type

    def __str__(self):
        base_str = super().__str__()
        return f"{base_str}, Roof Type: {self.roof_type}"