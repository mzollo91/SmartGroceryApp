""""A simple test for a SQLite DB"""

import asyncio
from database import engine, Base
import models # Python must execute the class for the table to be defined. Executing this line accomplishes this.

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables created successfully.")

if __name__ == "__main__":
    asyncio.run(init_db())