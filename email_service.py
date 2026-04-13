from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime, timedelta

# ✅ SCOPES
SCOPES = ['https://www.googleapis.com/auth/calendar']

# ✅ GET SERVICE
def get_calendar_service():
    credentials = service_account.Credentials.from_service_account_file(
        'service_account.json',
        scopes=SCOPES
    )

    service = build('calendar', 'v3', credentials=credentials)
    return service


# ✅ CREATE GOOGLE MEET LINK
def create_google_meet(service, name, date, time):

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

    # ✅ Extract Google Meet link
    meet_link = event['conferenceData']['entryPoints'][0]['uri']

    return meet_link
