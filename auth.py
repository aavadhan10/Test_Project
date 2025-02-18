import requests
import os
from config import CLIENT_ID, CLIENT_SECRET, REDIRECT_URI

CLIO_AUTH_URL = "https://app.clio.com/oauth/authorize"
CLIO_TOKEN_URL = "https://app.clio.com/oauth/token"

def get_auth_url():
    """Returns Clio OAuth login URL."""
    return f"{CLIO_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read_write"

def exchange_code_for_token(auth_code):
    """Exchanges authorization code for access token."""
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(CLIO_TOKEN_URL, data=payload)
    return response.json() if response.status_code == 200 else None
