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
        if service is None:
            raise Exception("Service not initialized")

        print("=== CREATING GOOGLE MEET ===")

        # Convert datetime
        start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=1)

        # Event body
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
            },
            'conferenceData': {
                'createRequest': {
                    'requestId': str(uuid.uuid4()),  # 🔥 unique ID
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
            conferenceDataVersion=1  # 🔥 VERY IMPORTANT
        ).execute()

        print("✅ Event created")

        # 🔥 BEST WAY TO GET MEET LINK
        meet_link = event.get('hangoutLink')

        if not meet_link:
            raise Exception("Meet link not generated")

        print("✅ Meet Link:", meet_link)

        return meet_link

    except Exception as e:
        print("❌ ERROR CREATING MEETING:", e)
        return None

