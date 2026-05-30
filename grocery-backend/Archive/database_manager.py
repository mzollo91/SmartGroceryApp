from tracemalloc import start
import pyodbc
import configparser
import os

import Grocery_Item

class DatabaseManager:
    def __init__(self,connection_string):
        self.conn_str = connection_string

    def insert_item(self, item):
        # Take GroceryItem object and persists it to SQL
        sql = """
              INSERT INTO Items (ItemName, WeightOrCount, Units, DepartmentLocation) VALUES (?, ?, ?, ?)
              """
        params = (item.name, item.weight_or_count, item.units, item.department_location)
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    conn.commit()
                    print(f"Successfully saved {item.name} to the database.")
                    return True
                except pyodbc.IntegrityError:
                    print(f"Note: {item.name} exists in the current database and was not added.")
                    return False
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")
                    return False

    def get_all_items(self):
        # Fetches all rows and converts them to Grocery_Item objects
        from Grocery_Item import grocery_item

        items = []
        sql = "SELECT ItemName, WeightOrCount, Units, DepartmentLocation FROM Items"

        with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = grocery_item(row[0], row[1], row[2], row[3])
                        items.append(new_obj)
                    return items

    def delete_item(self, item):
        sql = """
              DELETE FROM Items WHERE ItemID = ?
              """
        params = (item.item_id,)

        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql,params)
                    if cursor.rowcount == 0: # cursor.rowcount doesn't give the number of rows in the db, it gives the number of rows affected by the query.
                        print(f"{item} does not exist in the database.")
                        return False
                    conn.commit()
                    print(f"Successfully deleted {item} from the database.")
                    return True
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
             return False

    def search_items(self, search_term):
        from Grocery_Item import grocery_item
        sql = """
              SELECT ItemName, WeightOrCount, Units, DepartmentLocation, ItemID FROM Items WHERE ItemName LIKE ?
              """
        params = (f"%{search_term}%")

        found_items=[]

        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = grocery_item(row[0], row[1], row[2], row[3], row[4])
                        found_items.append(new_obj)
                    return found_items
                except pyodbc.Error as err:
                    print(f"A SQL specific error occurred: {err}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    def insert_store(self, store):
    # Take Stores object and persists it to SQL
        sql = """
                INSERT INTO Stores (StoreName, StreetAddress, City, State, ZipCode) VALUES (?, ?, ?, ?, ?)
                """
        params = (store.name, store.street_address, store.city, store.state, store.zip_code)
        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    conn.commit()
                    print(f"Successfully saved {store.name} to the database.")
                    return True
                except pyodbc.IntegrityError:
                    print(f"Note: {store.name} exists in the current database and was not added.")
                    return False
                except pyodbc.Error as e:
                    print(f"Database error: {e}")
                    return False

    def get_all_stores(self):
        # Fetches all rows and converts them to Stores objects
        from Stores import store_cl

        stores = []
        sql = "SELECT StoreName, StreetAddress, City, State, ZipCode, StoreID FROM Stores"

        with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = store_cl(row[0], row[1], row[2], row[3], row[4], row[5])
                        stores.append(new_obj)
                    return stores

    def delete_store(self, store):
        cleanup_sql = "DELETE FROM StoreDistances WHERE StoreA_ID = ? OR StoreB_ID = ?"
        
        sql = """
              DELETE FROM Stores WHERE StoreID = ?
              """
        params = (store.store_id,)

        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(cleanup_sql,store.store_id,store.store_id) # Delete affected distance rows first.
                    cursor.execute(sql,params)
                    if cursor.rowcount == 0: # cursor.rowcount doesn't give the number of rows in the db, it gives the number of rows affected by the query.
                        print(f"{store} does not exist in the database.")
                        return False
                    conn.commit()
                    print(f"Successfully deleted {store} from the database.")
                    return True
        except Exception as e:
             print(f"An unexpected error occurred: {e}")
             return False

    def search_stores(self, search_term):
        from Stores import store_cl
        sql = """
              SELECT StoreName, StreetAddress, City, State, ZipCode, StoreID FROM Stores WHERE StoreName LIKE ?
              """
        params = (f"%{search_term}%")

        found_stores=[]

        with pyodbc.connect(self.conn_str) as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql,params)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = store_cl(row[0], row[1], row[2], row[3], row[4], row[5])
                        found_stores.append(new_obj)
                    return found_stores
                except pyodbc.Error as err:
                    print(f"A SQL specific error occurred: {err}")
                except Exception as e:
                    print(f"An unexpected error occurred: {e}")

    def upsert_price(self, item_id, store_id, price):
        check_sql = "SELECT PriceID FROM Prices WHERE ItemID = ? AND StoreID = ?"

        update_sql = "UPDATE Prices SET Price = ?, DateRecorded = GETDATE() WHERE ItemID = ? and StoreID = ?"
        
        insert_sql = """
              INSERT INTO Prices (ItemID, StoreID, Price, DateRecorded)
              VALUES (?, ?, ?, GETDATE())
              """
        params = (item_id, store_id, price)

        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    # Check if item already has a price.
                    cursor.execute(check_sql, (item_id, store_id))
                    row = cursor.fetchone()

                    # If yes, then update.
                    if row:
                        cursor.execute(update_sql, (price, item_id,store_id))
                        print("Price updated successfully.")
                    else:
                        cursor.execute(insert_sql, (item_id, store_id, price))
                        print("New price link created.")
                    conn.commit()
                    return True
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def get_all_prices(self):
        # Fetches all rows and converts them to Stores objects
        from Price_Record import price_record

        prices = []
        sql = "SELECT ItemID, StoreID, Price, DateRecorded FROM Prices"

        with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    cursor.execute(sql)
                    rows = cursor.fetchall()
                    for row in rows:
                        new_obj = price_record(row[0], row[1], row[2], row[3])
                        prices.append(new_obj)
                    return prices

    def add_distance(self,dist_obj):
        
        directions = [(dist_obj.store_a_id, dist_obj.store_b_id),
                      (dist_obj.store_b_id, dist_obj.store_a_id)]
        
        check_sql = "SELECT DistanceID FROM StoreDistances WHERE StoreA_ID = ? AND StoreB_ID = ?"

        update_sql = "UPDATE StoreDistances SET TravelDistance_Minutes = ? WHERE StoreA_ID = ? AND StoreB_ID = ?"
        
        insert_sql = """
              INSERT INTO StoreDistances (StoreA_ID, StoreB_ID, TravelDistance_Minutes)
              VALUES (?, ?, ?)
              """
        #params = (id_a, id_b, time)

        try:
            with pyodbc.connect(self.conn_str) as conn:
                with conn.cursor() as cursor:
                    for start_id, end_id in directions:
                        # Check if item already has a price.
                        cursor.execute(check_sql, (start_id, end_id))
                        row = cursor.fetchone()

                        # If yes, then update.
                        if row:
                            cursor.execute(update_sql, (dist_obj.travel_distance_minutes, start_id, end_id))
                        else:
                            cursor.execute(insert_sql, (start_id, end_id, dist_obj.travel_distance_minutes))
                    conn.commit()
                    print(f"Bi-directional distance between {dist_obj.store_a_name} and {dist_obj.store_b_name} updated successfully.")
                    return True
        except Exception as e:
            print(f"Database error: {e}")
            return False

    def get_all_distances(self):
        from Store_Distance import store_distance

        distances = []
        sql = """
              SELECT
                d.DistanceID,
                d.StoreA_ID, s1.StoreName,
                d.StoreB_ID, s2.StoreName,
                d.TravelDistance_Minutes
              FROM StoreDistances d
              JOIN Stores s1 ON d.StoreA_ID = s1.StoreID
              JOIN Stores s2 ON d.StoreB_ID = s2.StoreID
              """
        try:
            with pyodbc.connect(self.conn_str) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute(sql)
                        rows = cursor.fetchall()
                        for row in rows:
                            new_obj = store_distance(distance_id = row[0], store_a_id = row[1], store_a_name= row[2], store_b_id= row[3], store_b_name = row[4], 
                                                     travel_distance_minutes = row[5])
                            distances.append(new_obj)
                        return distances
        except Exception as e:
            print(f"Error fetching distances: {e}")
            return []