from order import Order
import csv

class OrderManager:
    def __init__(self, order_csv, inventory):
        self.__order_csv = order_csv
        self.__inventory = inventory
        self.__orders = []
        self.load_orders(self.__inventory)

    @property
    def order_csv(self):
        return self.__order_csv

    @property
    def inventory(self):
        return self.__inventory

    @property
    def orders(self):
        return self.__orders

    def display_vehicles_with_id(self):
        print("Vehicale list in the inventory:")
        print("-" * 31)
        for vehicle in self.__inventory.vehicles:
            print(f"ID: {vehicle.id}, Model: {vehicle.model}, Price: ${vehicle.calculate_final_price()}")

    def order_id_exists(self, order_id):
        return any(order.id == order_id for order in self.__orders)

    def remove_order(self, order_id):
        order_to_remove = next((order for order in self.__orders if str(order.id) == order_id), None)
        
        if order_to_remove:
            self.__orders.remove(order_to_remove)
            self.save_orders()
            print(f"Order {order_id} removed successfully.")
        else:
            print(f"Order {order_id} not found.")

            
    def add_order(self):
        self.display_vehicles_with_id()
        order_id = input(f"\nEnter a unique ID for the order: ").upper()
        existing_order = next((order for order in self.orders if order.id == order_id), None)

        if existing_order:
            print("Adding another vehicle to existing order.")
        else:
            customer_name = input("Enter the customer's name for the order: ").title()
            order_date = input("Enter the date for the order (YYYY-MM-DD): ")
            existing_order = Order(order_id, customer_name, order_date)
            self.orders.append(existing_order)  

        while True:
            vehicle_id = input("Enter the ID of the vehicle to order: ").upper()
            vehicle = self.inventory.find_vehicle_by_id(vehicle_id)
            if vehicle:
                existing_order.add_vehicle_id(vehicle_id)
                print(f"Vehicle {vehicle_id} added to order {order_id}.")
                another_vehicle = input("Order another vehicle under the same order ID? (y/n): ").lower()
                if another_vehicle.lower() != 'y':
                    break
            else:
                print("Vehicle not found. Please try again.")

        self.save_orders()


    def add_vehicle_to_order(self, order_id, vehicle_id):
        existing_order = next((order for order in self.orders if order.id == order_id), None)
        if existing_order:
            vehicle = self.inventory.find_vehicle_by_id(vehicle_id)
            if vehicle:
                existing_order.vehicle.append(vehicle) 
                print(f"Added vehicle to order {order_id}.")
            else:
                print("Vehicle not found.")
        else:
            print("Order not found.")

    def calculate_and_display_order_totals(self, order_id):
        order = next((order for order in self.orders if order.id == order_id), None)
        if order:
            total_price = sum(vehicle.calculate_final_price() for vehicle in order.vehicle)
            print(f"Order ID: {order_id}\nTotal Price: ${total_price}")
            for vehicle in order.vehicle:
                print(f"Vehicle: {vehicle.model}, Price: ${vehicle.calculate_final_price()}")
        else:
            print("Order not found.")

            
    def load_orders(self, inventory):
        orders = []
        try:
            with open(self.__order_csv, 'r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    order_id = row.get('order_id')
                    vehicle_ids = row.get('vehicle_ids', '').split(';')
                    customer_name = row.get('customer_name')
                    order_date = row.get('order_date')
            
                    order = Order(order_id, customer_name, order_date)
                    for vid in vehicle_ids:
                        order.add_vehicle_id(vid)
                    orders.append(order)
        except FileNotFoundError:
            print(f"Order file {self.__order_csv} not found. A new one will be created.")
        self.__orders = orders

        
    def save_orders(self):
        with open(self.__order_csv, 'w', newline='') as file:
            fieldnames = ['order_id', 'vehicle_ids', 'customer_name', 'order_date']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for order in self.__orders:
                vehicle_ids_str = ';'.join(order.vehicle_ids)
                writer.writerow({
                    'order_id': order.id,
                    'vehicle_ids': vehicle_ids_str,
                    'customer_name': order.customer_name,
                    'order_date': order.order_date
                })
                
    def view_orders(self):
        if not self.__orders:
            print("No orders available.")
        else:
            for order in self.__orders:
                print(order.__str__(self.__inventory))
       