from datetime import datetime
import asyncio
from traveltimepy import TravelTimeSdk, Coordinates, Driving, PublicTransport, FullRange
import os
import dotenv


dotenv.load_dotenv()

sdk = TravelTimeSdk(app_id=os.getenv("TIME_APP_ID"), api_key=os.getenv("TIME_API_KEY"))


async def main():
    default_offices = ["Sloane Square, London", "Holborn, London", "Regents place, London"]
    default_home = "Goldsmid House, London"

    # get office locations from user input or use default
    use_default = input("Do you want to use default office and home locations? (yes/no): ").strip().lower()
    if use_default == 'yes':
        office_locations = default_offices
        home_location = default_home
    elif use_default == 'no':
        office_locations = []
        home_location = ""
    else:
        print("Invalid input. Exiting.")
        return
    
    # if user chose not to use default, get office locations from user input
    if not office_locations:
        # get office locations from user input until they dont need anymore
        office_locations = []
        while True:
            office_location = input("Enter the office location (or type 'done' to finish): ")
            if office_location.lower() == 'done':
                break
            office_locations.append(office_location)

        if not office_locations:
            print("No office locations provided. Exiting.")
            return
        
        # get home location from user input
        home_location = input("Enter your home location: ")
        if not home_location:
            print("No home location provided. Exiting.")
            return
    
    # Geocode office locations
    office_coords = []
    for office_location in office_locations:
        results = await sdk.geocoding_async(query=office_location, limit=1)
        if results.features:
            office_coords.append((
                results.features[0].geometry.coordinates.latitude, 
                results.features[0].geometry.coordinates.longitude
            ))
        else:
            print(f"No results found for office location: {office_location}")
    
    if not office_coords:
        print("No valid office locations found. Exiting.")
        return
    
    # Get coordinates for home location
    home_coords = await sdk.geocoding_async(query=home_location, limit=1)
    if not home_coords.features:
        print(f"No results found for home location: {home_location}")
        return
    
    home_coords = home_coords.features[0].geometry.coordinates.latitude, home_coords.features[0].geometry.coordinates.longitude
    home_coords = Coordinates(
        lat=home_coords[0],
        lng=home_coords[1]
    )

    

    locations = [{"id": "home", "coords": home_coords}]
    for i, (lat, lon) in enumerate(office_coords):
        locations.append({
            "id": office_locations[i],
            "coords": Coordinates(lat=lat, lng=lon)
        })

        # Define search IDs from home to each office
    search_ids = {"home": [office_locations[i] for i in range(len(office_coords))]}

    print(f"Search IDs: {search_ids}")

    # Perform the matrix API call
    res = await sdk.time_filter_async(
        locations=locations,
        search_ids=search_ids,
        departure_time=datetime.now(),
        travel_time=3600,
        transportation=PublicTransport(),
        range=FullRange(enabled=True, max_results=3, width=600)
    )


    
    print(f"\nTravel times from {home_location} to offices:")
    for result in res:
        for location in result.locations:
            office_id = location.id
            times = [round(prop.travel_time / 60, 2) for prop in location.properties]
            #get the minimum travel time for each office
            time = min(times)
            # Print the office ID and travel times
            print(f"\t- {office_id}: {time} minutes")
    


asyncio.run(main())

