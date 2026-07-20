"""Module to create the schema for the test db."""

import asyncio
from test_db_engine import engine, Base
import models # Python must execute the class for the table to be defined. Executing this line accomplishes this.
import sqlite3

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

def test_connection():
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

if __name__ == "__main__":
    #asyncio.run(init_db())
    test_connection()