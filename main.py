print('start')
from datetime import date, datetime
import pytz
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build

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
# Fetch the next 10 events from the calendar
def fetch_events():
    # Define the current time in UTC timezone
    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time

    # Fetch events from Google Calendar
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=10,
        singleEvents=True,
        timeMin=now,
        orderBy='startTime').execute()

    return events_result.get('items', [])

# Print fetched events
def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start_utc = event['start'].get('dateTime', event['start'].get('date'))

        # Parse the datetime string to datetime object
        start_datetime = datetime.fromisoformat(start_utc)

        # Convert the datetime to UTC timezone
        start_utc = start_datetime.astimezone(pytz.utc).isoformat()

        # If the datetime has timezone info, convert it to local timezone
        if start_datetime.tzinfo is not None:
            start_local = start_datetime.astimezone().isoformat()
        else:
            start_local = start_datetime.isoformat()
        print(f"Event: Start time UTC: {start_utc}, Start time local: {start_local}")

######################################################################################################
today_date = date.today()
print(today_date)


# Function to check room availability

from googleapiclient.errors import HttpError

def check_availability(calendar_id, start_time, end_time):
    try:
        # Ensure 'Z' is appended to indicate UTC timezone
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=start_time + 'Z',
            timeMax=end_time + 'Z',
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])

        return len(events) == 0
    except HttpError as e:
        print(f'HttpError occurred: {e.content}')
        raise  # Raise the error to propagate it further

if __name__ == '__main__':
    calendar_id = 'dancemati@gmail.com'  # Specify your calendar ID here

    # Adjusted to UTC time by removing timezone offset
    iso_datetime_start = '2024-06-19T06:30:00'
    iso_datetime_end = '2024-06-19T09:50:00'

    try:
        # Fetch and print events
        events = fetch_events()
        print_events(events)

        available = check_availability(calendar_id, iso_datetime_start, iso_datetime_end)
        if available:
            print('The room is available.')
            print(f'{iso_datetime_start}')
        else:
            print('The room is not available.')
            print(f'{iso_datetime_start}')
    except HttpError as e:
        print(f'Error occurred: {e}')

"""
def check_availability(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time + 'Z',  # Assuming start_time and end_time are already strings
        timeMax=end_time + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return len(events) == 0


iso_datetime_start = '2024-06-19T09:30:00+03:00'  # This is already a string
iso_datetime_end = '2024-06-19T09:50:00+03:00'    # This is already a string
available = check_availability(calendar_id, iso_datetime_start, iso_datetime_end)

if available:
    st.success('The room is available.')
else:
    st.error('The room is not available.')
"""



"""
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


#start_datetime = datetime.strptime('2024-06-19T09:30:00+03:00', '%Y-%m-%dT%H:%M:%S').isoformat()
#end_datetime = datetime.strptime('2024-06-19T09:50:00+03:00', '%Y-%m-%dT%H:%M:%S').isoformat()

#iso_datetime_start = datetime.strptime('2024-06-19T09:30:00+03:00', '%Y-%m-%dT%H:%M:%S%z').isoformat()

#print(iso_datetime_start)  # Output: '2024-06-19T09:30:00+03:00'

#iso_datetime_end = datetime.strptime('2024-06-19T09:50:00+03:00', '%Y-%m-%dT%H:%M:%S%z').isoformat()

#print(iso_datetime_end)  # Output: '2024-06-19T09:30:00+03:00'

# Parse the datetime string to a datetime object
iso_datetime_start = datetime.fromisoformat('2024-06-19T09:30:00+03:00').isoformat()

print(iso_datetime_start)  # Output: '2024-06-19T09:30:00+03:00'
iso_datetime_end = datetime.fromisoformat('2024-06-19T09:50:00+03:00').isoformat()

print(iso_datetime_end)  # Output: '2024-06-19T09:30:00+03:00'
print(type(iso_datetime_start))

available = check_availability(calendar_id, iso_datetime_start, iso_datetime_end)

if available:
    st.success('The room is available.')
else:
    st.error('The room is not available.')
"""
"""
# Streamlit app
st.title('Room Availability Checker')

calendar_id = st.text_input('Enter Calendar ID', 'your_calendar_id@group.calendar.google.com')
date = st.date_input('Date', today_date)
start_time = st.time_input('Start Time', datetime.time(9, 0))
end_time = st.time_input('End Time', datetime.time(10, 0))

if st.button('Check Availability'):
    start_datetime = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    available = check_availability(calendar_id, start_datetime, end_datetime)

    if available:
        st.success('The room is available.')
    else:
        st.error('The room is not available.')
        
        """

