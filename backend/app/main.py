# FastAPI server setup
from fastapi import FastAPI, Query, HTTPException
from app.services.booking import fetch_accomodations
from app.services.wikivoyage_scraper import scrape_city, fetch_page, parse_page
from pydantic import BaseModel
from typing import List, Optional

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

class WikiVoyageResponse(BaseModel):
    title: str
    sections: dict

# Basic route
@app.get('/')
def read_root():
    return {"message": "Welcome to the AI Travel Advisor API!"}

# Itinerary route
@app.get("/itinerary/", response_model=ItineraryResponse)
def get_itinerary(
    destination: str = Query(..., description="The destination for the itinerary"), 
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

# Booking.com accommodation route
@app.get("/accomodations/", response_model=AccommodationRequest)
def get_accommodations(
    location: str = Query(..., description="The city for accommodations"), 
    checkin_date: str = Query(..., description="Check-in date (YYYY-MM-DD)"), 
    checkout_date: str = Query(..., description="Check-out date (YYYY-MM-DD)")
):
    data = fetch_accomodations(location, checkin_date, checkout_date)
    if data:
        return {"accomodations": data.get("data", [])}
    return {"error": "Unable to fetch accommodations"}

# WikiVoyage scraper route
@app.get("/wikivoyage/", response_model=WikiVoyageResponse)
def get_wikivoyage_guide(city: str = Query(..., description="City to scrape from WikiVoyage")):
    try:
        # Scrape the page content
        html_content = fetch_page(city)
        title, sections = parse_page(html_content)
        return {"title": title, "sections": sections}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching data for {city}: {str(e)}")
