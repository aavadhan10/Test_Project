import os
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("CLIO_CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIO_CLIENT_SECRET")
REDIRECT_URI = os.getenv("CLIO_REDIRECT_URI")
CLIO_API_BASE = "https://app.clio.com/api/v4"
CLIO_TOKEN_URL = "https://app.clio.com/oauth/token"
