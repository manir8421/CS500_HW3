from dealership import Dealership

dealer_name = "XYZ Car Dealership"
dealer_address = "161 Mission Falls Ln., Fremont, CA 94539"
inventory_csv = 'vehicles.csv'
orders_csv = 'orders.csv'
dealership = Dealership(dealer_name, dealer_address, inventory_csv, orders_csv)

def main_menu():
    while True:
        dealership.display_dealer_info()
        print("Main Menu:\n==========")
        print("1. Inventory Management")
        print("2. Order Management")
        print("3. Exit")
        choice = input("\nSelect an option: ")
        if choice == "1":
            inventory_management(dealership)
        elif choice == "2":
            order_management(dealership)
        elif choice == "3":
            print("Exiting program...")
            exit()
        else:
            print("Invalid option. Please try again.")

def inventory_management(dealership):
    while True:
        print("\nInventory Management:\n=====================")
        print("1. Add a Preconfigured Vehicle")
        print("2. Customize New Vehicle")
        print("3. Search Vehicles")
        print("4. Display All Vehicles")
        print("5. Remove a Vehicle")
        print("6. Return to Main Menu")
        print("7. Exit Program")

        choice = input("\nSelect an option: ")
        if choice == "1":
            dealership.add_preconfigured_vehicle()
        elif choice == "2":
            dealership.customize_new_vehicle()
        elif choice == "3":
            dealership.search_vehicles()
        elif choice == "4":
            dealership.display_all_vehicles()
        elif choice == "5":
            dealership.remove_vehicle()
        elif choice == "6":
            break
        elif choice == "7":
            print("Exiting program...")
            exit()
        else:
            print("Invalid option. Please try again.")

def order_management(dealership):
    while True:
        print("\nOrder Management:\n=================")
        print("1. Add New Order")
        print("2. View All Orders")
        print("3. Remove an Order")
        print("4. Return to Main Menu")
        print("5. Exit Program")

        choice = input("\nSelect an option: ")
        if choice == "1":
            dealership.initiate_order_process()
        elif choice == "2":
            dealership.view_orders()
        elif choice == "3":
            dealership.remove_order()
        elif choice == "4":
            break
        elif choice == "5":
            print("Exiting program...")
            exit()
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main_menu()
