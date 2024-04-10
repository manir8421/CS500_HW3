from common import *
from vehicle import *
from inventory import Inventory
from orderManager import OrderManager

class Dealership:
    def __init__(self, dealer_name, dealer_address, csv_file, order_csv):
        self.__dealer_name = dealer_name
        self.__dealer_address = dealer_address
        self.__inventory = Inventory(csv_file)
        self.__order_manager = OrderManager(order_csv, self.__inventory)


    @property
    def dealer_name(self):
        return self.__dealer_name

    @dealer_name.setter
    def dealer_name(self, value):
        self.__dealer_name = value

    @property
    def dealer_address(self):
        return self.__dealer_address

    @dealer_address.setter
    def dealer_address(self, value):
        self.__dealer_address = value

    @property
    def inventory(self):
        return self.__inventory

    @property
    def order_manager(self):
        return self.__order_manager

    def display_dealer_info(self):
        print(f"\n========== {self.__dealer_name} ==========\n{self.__dealer_address}\n----------------------------------------")

    def add_order_through_manager(self):
        self.order_manager.add_order()

    def initiate_order_process(self):
        self.order_manager.add_order()

    def add_vehicle_to_inventory(self, vehicle):
        self.inventory.add_vehicle(vehicle)
        self.inventory.save_vehicles_to_csv()
        print("Vehicle added successfully and saved to CSV.\n")


    def add_optional_feature_to_vehicle(self, vehicle):
        feature_name = input("Enter the feature name: ")
        feature_price = input("Enter the feature price: ")
        try:
            feature_price = float(feature_price)
            vehicle.add_optional_feature(OptionalFeature(feature_name, feature_price))
        except ValueError:
            print("Price must be a number.")
    
    def is_valid_year(self, year):
        return 1800 <= year <= 2024

    @staticmethod
    def is_positive_number(number):
        return number > 0

    def is_valid_option(self, option, max_option):
        return 1 <= option <= max_option

    def add_preconfigured_vehicle(self):
        vehicle_id = input("Enter a unique ID for the new vehicle: ").upper()
        vehicle_options = ["Sedan", "SUV", "Truck", "Minivan"]
        print("Please select the type of vehicle to add:")
        for index, option in enumerate(vehicle_options, start=1):
            print(f"{index}. {option}")
        vehicle_type_choice = int(input("Your choice (1-4): "))
        vehicle_type = vehicle_options[vehicle_type_choice - 1]
    
        model = input("Enter model: ").upper()
        color = input("Enter color: ").title()
        model_year = self.get_valid_input("Enter model year: ", int, self.is_valid_year, "Please enter a valid year between 1800 and 2024.")
        base_price = BASE_PRICES[vehicle_type]
    
        bed_type = roof_type = None 
    
        if vehicle_type == "Truck":
            print("Select bed type:\n1. Short Bed\n2. Long Bed\n3. None")
            bed_choice = input()
            bed_type_map = {"1": "Short Bed", "2": "Long Bed", "3": None}
            bed_type = bed_type_map.get(bed_choice, "Not Specified")
            vehicle = Truck(id=vehicle_id, bed_type=bed_type, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=[])
    
        elif vehicle_type == "SUV":
            print("Select roof type:\n1. Standard Duty\n2. Heavy Duty\n3. None")
            roof_choice = input()
            roof_type_map = {"1": "Standard Duty", "2": "Heavy Duty", "3": None}
            roof_type = roof_type_map.get(roof_choice, "Not Specified")
            vehicle = SUV(id=vehicle_id, roof_type=roof_type, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=[])

        else:
            vehicle = Vehicle(id=vehicle_id, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=[])

        self.inventory.add_vehicle(vehicle)
        print(f"Vehicle added successfully with ID: {vehicle_id}")

    def get_valid_input(self, prompt, cast_to_type, condition, error_message):
        while True:
            user_input = input(prompt)
            try:
                value = cast_to_type(user_input)
                if condition(value):
                    return value
                else:
                    print(error_message)
            except ValueError:
                print(error_message)


    def print_vehicle_details(self, vehicle):
        print(f"\nTotal Price: ${vehicle.calculate_final_price()}")
        print(f"Vehicle Type: {vehicle.vehicle_type}, Model: {vehicle.model}, Color: {vehicle.color}, Model Year: {vehicle.model_year}, Base Price: ${vehicle.base_price}")
        if vehicle.optional_features:
            print("Optional Features:")
            for feature in vehicle.optional_features:
                print(f"{feature.name} (Price: ${feature.price})")
    
    def search_vehicles(self):
        print("Search Options:")
        print("1. Most Expensive Vehicle")
        print("2. Least Expensive Vehicle")
        print("3. Specific Feature")
        search_choice = input("Choose an option: ")

        if search_choice == '1':
            vehicle = self.inventory.most_expensive_vehicle()
            if vehicle:
                print("\nMost Expensive Vehicle:")
                self.print_vehicle_details(vehicle)

        elif search_choice == '2':
            vehicle = self.inventory.least_expensive_vehicle()
            if vehicle:
                print("\nLeast Expensive Vehicle:")
                self.print_vehicle_details(vehicle)

        elif search_choice == '3':
            print("\nFeatures:")
            print("1. Enhanced Safety Features")
            print("2. Security")
            print("3. Entertainment System")
            print("4. Sunroof")
            feature_choice = input("Select a feature number: ")
            if feature_choice in OPTIONAL_FEATURES:
                selected_feature = OPTIONAL_FEATURES[feature_choice]['name']
                vehicles_with_feature = self.inventory.search_vehicles_by_feature(selected_feature)
                print(f"\nVehicles with {selected_feature}:")
                for vehicle in vehicles_with_feature:
                    self.print_vehicle_details(vehicle)
            else:
                print("Invalid option. Please select a valid feature number.")


    def customize_new_vehicle(self):
        vehicle_id = input("Enter a unique ID for the customized vehicle: ").upper()
        print("Select the type of vehicle to customize:")
        vehicle_types = ["Sedan", "SUV", "Truck", "Minivan"]
        BASE_PRICES = {"Sedan": 30000, "SUV": 40000, "Truck": 35000, "Minivan": 45000}

        for i, v_type in enumerate(vehicle_types, start=1):
            print(f"{i}. {v_type}")

        choice = int(input("Your choice: "))
        vehicle_type = vehicle_types[choice - 1]
        base_price = BASE_PRICES[vehicle_type]

        print(f"Selected {vehicle_type} with base price: ${base_price}")

        model = input("Enter model: ").upper()
        color = input("Enter color: ").title()
        model_year = int(input("Enter model year: "))

        special_attribute = "Not Specified"
        if vehicle_type == "SUV":
            roof_type_choice = input("Choose Roof Type (1. Standard Duty, 2. Heavy Duty, press Enter to skip): ")
            special_attribute = {"1": "Standard Duty", "2": "Heavy Duty"}.get(roof_type_choice, "Not Specified")
        elif vehicle_type == "Truck":
            bed_type_choice = input("Choose Bed Type (1. Short Bed, 2. Long Bed, press Enter to skip): ")
            special_attribute = {"1": "Short Bed", "2": "Long Bed"}.get(bed_type_choice, "Not Specified")

        print("\nAvailable Optional Features (select by number, type 'done' to finish):")
        for key, feature in OPTIONAL_FEATURES.items():
            print(f"{key}. {feature['name']} - ${feature['price']}")

        optional_features_selected = []
        while True:
            feature_choice = input("> ")
            if feature_choice.lower() == 'done':
                break
            if feature_choice in OPTIONAL_FEATURES:
                selected_feature = OPTIONAL_FEATURES[feature_choice]
                optional_features_selected.append(OptionalFeature(selected_feature["name"], selected_feature["price"]))
                print(f"Added {selected_feature['name']}")

        if vehicle_type == "SUV":
            new_vehicle = SUV(id=vehicle_id, roof_type=special_attribute, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=optional_features_selected)
        elif vehicle_type == "Truck":
            new_vehicle = Truck(id=vehicle_id, bed_type=special_attribute, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=optional_features_selected)
        else:
            new_vehicle = Vehicle(id=vehicle_id, vehicle_type=vehicle_type, model=model, color=color, model_year=model_year, base_price=base_price, optional_features=optional_features_selected)

        self.inventory.add_vehicle(new_vehicle)
        print(f"\nCustomized {vehicle_type} added successfully with total price: ${new_vehicle.calculate_final_price()}.\n")


    def display_all_vehicles(self):
        print("\nAll Vehicles in Inventory:")
        if not self.inventory.vehicles:
            print("Inventory is empty.")
        else:
            for vehicle in self.inventory.vehicles:
                print(vehicle)


    def remove_vehicle(self):
        vehicle_id = input("Enter the ID of the vehicle to remove: ").upper().strip()
        vehicle_to_remove = None
        for vehicle in self.inventory.vehicles:
            if str(vehicle.id) == vehicle_id:
                vehicle_to_remove = vehicle
                break
        
        if vehicle_to_remove:
            self.inventory.vehicles.remove(vehicle_to_remove)
            self.inventory.save_vehicles_to_csv()
            print(f"Vehicle with ID {vehicle_id} removed successfully.")
        else:
            print("No vehicle found with the given ID.")

    def exit_program(self):
        print("Exit the program. Thank you...")
        exit()


    def view_inventory(self):
        print(self.inventory)

    def print_order_with_vehicle_info(self, order, inventory):
        print(f"Order ID: {order.id}")
        print(f"Customer Name: {order.customer_name}")
        print(f"Order Date: {order.order_date}")
        print("Vehicles:")
        for vehicle_id in order.vehicle_ids:
            vehicle = inventory.find_vehicle_by_id(vehicle_id)
            if vehicle:
                print(f"ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.calculate_final_price()}")
            else:
                print(f"Vehicle ID {vehicle_id} not found.")
        print("")

    def view_orders(self):
        if not self.order_manager.orders:
            print("No orders available.")
        else:
            for order in self.order_manager.orders:
                print(order.__str__(self.inventory)) 


    def remove_order(self):
        order_id = input("Enter the ID of the order to remove: ").upper().strip()
        if self.order_manager.remove_order(order_id):
            print("Order removed successfully.")
        else:
            print("")
