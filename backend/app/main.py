# FastAPI server setup
from fastapi import FastAPI, Query
from services.booking import fetch_accomodations

app = FastAPI()

# Basic route
@app.get('/')
def read_root():
    return {"message": "Welcome to the AI Travel Advisor API!"}

# Itenerary route
@app.get("/itinerary/")
def get_itenerary(destination: str):
    return {
        "destination": destination, 
        "itinerary": [
            {"day": 1, "activity": f"Explore the best spots in {destination}."},
            {"day": 2, "activity": f"Visit the famous landmarks in {destination}."},
        ]
    }

@app.get("/accomodations")
def get_accomodations(location = Query(..., description = "The city of accomodations"), check_in = Query(..., description = "check-in date (YYYY-MM-DD)"), check_out = Query(..., description = "check-in date (YYYY-MM-DD)")):
    return
