from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS so the Blazor frontend can access the API and local server.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/route")
def fet_route(start: str, end: str):
    # This is a dummy placeholder mapping to mimic the Dijkstra output.
    # Actual class to be imported later.

    sample_route = [start, "Store_A", "Store_B", end]

    return {
        "startLocation": start,
        "endLocation": end,
        "stops": sample_route,
        "totalDistanceMiles": 4.2}