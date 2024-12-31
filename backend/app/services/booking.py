import os
import requests
from dotenv import load_dotenv

load_dotenv()

RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "booking-com.p.rapidapi.com"

def fetch_accomodations(location, checkin_date, checkout_date):
    dest_id = get_dest_id(location)
    if not dest_id:
        return {"error": f"Could not find destination ID for location: {location}"}

    url = f"https://{API_HOST}/v1/hotels/search"
    query = {
        "checkin_date": checkin_date,
        "checkout_date": checkout_date,
        "dest_type": "city",
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

    if response.status == 200:
        return response.json()
    else: 
        print(f"Error: {response.status_code}, {response.text}")
        return None

def get_dest_id(location: str):
    url = f"https://{API_HOST}/v1/hotels/locations"
    query = {
        "name": location,
        "locale": "en-us"
    }
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": API_HOST
    }

    response = requests.get(url, headers=headers, params=query)
    if response.status_code == 200:
        locations = response.json()
        if locations:
            return locations[0].get("dest_id")  
    print(f"Error fetching dest_id: {response.status_code}, {response.text}")
    return None
