import requests
from datetime import datetime, timedelta
from datetime import timezone
import os
from dotenv import load_dotenv

load_dotenv()

STRAVA_CLIENT_ID = os.getenv("STRAVA_CLIENT_ID")
STRAVA_CLIENT_SECRET = os.getenv("STRAVA_CLIENT_SECRET")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")

def get_access_token():
    try:
        response = requests.post("https://www.strava.com/oauth/token", data={
            "client_id": STRAVA_CLIENT_ID,
            "client_secret": STRAVA_CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": STRAVA_REFRESH_TOKEN
        })
        response.raise_for_status()  # Raise exception for bad status codes
        data = response.json()
        
        if "access_token" not in data:
            raise ValueError("No access token in response")
        
        return data["access_token"]
    except requests.exceptions.RequestException as e:
        print(f"❌ Error getting Strava access token: Network request failed")
        print(f"💡 Check your internet connection and API credentials")
        raise
    except (KeyError, ValueError) as e:
        print(f"❌ Error parsing Strava token response: Invalid API response")
        print(f"💡 Check if your Strava credentials are correct")
        raise

def get_recent_activities():
    try:
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}
        since = int((datetime.utcnow() - timedelta(days=3)).timestamp())

        response = requests.get(
            f"https://www.strava.com/api/v3/athlete/activities?after={since}",
            headers=headers
        )
        response.raise_for_status()
        
        activities = response.json()
        if not isinstance(activities, list):
            print("❌ Unexpected response format from Strava API")
            return []
        
        parsed = []
        for a in activities:
            try:
                parsed.append({
                    "id": a["id"],
                    "name": a["name"],
                    "type": a["type"],
                    "start": datetime.strptime(a["start_date"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc),
                    "duration_min": int(a["elapsed_time"] / 60)
                })
            except (KeyError, ValueError) as e:
                print(f"⚠️ Skipping malformed activity: {e}")
                continue
        
        return parsed
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching Strava activities: {e}")
        return []
    except Exception as e:
        print(f"❌ Unexpected error in get_recent_activities: {e}")
        return []
