from fastapi.responses import HTMLResponse
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return HTMLResponse("""
    <html>
      <head><title>Herta Puppet</title></head>
      <body>
        <h1>Become a Herta Puppet</h1>
        <a href="/api/auth">Login with Twitter</a>
      </body>
    </html>
    """)
