import os
from dotenv import load_dotenv
import requests

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "booking-com15.p.rapidapi.com"

def fetch_accomodations(location, checkin_date, checkout_date):
    dest_id = get_dest_id(location)
    if not dest_id:
        return {"error": f"Could not find destination ID for location: {location}"}

    url = f"https://{API_HOST}/api/v1/hotels/searchHotels"
    query = {
        "arrival_date": checkin_date,
        "departure_date": checkout_date,
        "search_type": "city",
        "locale": "en-us",
        "dest_id": dest_id, 
        "units": "metric",
        "room_number": "1",
        "adults_number": "2",
        "order_by": "popularity",
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": API_HOST,
    }

    response = requests.get(url, headers = headers, params = query)

    if response.status_code == 200:
        return response.json()
    else: 
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_dest_id(location: str):
    url = f"https://{API_HOST}/api/v1/hotels/searchDestination"
    query = {
        "query": location,
        "locale": "en-us"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(url, headers=headers, params=query)
    print(f"Location API Response: {response.status_code}, {response.text}")  

    if response.status_code == 200:
        response_data = response.json()
        locations = response_data.get("data", [])
        if locations:
            return locations[0].get("dest_id") 

    print(f"Error fetching dest_id: {response.status_code}, {response.text}")
    return None
