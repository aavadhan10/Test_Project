from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

from auth import get_auth_url, exchange_code_for_token
from clio_api import fetch_clio_data
from webhooks import register_webhook

app = FastAPI()

# Allow CORS for frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/login")
async def login():
    """Redirect users to Clio OAuth login."""
    return {"login_url": get_auth_url()}

@app.get("/callback")
async def callback(code: str):
    """Handles OAuth callback from Clio."""
    token_data = exchange_code_for_token(code)
    if token_data:
        return {"access_token": token_data["access_token"]}
    raise HTTPException(status_code=400, detail="Failed to authenticate")

@app.get("/clio-data/{endpoint}")
async def get_clio_data(endpoint: str, token: str):
    """Fetch Clio data dynamically (Matters, Contacts, etc.)"""
    return fetch_clio_data(endpoint, token)

@app.post("/register-webhook")
async def webhook(token: str, event_type: str):
    """Register webhook to listen for Clio updates."""
    return register_webhook(token, event_type)
