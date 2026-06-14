from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from graph import GroceryStoreGraph

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
def fetch_route(start: str, end: str):
    # This is a dummy placeholder mapping to mimic the Dijkstra output.
    # Actual class to be imported later.

    sample_route = [start, "Store_A", "Store_B", end]

    return {
        "startLocation": start,
        "endLocation": end,
        "stops": sample_route,
        "totalDistanceMiles": 4.2}

@app.get("/api/store/locations")
def get_store_locations():
    """
    Exposes grocery store locations as a JSON array.
    """
    return graph.get_store_locations()