# FastAPI server setup
from fastapi import FastAPI, Query, HTTPException
from app.services.booking import fetch_accomodations
from pydantic import BaseModel
from pymongo import MongoClient
from typing import List, Optional
import os

app = FastAPI()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_name = "cluster0"
uri = f"mongodb+srv://{username}:{password}@{cluster_name}.6c59c.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)

db = client["travel_advisor"]
collection = db["cities"]

# Basic route
@app.get('/')
def read_root():
    return {"message": "Welcome to the AI Travel Advisor API!"}

@app.get("/cities")
async def get_all_cities():
    """Fetch all city names."""
    cities = collection.find({}, {"_id": 0, "title": 1})
    return list(cities)

@app.get("/cities/{city_name}")
async def get_city_data(city_name: str):
    """Fetch detailed data for a specific city."""
    city = collection.find_one({"title": city_name}, {"_id": 0})
    if city:
        return city
    return {"error": "City not found"}

@app.get("/search")
async def search_city(city_name: str, section: str = None):
    """Search within a specific section of a city."""
    city = collection.find_one({"title": city_name}, {"_id": 0})
    if city and section:
        return city["sections"].get(section, {"error": f"No data found for section '{section}'"})
    elif city:
        return city["sections"]
    return {"error": f"City '{city_name}' not found"}