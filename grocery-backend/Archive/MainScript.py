from logging import config

from Grocery_Item import grocery_item
from Pathfinder import Pathfinder
from Stores import store_cl
from Price_Record import price_record
from Store_Distance import store_distance
from database_manager import DatabaseManager
import configparser

def search_and_select(items):
    if items:
        for idx, item in enumerate(items,1):
            print(f"[{idx}] {item}")
        while True:
            try:
                choice = int(input("Select a number or enter '0' to exit: "))
                if choice == 0:
                    return None
                else:
                    try:
                        selected_item = items[choice-1]
                        return selected_item

                    except:
                        print("Invalid Selection!")
            except ValueError:
                print("Not a valid input!")


def main_menu():

    # Load the configuration file.
    config_file = 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_file)

    # Create the DB connection
    db_config = config['database']
    conn_str = (f"Driver={db_config['driver']};"
                f"Server={db_config['server']};"
                f"Database={db_config['database']};"
                f"Trusted_Connection={db_config['trusted_connection']};")
    
    db = DatabaseManager(conn_str)
    
    while True:
        print("\n=== GROCERY PLANNER 2026 ===")
        print("1. Manage Items")
        print("2. Manage Stores")
        print("3. Manage Prices")
        print("4. Manage Distances")
        print("Q. Exit")

        choice = input("\nSelect an option: ").lower()

        if choice == '1':
            item_submenu(db)
        elif choice == '2':
            store_submenu(db)
        elif choice == '3':
            prices_submenu(db)
        elif choice == '4':
            distances_submenu(db)
        elif choice == 'q':
            print("Goodbye!")
            break
        else:
            print("Invalid selection.")
    
def item_submenu(db):
    while True:
        print("\n--- ITEM MANAGEMENT ---")
        print("1. Add Item")
        print("2. View All Items")
        print("3. Delete Item")
        print("4. Search Item")
        print("5. Back to Main Menu")
        choice = input("Select an option: ")

        if choice == '1':
            name = input("Item Name: ")
            try:
                weight_or_count = float(input("Item weight or count per package: "))
            except ValueError:
                print("Invalid input, please enter a number for weight.")
                continue
            units = input("Units: ")
            department_location = input("OPTIONAL Department location in store: ")

            new_item = grocery_item(name=name, weight_or_count=weight_or_count,units=units,department_location=department_location)
            new_item.save_to_db(db)

        elif choice == '2':
            items = db.get_all_items()
            for item in items:
                print(item)
                #print(f"{item.name} ({item.weight_or_count} {item.units}), {item.department_location} department.")

        elif choice == '3':
            selected_item = None
            name = input(f"Enter the name of the item to delete: ")
            found_items = db.search_items(name)
            if found_items:
                selected_item = search_and_select(found_items)
                if selected_item:
                    confirm = input(f"Are you sure want to delete '{selected_item}'? (y/n): ")
                else:
                    print("No valid item selected.")
                    confirm = 'n'
            else:
                print("No item selected.")
                confirm = 'n'

            if confirm.lower() == 'y':
                db.delete_item(selected_item)
            else:
                print("Deletion cancelled.")

        elif choice == '4':
            name = input("Enter item to search: ")
            found_items = db.search_items(name)
            if found_items:
                for item in found_items:
                    print(item)
            else:
                print(f"{name} not found in database.")

        elif choice == '5':
            break
        
        else:
            print("Invalid selection.")

def store_submenu(db):
    while True:
        print("\n--- STORE MANAGEMENT ---")
        print("1. Add Store")
        print("2. View All Stores")
        print("3. Delete Store")
        print("4. Search Store")
        print("5. Back to Main Menu")
        choice = input("Select an option: ").lower()

        if choice == '1':
            name = input("Store Name: ")
            street_address = input("Street Address: ")
            city = input("City: ")
            
            while True:
                state = input("State (abbrevation): ").upper()
                if len(state) == 2:
                    break
                else:
                    print("Enter the two letter abbreviation for the state.")

            zip_code = input("Zip Code: ")
            new_store = store_cl(name=name, street_address=street_address,city=city, state=state, zip_code=zip_code)
            new_store.save_to_db(db)

        elif choice == '2':
            stores = db.get_all_stores()
            for s in stores:
                print(s)

        elif choice == '3':
            selected_store = None
            name = input(f"Enter the name of the store to delete: ")
            found_stores = db.search_stores(name)
            if found_stores:
                selected_store = search_and_select(found_stores)
                if selected_store:
                    confirm = input(f"Are you sure want to delete '{selected_store}'? (y/n): ")
                else:
                    print("No valid store selected.")
                    confirm = 'n'
            else:
                print("No store selected.")
                confirm = 'n'

            if confirm.lower() == 'y':
                db.delete_store(selected_store)
            else:
                print("Deletion cancelled.")

        elif choice == '4':
            name = input("Enter store to search: ")
            found_stores = db.search_stores(name)
            if found_stores:
                for store in found_stores:
                    print(store)
            else:
                print(f"{name} not found in database.")

        elif choice == '5':
            break

        else:
            print("Invalid selection.")

