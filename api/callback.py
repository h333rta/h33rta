from fastapi import Request, APIRouter
from fastapi.responses import HTMLResponse
from requests_oauthlib import OAuth1Session
import os

router = APIRouter()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")

@router.get("/api/callback", response_class=HTMLResponse)
async def twitter_callback(request: Request, oauth_token: str = "", oauth_verifier: str = ""):
    resource_owner_key = request.cookies.get("oauth_token")
    resource_owner_secret = request.cookies.get("oauth_token_secret")
    oauth = OAuth1Session(API_KEY,
                          client_secret=API_SECRET,
                          resource_owner_key=resource_owner_key,
                          resource_owner_secret=resource_owner_secret,
                          verifier=oauth_verifier)
    oauth_tokens = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
    access_token = oauth_tokens["oauth_token"]
    access_token_secret = oauth_tokens["oauth_token_secret"]

    return HTMLResponse(f"""<html><body>
    <h1>Confirm Profile Update</h1>
    <form action='/api/update' method='post'>
      <input type='hidden' name='token' value='{access_token}' />
      <input type='hidden' name='secret' value='{access_token_secret}' />
      <button type='submit'>Yes, I am a Puppet</button>
    </form>
    </body></html>""")
