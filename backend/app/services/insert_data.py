import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_name = "cluster0"  

print('username', username)
print('password', password)

uri = f"mongodb+srv://{username}:{password}@cluster0.6c59c.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri)

db = client["travel_advisor"]
collection = db["cities"]

city_data = {
    "title": "Berlin",
    "sections": {
        "Do": [{"description": "Take a walking tour of Mitte."}],
        "Eat": [{"description": "Try currywurst at Curry 36."}],
        "See": [{"description": "Explore the Brandenburg Gate."}],
        "Buy": [{"description": "Shop at KaDeWe for souvenirs."}]
    }
}

collection.insert_one(city_data)
print("Data inserted successfully!")
