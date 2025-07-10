from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv
load_dotenv()

calendar_id = os.getenv("GOOGLE_CALENDAR_ID", "").strip()

def get_calendar_service():
    try:
        # Try to get credentials from environment variable first (for GitHub Actions)
        google_credentials = os.getenv('GOOGLE_CREDENTIALS')
        if google_credentials:
            import json
            creds_data = json.loads(google_credentials)
            creds = Credentials.from_authorized_user_info(creds_data)
        else:
            # Fallback to file for local development
            creds = Credentials.from_authorized_user_file('credentials/token.json')
        
        # Check if credentials are expired and refresh if needed
        if not creds.valid:
            if creds.expired and creds.refresh_token:
                print("🔄 Refreshing expired Google credentials...")
                creds.refresh(Request())
                
                # Only save refreshed credentials to file if using local file method
                if not google_credentials:
                    with open('credentials/token.json', 'w') as token:
                        token.write(creds.to_json())
                    print("✅ Google credentials refreshed and saved to file")
                else:
                    print("✅ Google credentials refreshed (using environment variable)")
                    print("ℹ️  Note: Updated credentials are not persisted when using GOOGLE_CREDENTIALS env var")
            else:
                print("❌ Google credentials are invalid and cannot be refreshed")
                if google_credentials:
                    print("🔧 Please update your GOOGLE_CREDENTIALS secret with fresh credentials")
                else:
                    print("🔧 Please run authorize_google.py to re-authenticate")
                raise ValueError("Invalid Google credentials")
        
        return build('calendar', 'v3', credentials=creds)
    except FileNotFoundError:
        print("❌ Google credentials file not found at 'credentials/token.json'")
        print("🔧 Please run authorize_google.py to authenticate")
        raise
    except Exception as e:
        print(f"❌ Error creating Google Calendar service: {e}")
        raise

def get_upcoming_events(service, calendar_id):
    try:
        # Fix: Fetch past events to match Strava's 3-day lookback
        min_time = (datetime.utcnow() - timedelta(days=3)).isoformat() + 'Z'
        max_time = (datetime.utcnow() + timedelta(hours=6)).isoformat() + 'Z'  # Small buffer for activities just completed
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=min_time,
            timeMax=max_time,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        return events_result.get('items', [])
    except HttpError as e:
        print(f"❌ Google Calendar API error: {e}")
        return []
    except Exception as e:
        print(f"❌ Error fetching calendar events: {e}")
        return []

def delete_event(service, event_id, calendar_id):
    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        return True
    except HttpError as e:
        if e.resp.status == 410:
            # Event already deleted - this is fine, treat as success
            print(f"ℹ️ Event {event_id} was already deleted (multiple activities matched same event)")
            return True
        else:
            print(f"❌ Error deleting event {event_id}: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error deleting event {event_id}: {e}")
        return False

def create_event(service, activity, calendar_id):
    try:
        start_time = activity['start'].astimezone(timezone.utc)
        end_time = start_time + timedelta(minutes=activity["duration_min"])

        event = {
            'summary': f"{activity['type']} – {activity['name']}",
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC'
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC'
            },
        }
        result = service.events().insert(calendarId=calendar_id, body=event).execute()
        return result
    except HttpError as e:
        print(f"❌ Error creating event for {activity['name']}: {e}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error creating event for {activity['name']}: {e}")
        return None
