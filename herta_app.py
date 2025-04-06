import os
import secrets
from flask import Flask, redirect, request, session, url_for, render_template_string
from authlib.integrations.flask_client import OAuth
import requests

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# WARNING: Do not hardcode keys in production
TWITTER_CLIENT_ID = "x8tJfDFWS0Oqxug5iTUxwvu5Z"
TWITTER_CLIENT_SECRET = "MHMVqewBdSwkqIRwzQnwjFusGBHwfRRj4ypwdPoLFox1JzsnAK"
CALLBACK_URL = "https://h33rta.vercel.app/auth/callback"

oauth = OAuth(app)
twitter = oauth.register(
    name='twitter',
    client_id=TWITTER_CLIENT_ID,
    client_secret=TWITTER_CLIENT_SECRET,
    request_token_url=None,
    access_token_url='https://api.twitter.com/2/oauth2/token',
    authorize_url='https://twitter.com/i/oauth2/authorize',
    api_base_url='https://api.twitter.com/2/',
    client_kwargs={
        'scope': 'tweet.read users.read tweet.write users.write offline.access',
        'token_endpoint_auth_method': 'client_secret_post'
    }
)

@app.route('/')
def homepage():
    return render_template_string('''
        <h1>Herta Puppet App</h1>
        <p>This app will update your profile ONLY with your full consent.</p>
        <a href="/login">Login with Twitter</a>
    ''')

@app.route('/login')
def login():
    redirect_uri = url_for('auth_callback', _external=True)
    return twitter.authorize_redirect(redirect_uri)

@app.route('/auth/callback')
def auth_callback():
    token = twitter.authorize_access_token()
    session['token'] = token
    return redirect(url_for('confirm'))

@app.route('/confirm')
def confirm():
    return render_template_string('''
        <h2>Confirm Profile Update</h2>
        <p>Do you agree to update your profile with the Herta Puppet theme?</p>
        <form action="/apply" method="post">
            <button type="submit">Yes, I'm a puppet >_<</button>
        </form>
    ''')

@app.route('/apply', methods=['POST'])
def apply():
    token = session.get('token')
    if not token:
        return redirect('/')

    headers = {
        'Authorization': f"Bearer {token['access_token']}",
        'Content-Type': 'application/json'
    }

    user_number = secrets.randbelow(9999)
    tag = f"#{user_number:04d}"

    payload = {
        "name": f"Herta Puppet {tag}",
        "description": "I am a puppet weak for @HERTA_2DFD >_< CLICK -> https://h3rta.com/#send",
        "profile_image_url": "https://pbs.twimg.com/media/Gn2ng4UW4AAFTvY?format=jpg&name=large",
        "profile_banner_url": "https://pbs.twimg.com/media/Gn2ng4WXYAAuTOI?format=jpg&name=large"
    }

    update_url = 'https://api.twitter.com/1.1/account/update_profile.json'
    requests.post(update_url, headers=headers, data={
        'name': payload['name'],
        'description': payload['description']
    })

    requests.post('https://api.twitter.com/1.1/account/update_profile_image.json',
                  headers=headers,
                  data={'image': payload['profile_image_url']})

    requests.post('https://api.twitter.com/1.1/account/update_profile_banner.json',
                  headers=headers,
                  data={'banner': payload['profile_banner_url']})

    return "<h3>Your profile has been updated! Long live Herta!</h3>"

if __name__ == '__main__':
    app.run(port=3000, debug=True)
