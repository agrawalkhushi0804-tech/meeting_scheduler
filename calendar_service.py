import os
import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/calendar']


# =========================
# GET SERVICE
# =========================
def get_calendar_service():
    try:
        # 🔥 Load JSON from environment variable
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
# CREATE GOOGLE MEET
# =========================
def create_google_meet(service, name, date, time):
    try:
        if service is None:
            return "Error: Calendar service not available"

        start_time = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
        end_time = start_time + timedelta(hours=1)

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

        event = service.events().insert(
            calendarId='primary',
            body=event,
            conferenceDataVersion=1
        ).execute()

        raw_link = event['conferenceData']['entryPoints'][0]['uri']

        # 🔥 FIX REDIRECT ISSUE
        if "google.com/url?q=" in raw_link:
            import urllib.parse
            meet_link = urllib.parse.parse_qs(
                urllib.parse.urlparse(raw_link).query
            )['q'][0]
        else:
            meet_link = raw_link

        return meet_link.strip()

    except Exception as e:
        print("❌ ERROR CREATING MEETING:", e)
        return "Error creating meeting"
