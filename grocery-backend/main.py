from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from graph import GroceryStoreGraph
from DistanceRepository import DistanceRepository
from AisleRepository import AisleRepository
from Pathfinder import Pathfinder
import math
from database import AsyncSessionLocal

app = FastAPI()

origins = [
    "http://localhost:5251", # This is the Blazor HTTP address, found in launchSettings.json.
    "https://localhost:7137", # This is the Blazor HTTPS address, found in launchSettings.json.
    ]

# Instantiate the graph right after the FastAPI "app". The graph needs to stay alive in the servers memory but outside of any functions.
graph = GroceryStoreGraph()
graph.map_initialize()

# Enable CORS so the Blazor frontend can access the API and local server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allows GET, POST, PUT, DELETE, etc.
    allow_headers=["*"], # Allows all headers.
)

@app.get("/api/route")
async def fetch_route(start_id: int, end_id: int):

    dr = DistanceRepository()
    ar = AisleRepository()
    pf = Pathfinder(distance_repo=dr)

    async with AsyncSessionLocal() as session:
        aisle_a = await ar.get_aisle(session=session, aisle_id=start_id)
        aisle_b = await ar.get_aisle(session=session, aisle_id=end_id)

        if not aisle_a or not aisle_b:
            errors = []
            if not aisle_a:
                errors.append(start_id)
            if not aisle_b:
                errors.append(end_id)
            
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=errors
            )
        
        if aisle_a.store_id != aisle_b.store_id:
            error_dict = {
                aisle_a.id: aisle_a.store_id,
                aisle_b.id: aisle_b.store_id
            }

            raise HTTPException(
                status_code= status.HTTP_400_BAD_REQUEST,
                detail=error_dict
            )
        
        store_id = aisle_a.store_id
            
        path, total_distance = await pf.find_shortest_path(start_node_id=start_id, end_node_id=end_id, session=session,store_id=store_id)

    return {
        "startLocation": start_id,
        "endLocation": end_id,
        "path": path,
        "totalDistanceFeet": total_distance if not math.isinf(total_distance) else None}

@app.get("/api/aisles/locations")
def get_all_locations():
    """
    Exposes grocery store locations as a JSON array.
    """
    return graph.get_all_locations()