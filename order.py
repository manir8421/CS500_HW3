class Order:
    def __init__(self, order_id, customer_name, order_date):
        self.__id = order_id
        self.__customer_name = customer_name
        self.__order_date = order_date
        self.__vehicle_ids = []

    @property
    def id(self):
        return self.__id

    @property
    def customer_name(self):
        return self.__customer_name

    @customer_name.setter
    def customer_name(self, value):
        self.__customer_name = value

    @property
    def order_date(self):
        return self.__order_date

    @order_date.setter
    def order_date(self, value):
        self.__order_date = value

    @property
    def vehicle_ids(self):
        return self.__vehicle_ids

    def add_vehicle_id(self, vehicle_id):
        if vehicle_id not in self.__vehicle_ids:
            self.__vehicle_ids.append(vehicle_id)

    def calculate_total_price(self, inventory):
        total_price = sum(inventory.find_vehicle_by_id(vid).calculate_final_price() for vid in self.__vehicle_ids if inventory.find_vehicle_by_id(vid))
        return total_price

    def __str__(self, inventory):
        vehicle_details = "\n".join([str(inventory.find_vehicle_by_id(vid)) for vid in self.__vehicle_ids if inventory.find_vehicle_by_id(vid)])
        total_price = self.calculate_total_price(inventory)
        return (f"\nOrder ID: {self.__id}\n"
                f"Customer Name: {self.__customer_name}\n"
                f"Order Date: {self.__order_date}\n"
                f"Total Order Price: ${total_price}\n"
                f"\nVehicles:{vehicle_details}"
                f"\n-------------------")
   