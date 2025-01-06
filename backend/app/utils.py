import re
import spacy

nlp = spacy.load("en_core_web_sm")

SEASONS = {
    "spring": ["March", "April", "May"],
    "summer": ["June", "July", "August"],
    "autumn": ["September", "October", "November"],
    "fall": ["September", "October", "November"],  
    "winter": ["December", "January", "February"]
}

THEMES = ["party", "dinner", "date night", "beach", "landscape", "nature", "city"]

def extract_city_month_season_theme(query):
    """
    Extract city, month, season, and themes from a user query.
    query (str): The user's search query.
    """

    doc = nlp(query)
    city = None
    month = None
    season = None
    detected_themes = []

    for ent in doc.ents:
        if ent.label_ == "GPE":  
            city = ent.text
        elif ent.label_ == "DATE": 
            month_match = re.search(r"(January|February|March|April|May|June|July|August|September|October|November|December)", ent.text, re.IGNORECASE)
            if month_match:
                month = month_match.group(0)

            season_match = re.search(r"(spring|summer|autumn|fall|winter)", ent.text, re.IGNORECASE)
            if season_match:
                season = season_match.group(0).lower()

    # Check for themes/keywords
    for theme in THEMES:
        if theme in query.lower():
            detected_themes.append(theme)

    return {
        "city": city,
        "month": month,
        "season": season,
        "themes": detected_themes
    }         

query = "What can I do in Berlin during summer for a beach vacation in december?"

result = extract_city_month_season_theme(query)
print(result)