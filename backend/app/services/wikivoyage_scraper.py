import requests
import re
from bs4 import BeautifulSoup

def fetch_page(city_name, base_url="https://en.wikivoyage.org/wiki/"):
    """
    Fetches the WikiVoyage page for the given city.
    """
    url = base_url + city_name.replace(" ", "_")
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch WikiVoyage page for {city_name}. HTTP Status: {response.status_code}")
    print(response.text[:1000])
    return response.text

def parse_page(html_content):
    def clean_text(text):
        text = re.sub(r"\d{1,3}\.\d{1,6}\.\d{1,6}", "", text)
        text = re.sub(r"\(updated .*?\)", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    
    def parse_section_content(section_text):
        """
        Splits the section content into smaller, structured data points.
        """
        entries = re.split(r"(?:\. |\n)", section_text)  # Split on sentence-ending punctuation or newlines
        structured_entries = []
        for entry in entries:
            entry = entry.strip()
            if len(entry) > 10:  # Avoid including very short or irrelevant entries
                structured_entries.append({"description": entry})
        return structured_entries
        
    soup = BeautifulSoup(html_content, "html.parser")

    title_tag = soup.find("title")
    title = title_tag.text.split(" – ")[0].strip() if title_tag else "Title not found"
    print(f"Title: {title}")

    content = {}

    main_content = soup.find("div", class_="mw-content-ltr mw-parser-output")
    if not main_content:
        raise Exception("Main content container not found.")

    sections_to_extract = ["Do", "Eat", "See", "Buy"]

    for section_title in sections_to_extract:
        section_heading = main_content.find("h2", id=section_title)
        if section_heading:
            section_parent = section_heading.find_parent("section")
            if section_parent:
                section_content = ""

                for tag in section_parent.find_all(["p", "ul", "ol"]):
                    section_content += tag.get_text(strip=True) + "\n"

                if section_content.strip():
                    content[section_title] = parse_section_content(clean_text(section_content.strip()))
            else:
                print(f"'{section_title}' section content not found")
        else:
            print(f"'{section_title}' section not found")

    return title, content


def save_to_file(city_name, title, content, output_dir="data"):
    """
    Saves the scraped data to a text file.
    """
    import os
    os.makedirs(output_dir, exist_ok=True)  # Ensure the output directory exists
    filename = os.path.join(output_dir, f"{city_name.replace(' ', '_')}_travel_guide.txt")
    with open(filename, "w", encoding="utf-8") as file:
        file.write(f"Title: {title}\n\n")
        for section, text in content.items():
            file.write(f"## {section}\n{text}\n\n")
    print(f"Data saved to {filename}")

def scrape_city(city_name):
    """
    Main function to scrape a city's WikiVoyage page.
    """
    print(f"Scraping WikiVoyage page for {city_name}...")
    html_content = fetch_page(city_name)
    title, content = parse_page(html_content)
    save_to_file(city_name, title, content)
    print("Scraping completed successfully.")
