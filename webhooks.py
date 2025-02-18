import requests
from config import CLIO_API_BASE

def register_webhook(access_token, event_type, webhook_url):
    """Registers a webhook to listen for Clio events."""
    headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
    payload = {"url": webhook_url, "event_type": event_type}
    response = requests.post(f"{CLIO_API_BASE}/webhooks", headers=headers, json=payload)
    return response.json() if response.status_code == 201 else None
