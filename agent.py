"""
MIT License

Copyright (c) 2024 Ngoga Alexis

This is an educational example demonstrating how to integrate Google ADK with Chainlit.
Feel free to use, modify, and share this code for learning purposes.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so.

See the LICENSE file for the full license text.
"""

import requests
from google.adk.agents import Agent
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENCAGE_API_KEY = getenv("OPENCAGE_API_KEY")

def get_location(latitude: str, longitude: str) -> dict:
    """Returns the place name based on latitude and longitude."""
    try:
        params = {
            'q': f"{latitude},{longitude}",
            'key': OPENCAGE_API_KEY,
            'language': 'en',
            'pretty': 1
        }
        response = requests.get("https://api.opencagedata.com/geocode/v1/json", params=params)
        response.raise_for_status()
        data = response.json()

        if data['results']:
            place_name = data['results'][0]['formatted']
            return {"status": "success", "report": f"The location is: {place_name}"}
        else:
            return {"status": "error", "error_message": "No results found for the given coordinates."}
    except Exception as e:
        return {"status": "error", "error_message": str(e)}

root_agent = Agent(
    name="geolocation_agent",
    model="gemini-1.5-flash",  # or gemini-2.0-pro if available
    description="Agent that helps users identify a location based on coordinates.",
    instruction=(
        "You are a helpful geolocation assistant. "
        "Ask users for latitude and longitude if not provided. "
        "Use get_location tool to return the place name."
    ),
    tools=[get_location],
)
