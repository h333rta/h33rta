from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from requests_oauthlib import OAuth1Session
import os

router = APIRouter()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")
CALLBACK_URI = os.getenv("TWITTER_CALLBACK_URL")

@router.get("/api/auth")
async def twitter_login():
    oauth = OAuth1Session(API_KEY, client_secret=API_SECRET, callback_uri=CALLBACK_URI)
    fetch_response = oauth.fetch_request_token("https://api.twitter.com/oauth/request_token")
    resource_owner_key = fetch_response.get("oauth_token")
    resource_owner_secret = fetch_response.get("oauth_token_secret")
    auth_url = oauth.authorization_url("https://api.twitter.com/oauth/authorize")
    response = RedirectResponse(auth_url)
    response.set_cookie("oauth_token", resource_owner_key)
    response.set_cookie("oauth_token_secret", resource_owner_secret)
    return response
