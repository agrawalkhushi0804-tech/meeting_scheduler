import os
import datetime
import uuid
import urllib.parse

from google.oauth2 import service_account
from googleapiclient.discovery import build


# 🔹 Load credentials from environment variable
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_CREDENTIALS_JSON")

SCOPES = ['https://www.googleapis.com/auth/calendar']

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build('calendar', 'v3', credentials=credentials)


def create_meeting(name, email, date, time):
    try:
        print("=== GOOGLE CALENDAR FUNCTION STARTED ===")

        # Convert date + time to datetime
        start_datetime = datetime.datetime.strptime(
            f"{date} {time}", "%Y-%m-%d %H:%M"
        )

        end_datetime = start_datetime + datetime.timedelta(hours=1)

        # Convert to ISO format
        start_iso = start_datetime.isoformat()
        end_iso = end_datetime.isoformat()

        # Unique request ID
        request_id = str(uuid.uuid4())

        event = {
            'summary': f'Meeting with {name}',
            'description': 'Scheduled via Meeting Scheduler App',
            'start': {
                'dateTime': start_iso,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_iso,
                'timeZone': 'Asia/Kolkata',
            },
            'attendees': [
                {'email': email},
            ],
            'conferenceData': {
                'createRequest': {
                    'requestId': request_id,
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

        print("Event created successfully")

        # 🔥 GET MEET LINK
        raw_link = event['conferenceData']['entryPoints'][0]['uri']

        print("Raw Meet Link:", raw_link)

        # 🔥 FIX REDIRECT ISSUE
        if "google.com/url?q=" in raw_link:
            meet_link = urllib.parse.parse_qs(
                urllib.parse.urlparse(raw_link).query
            )['q'][0]
        else:
            meet_link = raw_link

        meet_link = meet_link.strip()

        print("Final Meet Link:", meet_link)

        return meet_link

    except Exception as e:
        print("❌ ERROR IN CALENDAR:", e)
        return None
