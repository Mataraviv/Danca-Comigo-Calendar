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
        end_utc = event['end'].get('dateTime', event['end'].get('date'))

        # Parse the datetime string to datetime object
        start_datetime = datetime.fromisoformat(start_utc)
        end_datetime = datetime.fromisoformat(end_utc)

        # Convert the datetime to UTC timezone
        start_utc = start_datetime.astimezone(pytz.utc).isoformat()
        end_utc = end_datetime.astimezone(pytz.utc).isoformat()

        # If the datetime has timezone info, convert it to local timezone
        if start_datetime.tzinfo is not None:
            start_local = start_datetime.astimezone().isoformat()
            end_local = end_datetime.astimezone().isoformat()
            g = end_datetime - start_datetime
            length = f'{g.total_seconds() / 3600} hours'
        else:
            start_local = start_datetime.isoformat()
            end_local = end_datetime.isoformat()
            length = "all day"

        summary = event['summary']
        print(
            f"Event {summary}: Start time UTC: {start_utc}, Start time local: {start_local}.\n End time UTC: {end_utc}, End time local: {end_local}.\n duration: {length}")


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

    start_time_local = '2024-06-19T09:30:00'
    local_time_s = datetime.strptime(start_time_local, '%Y-%m-%dT%H:%M:%S')
    iso_datetime_start = local_time_s.astimezone(pytz.utc)
    str_datetime_start = iso_datetime_start.strftime('%Y-%m-%dT%H:%M:%S')

    end_time_local = '2024-06-19T09:50:00'
    local_time_e = datetime.strptime(end_time_local, '%Y-%m-%dT%H:%M:%S')
    iso_datetime_end = local_time_e.astimezone(pytz.utc)
    str_datetime_end = iso_datetime_end.strftime('%Y-%m-%dT%H:%M:%S')

    try:
        # Fetch and print events
        events = fetch_events()
        print_events(events)

        available = check_availability(calendar_id, str_datetime_start, str_datetime_end)
        if available:
            print('The room is available.')
            print(f'{iso_datetime_start}')
            print(f'{str_datetime_start}')
            print(f'{start_time_local}')
        else:
            print('The room is not available.')
            print(f'{iso_datetime_start}')
            print(f'{str_datetime_start}')
            print(f'{start_time_local}')
    except HttpError as e:
        print(f'Error occurred: {e}')

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

print('start')
from datetime import date, datetime, time
import pytz
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
from google.auth import exceptions, jwt, impersonated_credentials

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

def fetch_events():
    now = datetime.utcnow().isoformat() + 'Z'


    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=10,
        singleEvents=True,
        timeMin=now,
        orderBy='startTime').execute()

    return events_result.get('items', [])

def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start_utc = event['start'].get('dateTime', event['start'].get('date'))
        end_utc = event['end'].get('dateTime', event['end'].get('date'))

        # Parse the datetime string to datetime object
        start_datetime = datetime.fromisoformat(start_utc)
        end_datetime = datetime.fromisoformat(end_utc)

        # Convert the datetime to UTC timezone
        start_utc = start_datetime.astimezone(pytz.utc).isoformat()
        end_utc = end_datetime.astimezone(pytz.utc).isoformat()

        # If the datetime has timezone info, convert it to local timezone
        if start_datetime.tzinfo is not None:
            start_local = start_datetime.astimezone().isoformat()
            end_local = end_datetime.astimezone().isoformat()
            g = end_datetime-start_datetime
            length = f'{g.total_seconds()/3600} hours'
        else:
            start_local = start_datetime.isoformat()
            end_local = end_datetime.isoformat()
            length = "all day"

        summary = event['summary']
        print(f"Event {summary}: Start time UTC: {start_utc}, Start time local: {start_local}.\n End time UTC: {end_utc}, End time local: {end_local}.\n duration: {length}")

events = fetch_events()
print_events(events)

######################################################################################################
today_date = date.today()
print(today_date)


def check_availability(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time + 'Z',
        timeMax=end_time + 'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return len(events) == 0

"""
date = input("choose date")
ttime = input("choose time")
dt = date+'T'+ttime+':00'
print(dt)
"""

start_time_local = '2024-06-19T09:30:00'  # dt
local_time_s = datetime.strptime(start_time_local, '%Y-%m-%dT%H:%M:%S')
iso_datetime_start = local_time_s.astimezone(pytz.utc)
str_datetime_start = iso_datetime_start.strftime('%Y-%m-%dT%H:%M:%S')

end_time_local = '2024-06-19T09:50:00'
local_time_e = datetime.strptime(end_time_local, '%Y-%m-%dT%H:%M:%S')
iso_datetime_end = local_time_e.astimezone(pytz.utc)
str_datetime_end = iso_datetime_end.strftime('%Y-%m-%dT%H:%M:%S')


available = check_availability(calendar_id, str_datetime_start, str_datetime_end)
if available:
    print('The Studio is available.')
    print(f'{iso_datetime_start}')
    print(f'{str_datetime_start}')
    print(f'{start_time_local}')
else:
    print('Sorry. The Studio is not available.')
    print(f'{iso_datetime_start}')
    print(f'{str_datetime_start}')
    print(f'{start_time_local}')


######################################################################################################


st.title('Studio Availability Checker')

calendar_id = st.text_input(calendar_id)
date = st.date_input('Date', today_date)
start_time = st.time_input('Start Time', time(9, 0))
end_time = st.time_input('End Time', time(10, 0))

if st.button('Check Availability'):
    start_datetime = datetime.combine(date, start_time)
    end_datetime = datetime.combine(date, end_time)

    available = check_availability(calendar_id, start_datetime, end_datetime)

    if available:
        st.success('The room is available.')
    else:
        st.error('The room is not available.')


print('end')