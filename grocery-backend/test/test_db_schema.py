"""Module to create the schema for the test db."""

import sqlite3
import os
import sys

# Using the production 'models' module, the parent directory needs to be added to the search path.
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),"..")) # parent directory one level up.
sys.path.insert(0,parent_dir) # Use '0' to check the parent directory first.

import models # Python must execute the class for the table to be defined. Executing this line accomplishes this.

async def init_db(engine, Base):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

def try_connection():
    try:
        with sqlite3.connect('test_grocery.db') as conn: # Use the 'with' block to guarantee that the connection closes at the end, even if an exception is thrown partway.
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            for table in tables:
                print(f"Table: {table[0]}")
                cursor.execute(f"PRAGMA table_info({table[0]})")
                columns = cursor.fetchall()
                print(f"\nAvailable Columns:")
                for column in columns:
                    print(column[1])
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")