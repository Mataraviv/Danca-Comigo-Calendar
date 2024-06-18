print('start')
from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime
import streamlit as st

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Path to the service account key file
SERVICE_ACCOUNT_FILE = 'cerdentials.json'

# Create credentials using the service account file
credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# Build the service for the Calendar API
service = build('calendar', 'v3', credentials=credentials)

# Specify the calendar ID (use 'primary' for the primary calendar of the account)
calendar_id = 'dancemati@gmail.com'  # or use your specific calendar ID

####################################################################################################

# Define the current time in UTC timezone
now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

# Fetch the next 10 events from the calendar
events_result = service.events().list(
    calendarId=calendar_id
    , maxResults=2
    , singleEvents=True,
    timeMin=now,
    orderBy='startTime').execute()

# Get the list of events
events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    print(f"Event: Start time: {start}")

######################################################################################################

# Function to check room availability
def check_availability(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time.isoformat() + 'Z',
        timeMax=end_time.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return len(events) == 0  # True if no events, room is available


# Streamlit app
st.title('Room Availability Checker')

calendar_id = st.text_input('Enter Calendar ID', 'your_calendar_id@group.calendar.google.com')
date = st.date_input('Date', datetime.date.today())
start_time = st.time_input('Start Time', datetime.time(9, 0))
end_time = st.time_input('End Time', datetime.time(10, 0))

if st.button('Check Availability'):
    start_datetime = datetime.datetime.combine(date, start_time)
    end_datetime = datetime.datetime.combine(date, end_time)

    available = check_availability(calendar_id, start_datetime, end_datetime)

    if available:
        st.success('The room is available.')
    else:
        st.error('The room is not available.')