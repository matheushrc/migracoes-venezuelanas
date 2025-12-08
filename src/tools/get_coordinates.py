import os

import requests
from dotenv import load_dotenv

load_dotenv()


GEOCODING_API_KEY = os.environ["GEOCODING_API_KEY"]
if not GEOCODING_API_KEY:
    raise ValueError("GEOCODING_API_KEY environment variable not set.")


def get_coordinates(address: str):
    response = requests.get(
        "https://maps.googleapis.com/maps/api/geocode/json",
        params={
            "address": address,
            "key": GEOCODING_API_KEY,
        },
    )
    data = response.json()

    if data["status"] == "OK":
        location = data["results"][0]["geometry"]["location"]
        address = data["results"][0]["formatted_address"]
        return {
            "address": address,
            "latitude": location["lat"],
            "longitude": location["lng"],
        }
    else:
        raise Exception(f"Geocoding API error: {data['status']}")
