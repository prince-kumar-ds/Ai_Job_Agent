import requests
import os
from dotenv import load_dotenv

load_dotenv()

def fetch_jobs(role, location, date_posted, num_pages, remote_only, employment_type):

    url = "https://jsearch.p.rapidapi.com/search"

    query = f"{role} in {location}"

    querystring = {
        "query": query,
        "page": "1",
        "num_pages": str(num_pages),
        "country": "india",
        "date_posted": date_posted
    }

    # Optional filters
    if remote_only:
        querystring["work_from_home"] = "true"

    if employment_type:
        querystring["employment_types"] = ",".join(employment_type)

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPIDAPI_KEY"),
        "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()