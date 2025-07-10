from strava import get_recent_activities
from gcal import get_calendar_service, get_upcoming_events, calendar_id
from datetime import datetime, timedelta, timezone

def debug_overlap(event, activity):
    event_start = datetime.fromisoformat(event["start"]["dateTime"]).astimezone(timezone.utc)
    event_end = datetime.fromisoformat(event["end"]["dateTime"]).astimezone(timezone.utc)

    activity_start = activity["start"].astimezone(timezone.utc)
    activity_end = activity_start + timedelta(minutes=activity["duration_min"])

    overlap = (activity_start < event_end) and (event_start < activity_end)

    return {
        "event_summary": event.get("summary", ""),
        "event_start": event_start,
        "event_end": event_end,
        "activity_name": activity["name"],
        "activity_type": activity["type"],
        "activity_start": activity_start,
        "activity_end": activity_end,
        "overlaps": overlap
    }

def main():
    service = get_calendar_service()
    events = get_upcoming_events(service, calendar_id)
    activities = get_recent_activities()

    print(f"\n📅 Total events: {len(events)}")
    print(f"🏃‍♂️ Total activities: {len(activities)}\n")

    for activity in activities:
        print(f"\n=== Checking activity: {activity['name']} ===")
        for event in events:
            if "dateTime" not in event.get("start", {}):
                continue

            result = debug_overlap(event, activity)

            print(f"🗓️ Event: {result['event_summary']}")
            print(f"   📆 {result['event_start']} to {result['event_end']}")
            print(f"   🚴 {result['activity_start']} to {result['activity_end']}")
            print(f"   🔍 Overlap: {result['overlaps']}")
            print("-" * 40)

if __name__ == "__main__":
    main()
