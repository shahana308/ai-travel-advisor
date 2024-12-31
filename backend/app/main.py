# FastAPI server setup
from fastapi import FastAPI, Query
from app.services.booking import fetch_accomodations
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Activity(BaseModel):
    day: int
    activity: str

class ItineraryResponse(BaseModel):
    destination: str
    duration: int
    itinerary: List[Activity]

class AccommodationRequest(BaseModel):
    location: str
    checkin_date: str
    checkout_date: str   

# Basic route
@app.get('/')
def read_root():
    return {"message": "Welcome to the AI Travel Advisor API!"}

# Itenerary route
@app.get("/itinerary/", response_model=ItineraryResponse)
def get_itenerary(
    destination: str = Query(..., description="The destination for the itinarary"), 
    duration: int = Query(..., ge=1, le=10, description="Number of days (1 - 10 days)")
):
    return {
        "destination": destination, 
        "duration": duration, 
        "itinerary": [
            {"day": 1, "activity": f"Explore the best spots in {destination}."},
            {"day": 2, "activity": f"Visit the famous landmarks in {destination}."},
            {"day": 3, "activity": f"Enjoy local food and culture in {destination}."},
        ][:duration]
    }

# booking.com accomodation route
@app.get("/accomodations/", response_model=AccommodationRequest)
def get_accomodations(
    location = Query(..., description = "The city of accomodations"), 
    checkin_date = Query(..., description = "check-in date (YYYY-MM-DD)"), 
    checkout_date = Query(..., description = "check-in date (YYYY-MM-DD)")
):
    data = fetch_accomodations(location, checkin_date, checkout_date)
    print(data)
    if data:
        return {"accomadation" : data.get("data", [])}
    return {"error": "Unable to fetch accommodations"}

