import os
import re
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MongoDB credentials from .env
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster_name = "cluster0"

# MongoDB connection
uri = f"mongodb+srv://{username}:{password}@{cluster_name}.6c59c.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["travel_advisor"]
collection = db["cities"]

# Function to fetch WikiVoyage page
def fetch_page(city_name, base_url="https://en.wikivoyage.org/wiki/"):
    url = base_url + city_name.replace(" ", "_")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch WikiVoyage page for {city_name}. HTTP Status: {response.status_code}")
    return response.text

# Function to parse page content
def parse_page(html_content):
    def clean_text(text):
        text = re.sub(r"\d{1,3}\.\d{1,6}\.\d{1,6}", "", text)
        text = re.sub(r"\(updated .*?\)", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def parse_section_content(section_text):
        entries = re.split(r"(?:\. |\n)", section_text)  # Split on sentence-ending punctuation or newlines
        structured_entries = []
        for entry in entries:
            entry = entry.strip()
            if len(entry) > 10:  # Avoid short/irrelevant entries
                structured_entries.append({"description": entry})
        return structured_entries

    soup = BeautifulSoup(html_content, "html.parser")
    title_tag = soup.find("title")
    title = title_tag.text.split(" – ")[0].strip() if title_tag else "Title not found"

    content = {}
    main_content = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if not main_content:
        raise Exception("Main content container not found.")

    sections_to_extract = ["Do", "Eat", "See", "Buy"]

    for section_title in sections_to_extract:
        section_heading = main_content.find("h2", string=section_title)
        if section_heading:
            section_parent = section_heading.find_next("section")
            section_content = ""

            if section_parent:
                for tag in section_parent.find_all(["p", "ul", "ol"]):
                    section_content += tag.get_text(strip=True) + "\n"

                if section_content.strip():
                    content[section_title] = parse_section_content(clean_text(section_content.strip()))
        else:
            print(f"'{section_title}' section not found")

    return title, content

# Function to scrape and insert data for a city
def scrape_and_insert_city(city_name):
    print(f"Scraping WikiVoyage page for {city_name}...")
    try:
        html_content = fetch_page(city_name)
        title, content = parse_page(html_content)
        city_data = {"title": title, "sections": content}
        collection.insert_one(city_data)
        print(f"Data for {city_name} inserted successfully!")
    except Exception as e:
        print(f"Error scraping {city_name}: {e}")

# List of cities to scrape
cities = ["Berlin", "Tokyo", "New York City", "Paris", "Dubai", "Sydney", "London", "Istanbul", "Bangkok", "Rome"]

# Scrape and insert data for each city
for city in cities:
    scrape_and_insert_city(city)

print("Data scraping and insertion completed!")