def prices_submenu(db):
    while True:
        print("\n--- PRICES MANAGEMENT ---")
        print("1. Insert/Update Price")
        print("2. View All Prices")
        print("3. Back to Main Menu")
        choice = input("Select an option: ").lower()

        if choice == '1':
            while True:
                item_name = input("Enter item to search: ")
                found_items = db.search_items(item_name)
                if found_items:
                    item = search_and_select(found_items)
                    if item:
                        item_id = item.item_id

                    else:
                        print("No item selected.")
                        break
                else:
                    print(f"'{item_name}'' not found in database.")
                    break

                store_name = input("Enter store to search: ")
                found_stores = db.search_stores(store_name)
                if found_stores:
                    store = search_and_select(found_stores)
                    if store:
                        store_id = store.store_id
                    else:
                        print("No store selected.")
                        break
                else:
                    print(f"'{store_name}'' not found in database.")
                    break

                try:
                    price = float(input("Enter the price of item: "))
                except ValueError:
                    print("Invalid input, please enter a number for prices.")
                    continue
                db.upsert_price(item_id, store_id, price)
                break

        elif choice == '2':
            prices = db.get_all_prices()
            for p in prices:
                print(p)

        elif choice == '3':
            break

        else:
            print("Invalid selection.")

def distances_submenu(db):
    while True:
        print("\n--- STORE DISTANCES MANAGEMENT ---")
        print("1. Insert/Update Distance")
        print("2. View All Distances")
        print("3. Back to Main Menu")
        choice = input("Select an option: ").lower()

        if choice == '1':
            while True:
                store_a_name = input("Start point store name: ")
                found_stores = db.search_stores(store_a_name)
                if found_stores:
                    store_a = search_and_select(found_stores)
                    if store_a:
                        id_a = store_a.store_id

                    else:
                        print("No store selected.")
                        break
                else:
                    print(f"'{store_a_name}'' not found in database.")
                    break

                store_b_name = input("End point store name: ")
                found_stores = db.search_stores(store_b_name)
                if found_stores:
                    store_b = search_and_select(found_stores)
                    if store_b:
                        id_b = store_b.store_id

                    else:
                        print("No store selected.")
                        break
                else:
                    print(f"'{store_b_name}'' not found in database.")
                    break

                try:
                    distance_time = float(input("Enter the distance between locations in minutes: "))
                except ValueError:
                    print("Invalid input, please enter a number for distance.")
                    continue
                dist_obj = store_distance(store_a_id = id_a, store_a_name = store_a.name, store_b_id = id_b, store_b_name = store_b.name, travel_distance_minutes = distance_time)
                dist_obj.save_to_db(db)
                break

        elif choice == '2':
            distances = db.get_all_distances()
            row = 1
            for d in distances:
                if row % 2 == 0:
                    print(d)
                else:
                    print(f"\n{d}")
                row += 1


        elif choice == '3':
            break

        else:
            print("Invalid selection.")

main_menu()

# Load the configuration file.
config_file = 'config.ini'
config = configparser.ConfigParser()
config.read(config_file)

# Create the DB connection
db_config = config['database']
conn_str = (f"Driver={db_config['driver']};"
            f"Server={db_config['server']};"
            f"Database={db_config['database']};"
            f"Trusted_Connection={db_config['trusted_connection']};")
    
db = DatabaseManager(conn_str)
pathfinder = Pathfinder(db)
route, minutes = pathfinder.find_shortest_path("Home", "GIANT")

print(f"Optimal Route: {' -> '.join(route)}")
print(f"Total Travel Time: {minutes} minutes")
