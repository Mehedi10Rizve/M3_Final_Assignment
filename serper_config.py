from dotenv import load_dotenv
import os

# Load the .env_serperdevtool file
load_dotenv(dotenv_path=".env_serperdevtool")

# Retrieve the SERPER API Key
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not SERPER_API_KEY:
    raise ValueError("SERPER_API_KEY is missing. Please check your .env_serperdevtool file.")

# Function to return the API key
def get_serper_api_key():
    return SERPER_API_KEY