import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

# ✅ Google Calendar scope
SCOPES = ['https://www.googleapis.com/auth/calendar']


# =========================
# GET CALENDAR SERVICE
# =========================
def get_calendar_service():
    try:
        # 🔐 Load credentials from environment variable
        credentials_info = json.loads(os.getenv("GOOGLE_CREDENTIALS"))

        credentials = service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=SCOPES
        )

        service = build('calendar', 'v3', credentials=credentials)
        return service

    except Exception as e:
        print("❌ ERROR LOADING GOOGLE CREDENTIALS:", e)
        return None


# =========================
# CREATE GOOGLE MEET LINK
# =========================
def create_google_meet(service, name, date, time):
    try:
        if service is None:
            return "Error: Calendar service not available"

        # Convert to datetime
        start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=1)

        # Event body
        event = {
            'summary': f'Meeting with {name}',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Kolkata',
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': f"{name}-{date}-{time}",
                    'conferenceSolutionKey': {
                        'type': 'hangoutsMeet'
                    }
                }
            }
        }

        # Create event
        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        # Extract Meet link
        meet_link = event['conferenceData']['entryPoints'][0]['uri']

        print("✅ Google Meet link created:", meet_link)

        return meet_link

    except Exception as e:
        print("❌ ERROR CREATING MEETING:", e)
        return "Error creating meeting"
