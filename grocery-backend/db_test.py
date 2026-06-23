""""A simple test for a SQLite DB"""

import asyncio
from database import engine, Base
import models # Python must execute the class for the table to be defined. Executing this line accomplishes this.
import sqlite3

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

def test_connection():
    try:
        conn = sqlite3.connect('grocery.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        for table in tables:
            print(table)
            table_info = cursor.execute("PRAGMA table_info()")
            print(table_info)
        
    except Exception as e:
        print(f"Error connecting to the database: {e}")

if __name__ == "__main__":
    #asyncio.run(init_db())
    test_connection()