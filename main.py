import streamlit as st
import requests
import json
import os

# 1️⃣ Clio OAuth Credentials - Set these from your Clio Developer App
CLIENT_ID = "YOUR_CLIENT_ID"
CLIENT_SECRET = "YOUR_CLIENT_SECRET"
REDIRECT_URI = "http://localhost:8501/callback"
CLIO_AUTH_URL = "https://app.clio.com/oauth/authorize"
CLIO_TOKEN_URL = "https://app.clio.com/oauth/token"
CLIO_API_BASE = "https://app.clio.com/api/v4"

# 2️⃣ Store user access tokens
if "access_token" not in st.session_state:
    st.session_state.access_token = None

# 3️⃣ OAuth Login Flow
def clio_login():
    """Redirects user to Clio login page"""
    auth_url = f"{CLIO_AUTH_URL}?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=read_write"
    st.markdown(f"[Login with Clio]({auth_url})")

def fetch_access_token(auth_code):
    """Exchange authorization code for an access token"""
    payload = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "code": auth_code,
        "redirect_uri": REDIRECT_URI
    }
    response = requests.post(CLIO_TOKEN_URL, data=payload)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("Failed to authenticate with Clio API.")
        return None

# 4️⃣ Fetch Clio Data
def fetch_clio_data(endpoint):
    """Fetch data from Clio API (Matters, Contacts, etc.)"""
    headers = {"Authorization": f"Bearer {st.session_state.access_token}"}
    response = requests.get(f"{CLIO_API_BASE}/{endpoint}", headers=headers)
    return response.json() if response.status_code == 200 else None

# 5️⃣ Webhook Handling (Register Webhooks)
def register_webhook():
    """Registers a webhook with Clio to listen for updates"""
    headers = {"Authorization": f"Bearer {st.session_state.access_token}", "Content-Type": "application/json"}
    payload = {
        "url": "https://your-webhook-endpoint.com",  # Change this to your actual webhook URL
        "event_type": "matter.create"  # You can change this to listen for other events (e.g., billing, contacts)
    }
    response = requests.post(f"{CLIO_API_BASE}/webhooks", headers=headers, json=payload)
    if response.status_code == 201:
        st.success("Webhook registered successfully!")
    else:
        st.error("Failed to register webhook.")

# 6️⃣ Streamlit UI
st.title("Clio OAuth + Webhooks in Streamlit")

# Handle OAuth Callback
if "code" in st.query_params:
    auth_code = st.query_params["code"]
    token_response = fetch_access_token(auth_code)
    if token_response:
        st.session_state.access_token = token_response["access_token"]
        st.success("✅ Successfully connected to Clio!")
        st.experimental_rerun()

# If user is logged in, show data options
if st.session_state.access_token:
    st.subheader("📊 Fetch Clio Data")

    option = st.selectbox("Select Data to Fetch", ["Matters", "Contacts", "Billing"])
    if st.button("Fetch Data"):
        endpoint = option.lower()  # Convert selection to API endpoint name
        data = fetch_clio_data(endpoint)
        if data:
            st.json(data)
        else:
            st.error("Failed to fetch data.")

    st.subheader("🔔 Webhooks")
    if st.button("Register Webhook"):
        register_webhook()

# If user is not logged in, show login button
else:
    st.warning("You must log in with Clio to access data.")
    clio_login()


