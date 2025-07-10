import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Get credentials from environment variables or prompt user
client_id = os.getenv("STRAVA_CLIENT_ID")
client_secret = os.getenv("STRAVA_CLIENT_SECRET")
authorization_code = os.getenv("STRAVA_AUTHORIZATION_CODE")

if not client_id:
    client_id = input("Enter your Strava Client ID: ")
if not client_secret:
    client_secret = input("Enter your Strava Client Secret: ")
if not authorization_code:
    authorization_code = input("Enter your Strava Authorization Code: ")

url = "https://www.strava.com/oauth/token"

payload = {
    'client_id': client_id,
    'client_secret': client_secret,
    'code': authorization_code,
    'grant_type': 'authorization_code'
}

try:
    response = requests.post(url, data=payload)
    response.raise_for_status()
    
    if response.status_code == 200:
        data = response.json()
        print("✅ Access Token:", data["access_token"][:20] + "..." if len(data["access_token"]) > 20 else data["access_token"])
        print("🔁 Refresh Token:", data["refresh_token"][:20] + "..." if len(data["refresh_token"]) > 20 else data["refresh_token"])
        print("⏳ Expires At:", data["expires_at"])
        print("\n📝 Add these to your .env file:")
        print(f"STRAVA_CLIENT_ID={client_id}")
        print(f"STRAVA_CLIENT_SECRET={client_secret[:10]}...")
        print(f"STRAVA_REFRESH_TOKEN={data['refresh_token'][:20]}...")
        print("\n⚠️  Keep these tokens secure and never commit them to version control!")
    else:
        print("❌ Error:", response.status_code, response.text)
        
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
except KeyError as e:
    print(f"❌ Missing field in response: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")
