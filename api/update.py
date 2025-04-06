from fastapi import Form, APIRouter
from fastapi.responses import HTMLResponse
from requests_oauthlib import OAuth1Session
import os

router = APIRouter()

API_KEY = os.getenv("TWITTER_API_KEY")
API_SECRET = os.getenv("TWITTER_API_SECRET")

AVATAR_URL = "https://pbs.twimg.com/media/Gn2ng4UW4AAFTvY?format=jpg&name=large"
BANNER_URL = "https://pbs.twimg.com/media/Gn2ng4WXYAAuTOI?format=jpg&name=large"
BIO = "I am a puppet weak for @HERTA_2DFD >_< CLICK -> https://h3rta.com/#send"

@router.post("/api/update", response_class=HTMLResponse)
async def update_profile(token: str = Form(...), secret: str = Form(...)):
    # You need to implement media upload and ID counter here
    return HTMLResponse("<h1>Profile would be updated here (placeholder)</h1>")
