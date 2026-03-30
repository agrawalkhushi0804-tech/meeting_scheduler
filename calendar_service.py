from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime

# Permission scope
SCOPES = ['https://www.googleapis.com/auth/calendar']


def get_calendar_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        'credentials.json',
        SCOPES
    )
    creds = flow.run_local_server(port=0)
    service = build('calendar', 'v3', credentials=creds)
    return service


def create_google_meet(service, name, date, time):
    # Convert date & time into datetime object
    start_datetime = datetime.datetime.strptime(
        f"{date} {time}",
        "%Y-%m-%d %H:%M"
    )

    # Default meeting duration = 1 hour
    end_datetime = start_datetime + datetime.timedelta(hours=1)

    event = {
        'summary': f'Meeting with {name}',
        'start': {
            'dateTime': start_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_datetime.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'conferenceData': {
            'createRequest': {
                'requestId': 'meeting_scheduler_unique'
            }
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'email', 'minutes': 60},   # Email reminder 1 hour before
                {'method': 'popup', 'minutes': 30},   # Popup reminder 30 mins before
            ],
        }
    }

    # Insert event into Google Calendar
    event = service.events().insert(
        calendarId='primary',
        body=event,
        conferenceDataVersion=1
    ).execute()

    # Return Google Meet link
    return event.get("hangoutLink")