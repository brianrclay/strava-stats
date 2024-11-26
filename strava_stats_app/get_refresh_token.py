from flask import Flask, request
import requests
import webbrowser
from urllib.parse import urlencode

app = Flask(__name__)

# Replace these with your values from Strava API settings
CLIENT_ID = "141068"
CLIENT_SECRET = "43cf664d0dcf985830577f80ecc9d9197a2e283b"
REDIRECT_URI = "http://localhost:9000/callback"

@app.route("/")
def start_auth():
    return "Please check your terminal for the authorization URL."

@app.route("/callback")
def callback():
    code = request.args.get("code")
    
    response = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
    )
    
    data = response.json()
    refresh_token = data.get("refresh_token")
    
    print("\n=== Your Refresh Token ===")
    print(refresh_token)
    print("=========================\n")
    
    return f"Your refresh token is: {refresh_token}. You can close this window now."

if __name__ == "__main__":
    print("Starting authentication process...")
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": "activity:read_all",
        "approval_prompt": "force"
    }
    auth_url = f"https://www.strava.com/oauth/authorize?{urlencode(params)}"
    print("\n" + "="*80)
    print("Please copy and paste this URL into your browser to authorize the application:")
    print(auth_url)
    print("="*80 + "\n")
    app.run(port=9000)
