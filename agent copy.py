import requests
from google.adk.agents import Agent
from os import getenv
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

OPENCAGE_API_KEY = getenv("OPENCAGE_API_KEY")

def get_location(latitude: str, longitude: str) -> dict:
    """Returns the place name based on latitude and longitude.
    
    Args:
        latitude (str): The latitude coordinate
        longitude (str): The longitude coordinate
        
    Returns:
        dict: A dictionary containing the status and either a report or error message
    """
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
    model="gemini-2.0-flash",  # Using the latest stable model
    description="Agent that helps users identify a location based on coordinates.",
    instruction="""You are a helpful geolocation assistant that helps users find locations based on coordinates.

    When users provide coordinates:
    1. Extract the latitude and longitude from their message
    2. Use the get_location tool to find the place name
    3. Return the result in a friendly way

    When users don't provide coordinates:
    1. Ask them to provide both latitude and longitude
    2. Explain that you need both values to find the location
    3. Give an example of the format you expect (e.g., "latitude 40.7128, longitude -74.0060")

    Always be friendly and helpful in your responses.""",
    tools=[get_location],
)
