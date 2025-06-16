from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from datetime import datetime
from traveltimepy import TravelTimeSdk, Coordinates, PublicTransport, FullRange
import os
import dotenv
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

dotenv.load_dotenv()

sdk = TravelTimeSdk(app_id=os.getenv("TIME_APP_ID"), api_key=os.getenv("TIME_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with ["http://localhost:3000"] etc. for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommuteRequest(BaseModel):
    home_location: str
    office_locations: List[str]

class LocationWithTime(BaseModel):
    id: str
    lat: float
    lng: float
    travel_time_minutes: float

@app.post("/commute", response_model=List[LocationWithTime])
async def compute_commute(data: CommuteRequest):
    home_location = data.home_location
    office_locations = data.office_locations

    if not home_location or not office_locations:
        raise HTTPException(status_code=400, detail="Missing home or office locations.")

    # Geocode home
    home_geo = await sdk.geocoding_async(query=home_location, limit=1)
    if not home_geo.features:
        raise HTTPException(status_code=404, detail=f"Home location not found: {home_location}")
    home_coords_raw = home_geo.features[0].geometry.coordinates
    home_coords = Coordinates(lat=home_coords_raw.latitude, lng=home_coords_raw.longitude)

    # Geocode offices
    office_coords = []
    valid_offices = []
    for office in office_locations:
        geo = await sdk.geocoding_async(query=office, limit=1)
        if geo.features:
            coord = geo.features[0].geometry.coordinates
            office_coords.append(Coordinates(lat=coord.latitude, lng=coord.longitude))
            valid_offices.append(office)

    if not valid_offices:
        raise HTTPException(status_code=404, detail="No valid office locations found.")

    # Build locations
    locations = [{"id": "home", "coords": home_coords}]
    for office, coord in zip(valid_offices, office_coords):
        locations.append({"id": office, "coords": coord})

    search_ids = {"home": valid_offices}

    res = await sdk.time_filter_async(
        locations=locations,
        search_ids=search_ids,
        departure_time=datetime.now(),
        travel_time=3600,
        transportation=PublicTransport(),
        range=FullRange(enabled=True, max_results=3, width=600)
    )

    output = [
        LocationWithTime(
            id="home",
            lat=home_coords.lat,
            lng=home_coords.lng,
            travel_time_minutes=0.0
        )
    ]

    for result in res:
        for location in result.locations:
            times = [round(p.travel_time / 60, 2) for p in location.properties]
            if times:
                min_time = min(times)
                matched = next((loc for loc in locations if loc["id"] == location.id), None)
                if matched:
                    coords = matched["coords"]
                    output.append(LocationWithTime(
                        id=location.id,
                        lat=coords.lat,
                        lng=coords.lng,
                        travel_time_minutes=min_time
                    ))

    print(output)
    return output

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
