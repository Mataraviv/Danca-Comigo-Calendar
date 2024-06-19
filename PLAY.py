print('start')
from datetime import date, datetime, time
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
def fetch_events_now():
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=2,
        singleEvents=True,
        timeMin=now,
        orderBy='startTime').execute()

    return events_result.get('items', [])

def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        start_loc = event['start'].get('dateTime', event['start'].get('date'))
        end_loc = event['end'].get('dateTime', event['end'].get('date'))
        print(start_loc, type(start_loc),'start_loc')
        #print(end_loc, type(end_loc),'end_loc')

        # Parse the datetime string to datetime object
        start_datetime = datetime.fromisoformat(start_loc)
        end_datetime = datetime.fromisoformat(end_loc)
        print(start_datetime, type(start_datetime),'start_datetime')
        #print(end_datetime, type(end_datetime),'end_datetime')

        # Convert the datetime to UTC timezone
        start_utc = start_datetime.astimezone(pytz.utc).isoformat()
        end_utc = end_datetime.astimezone(pytz.utc).isoformat()
        print(start_utc, type(start_utc),'start_utc')
        #print(end_utc, type(end_utc),'end_utc')

        start_local_if = start_datetime.astimezone().isoformat()
        start_local_else = start_datetime.isoformat()
        print(start_local_if, type (start_local_if),'start_local_if')
        print(start_local_else, type (start_local_else),'start_local_else')
        #end_local = end_datetime.astimezone().isoformat()

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


events_now = fetch_events_now()
print_events(events_now)

######################################################################################################
today_date = date.today()
print(today_date)


def check_availability(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time +'Z',
        timeMax=end_time +'Z',
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    events = events_result.get('items', [])

    return len(events) == 0


start_time_local = '2024-06-19T09:30:00'
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
print('streamlit')

st.title('Studio Availability Checker')

date = st.date_input('Date', today_date)
start_time = st.time_input('Start Time', time(9, 0))
end_time = st.time_input('End Time', time(10, 0))


def valid_end_time_fun(start_time,end_time):
    if end_time < start_time:
        st.error('End time must be later than start time.')
        return False
    else:
        st.success('Time range is valid.')
        st.write(f'Start Time: {start_time}')
        st.write(f'End Time: {end_time}')
        return True


valid_end_time = valid_end_time_fun(start_time,end_time)


def fetch_events(calendar_id, start_time, end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time + 'Z',
        timeMax=end_time + 'Z',
        singleEvents=True,
        orderBy='startTime').execute()
    return events_result.get('items', [])


if valid_end_time and st.button('Check Availability'):
    start_datetime = datetime.combine(date, start_time)
    start_datetime_utc = start_datetime.astimezone(pytz.utc)
    str_start_datetime = start_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S')
    print(str_start_datetime)
    end_datetime = datetime.combine(date, end_time)
    end_datetime_utc = end_datetime.astimezone(pytz.utc)
    str_end_datetime = end_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S')
    print(str_end_datetime)

    events = fetch_events('dancemati@gmail.com', str_start_datetime, str_end_datetime)
    print_events(events)

    available = check_availability('dancemati@gmail.com', str_start_datetime, str_end_datetime)

    if available:
        st.success('The Studio is available.')
    else:
        st.error('Sorry. The Studio is not available.')

print('end')