print ('hell')

# calendar_access.py

from google.oauth2 import service_account
from googleapiclient.discovery import build

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'credentials.json'

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service for the Calendar API
service = build('calendar', 'v3', credentials=credentials)

# Specify the calendar ID (use 'primary' for the primary calendar of the account)
calendar_id = 'primary'  # or use your specific calendar ID

# Fetch the next 10 events from the calendar
events_result = service.events().list(
    calendarId=calendar_id, maxResults=10, singleEvents=True,
    orderBy='startTime').execute()

# Get the list of events
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(f"Event: {event['summary']}, Start time: {start}")
