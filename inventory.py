from common import *
from vehicle import *
import csv
class Inventory:
    def __init__(self, csv_file: str):
        self.__csv_file = csv_file
        self.__vehicles = self.load_vehicles_from_csv()

    @property
    def vehicles(self):
        return self.__vehicles

    @vehicles.setter
    def vehicles(self, value):
        self.__vehicles = value
 
    
    def get_vehicle_price(self, vehicle):
        return vehicle.calculate_final_price()

    def most_expensive_vehicle(self):
        if not self.vehicles:
            print("No vehicles in inventory.")
            return None
        most_expensive = max(self.vehicles, key=self.get_vehicle_price)
        return most_expensive
    
    def least_expensive_vehicle(self):
        if not self.vehicles:
            print("No vehicles in inventory.")
            return None
        least_expensive = min(self.vehicles, key=self.get_vehicle_price)
        return least_expensive
    

    def search_vehicles_by_feature(self, feature_name):
        return [vehicle for vehicle in self.vehicles if any(feat.name == feature_name for feat in vehicle.optional_features)]

    def load_vehicles_from_csv(self):
        vehicles = []
        try:
            with open(self.__csv_file, mode='r', newline='') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    vehicle_id = row.get('id', '') 

                    model_year = int(row.get('model_year', 0))
                    base_price = float(row.get('base_price', 0))
                    optional_features_str = row.get('optional_features', "")
                    optional_features = self.parse_optional_features(optional_features_str)

                    if row['vehicle_type'].lower() == 'truck':
                        vehicle = Truck(bed_type=row.get('bed_type', 'Not Specified'), vehicle_type=row['vehicle_type'], model=row['model'], color=row['color'], model_year=model_year, base_price=base_price, optional_features=optional_features, id=vehicle_id)
                    elif row['vehicle_type'].lower() == 'suv':
                        vehicle = SUV(roof_type=row.get('roof_type', 'Not Specified'), vehicle_type=row['vehicle_type'], model=row['model'], color=row['color'], model_year=model_year, base_price=base_price, optional_features=optional_features, id=vehicle_id)
                    else:
                        vehicle = Vehicle(id=vehicle_id, vehicle_type=row['vehicle_type'], model=row['model'], color=row['color'], model_year=model_year, base_price=base_price, optional_features=optional_features)
            
                    vehicles.append(vehicle)
        except FileNotFoundError:
            print("CSV file not found.")
        except ValueError as e:
            print(f"Error processing CSV file: {e}")
        return vehicles

    
    def parse_optional_features(self, optional_features_str):
        optional_features = []
        if optional_features_str:
            features_list = optional_features_str.split(';')
            for feature_str in features_list:
                name, price = feature_str.split(',')
                price = float(price)
                optional_features.append(OptionalFeature(name, price))
        return optional_features

    
    def save_vehicles_to_csv(self):
        try:
            with open(self.__csv_file, 'w', newline='') as file:
                fieldnames = ['id', 'vehicle_type', 'model', 'color', 'model_year', 'base_price', 'optional_features', 'bed_type', 'roof_type']
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for vehicle in self.__vehicles:
                    row_data = {
                        'id': vehicle.id,
                        'vehicle_type': vehicle.vehicle_type,
                        'model': vehicle.model,
                        'color': vehicle.color,
                        'model_year': vehicle.model_year,
                        'base_price': str(vehicle.base_price),
                        'optional_features': ";".join([f"{feature.name},{feature.price}" for feature in vehicle.optional_features]),
                        'bed_type': getattr(vehicle, 'bed_type', ''),
                        'roof_type': getattr(vehicle, 'roof_type', '')
                    }
                    writer.writerow(row_data)
            print("Updated CSV file successfully.")
        except Exception as e:
            print(f"Failed to update CSV file: {e}")


    def add_vehicle(self, vehicle):
        self.__vehicles.append(vehicle)
        self.save_vehicles_to_csv()


    def find_vehicle_by_id(self, vehicle_id):
        for vehicle in self.vehicles:
            if str(vehicle.id) == vehicle_id:
                return vehicle
        return None
   