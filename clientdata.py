from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()

# init
api_key = os.getenv('API_KEY')
api_secret = os.getenv('API_SECRET')

client = Client(api_key, api_secret)