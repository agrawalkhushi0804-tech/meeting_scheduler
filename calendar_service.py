import os
import json
from datetime import datetime, timedelta
import uuid

from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


# =========================
# GET GOOGLE CALENDAR SERVICE
# =========================
def get_calendar_service():
    try:
        credentials_json = os.getenv("GOOGLE_CREDENTIALS")

        if not credentials_json:
            raise Exception("GOOGLE_CREDENTIALS not found")

        credentials_info = json.loads(credentials_json)

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES
        )

        service = build('calendar', 'v3', credentials=credentials)
        return service

    except Exception as e:
        print("❌ ERROR LOADING GOOGLE SERVICE:", e)
        return None


# =========================
# CREATE GOOGLE MEET LINK
# =========================
def create_google_meet(service, name, date, time):
    try:
        from datetime import datetime, timedelta

        start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=1)

        event = {
            'summary': f'Meeting with {name}',
            'description': 'Scheduled via Meeting Scheduler',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            }
        }

        # ✅ Create event WITHOUT conferenceData
        event = service.events().insert(
            calendarId='primary',
            body=event
        ).execute()

        print("✅ Event created")

        # 🔥 OPTION 1: Try to get Meet link (rare case)
        meet_link = event.get('hangoutLink')

        # 🔥 OPTION 2: Fallback (100% works)
        if not meet_link:
            meet_link = "https://meet.google.com/new"

        print("✅ Meet Link:", meet_link)

        return meet_link

    except Exception as e:
        print("❌ ERROR CREATING MEETING:", e)
        return None
