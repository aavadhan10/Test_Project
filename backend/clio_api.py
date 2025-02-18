import requests
from config import CLIO_API_BASE

def fetch_clio_data(endpoint, access_token):
    """Fetches Clio data from API."""
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{CLIO_API_BASE}/{endpoint}", headers=headers)
    return response.json() if response.status_code == 200 else None
