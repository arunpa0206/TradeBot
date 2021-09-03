from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()


# Initialize the binance API key and secret key:
api_key = os.getenv('TEST_API_KEY') #API_KEY
api_secret = os.getenv('TEST_SECRET_KEY') #API_SECRET


# Initializing the client object, which will be used for all API-calls in all the modules.
client = Client(api_key, api_secret)


# A DOT-ENV FILE IS NEEDED TO BE PRESENT FIRST WITH THE API KEY AND SECRET KEY IN THIS DIRECTORY!