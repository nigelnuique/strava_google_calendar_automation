from strava import get_recent_activities
from gcal import get_calendar_service, get_upcoming_events, delete_event, create_event
from datetime import datetime, timezone, timedelta
from gcal import calendar_id
import os
import sys

def validate_environment():
    """Validate that all required environment variables are set"""
    required_vars = [
        'STRAVA_CLIENT_ID',
        'STRAVA_CLIENT_SECRET',
        'STRAVA_REFRESH_TOKEN',
        'GOOGLE_CALENDAR_ID'
    ]

    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print("❌ Missing required environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\n📝 Please set these in your .env file or environment")
        sys.exit(1)

    # Check for Google credentials (either from env var or local file)
    google_credentials = os.getenv('GOOGLE_CREDENTIALS')
    credentials_file_exists = os.path.exists('credentials/token.json')
    
    if not google_credentials and not credentials_file_exists:
        print("❌ Google credentials not found!")
        print("   Neither GOOGLE_CREDENTIALS environment variable nor credentials/token.json file exists")
        print("\n🔧 To fix this:")
        print("   For local development: Run 'python authorize_google.py'")
        print("   For GitHub Actions: Set GOOGLE_CREDENTIALS secret in your repository")
        sys.exit(1)
    
    if google_credentials:
        print("✅ All required environment variables are set (using GOOGLE_CREDENTIALS)")
    else:
        print("✅ All required environment variables are set (using local credentials file)")


def is_match(event, activity):
    if "dateTime" not in event["start"] or "dateTime" not in event["end"]:
        return False

    event_start = datetime.fromisoformat(event["start"]["dateTime"]).astimezone(timezone.utc)
    event_end = datetime.fromisoformat(event["end"]["dateTime"]).astimezone(timezone.utc)

    activity_start = activity["start"].astimezone(timezone.utc)
    activity_end = activity_start + timedelta(minutes=activity["duration_min"])

    return (activity_start < event_end) and (event_start < activity_end)


def main():
    validate_environment()

    strava_activities = get_recent_activities()
    service = get_calendar_service()
    scheduled_events = get_upcoming_events(service, calendar_id)

    for activity in strava_activities:
        activity_start = activity["start"].astimezone(timezone.utc)

        # Filter events within ±1 day
        relevant_events = []
        for event in scheduled_events:
            if "dateTime" in event["start"]:
                event_time = datetime.fromisoformat(event["start"]["dateTime"]).astimezone(timezone.utc)
                if abs((event_time - activity_start).total_seconds()) < 86400:
                    relevant_events.append(event)

        for event in relevant_events:
            if is_match(event, activity):
                print(f"🗑️ Deleting matched event: {event['summary']}")
                if not delete_event(service, event['id'], calendar_id):
                    print(f"⚠️ Failed to delete event: {event['summary']}")

        print(f"➕ Creating event for: {activity['name']}")
        result = create_event(service, activity, calendar_id)
        if result:
            print(f"✅ Successfully created event for: {activity['name']}")
        else:
            print(f"❌ Failed to create event for: {activity['name']}")

if __name__ == "__main__":
    main()
