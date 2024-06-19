print('start')
from datetime import date, datetime, time, timedelta
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
calendar_id = 'dancemati@gmail.com'
owner_email = calendar_id

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


events_now = fetch_events_now()
print_events(events_now)

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

######################################################################################################
print('streamlit')
logo_path = 'C:/Users/matar.aviv/Desktop/DS17/Danca-Comigo-Calendar/Current Logo.png'
link = "http://www.danca-comigo.com/"
cola, colb = st.columns(2)
with cola:
    st.image(logo_path, use_column_width=True)
with colb:
    st.logo(logo_path,link="http://www.danca-comigo.com/")


st.title(':violet[_Studio Availability Checker_]')

date = st.date_input('Date', value=today_date, min_value=today_date, label_visibility='visible',format="DD/MM/YYYY")
col1, col2 = st.columns(2)
with col1:
    start_time = st.time_input('Start Time',time(8, 0),step=900,label_visibility='visible')
with col2:
    end_time = st.time_input('End Time', time(9, 0),step=900,label_visibility='visible')


def valid_end_time_fun(start_time, end_time):
    if end_time < start_time:
        st.error('End time must be later than start time.')
        return False
    else:
        st.success('Time range is valid.')
        #st.write(f'Start Time: {start_time} End Time: {end_time} On {date}')
        return True


valid_end_time = valid_end_time_fun(start_time, end_time)

def fetch_events(calendar_id,start_time,end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time +'Z',
        timeMax=end_time +'Z',
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

        user_email = st.text_input('Enter your email', value="")
        summary = st.text_input('Event Summary', 'Booking Request')
        description = st.text_area('Event Description', 'Please approve this booking request for the studio.')


        def book_studio(calendar_id, start_time, end_time, summary, description, user_email, owner_email):
            event = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time + 'Z',
                    'timeZone': 'UTC',
                },
                'end': {
                    'dateTime': end_time + 'Z',
                    'timeZone': 'UTC',
                },
                'attendees': [
                    {'email': user_email},
                    {'email': owner_email, 'responseStatus': 'needsAction'}  # Owner invited for approval
                ],
                'guestsCanModify': False,
                'status': 'tentative'  # Tentative until the owner approves
            }

            event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
            return event_result

        if st.button('book_studio'):
            event = book_studio(
                calendar_id, str_start_datetime, str_end_datetime,
                summary, description, user_email, owner_email)
            st.success('The Studio is available and your booking request has been sent!')
            st.write(f'Booking link: {event["htmlLink"]}')
            st.balloons()

    else:
        st.error('Sorry. The Studio is not available.')

        """
        # Get the current week start and end dates
        def get_week_dates():
            today = date.today()
            start_of_week = today - timedelta(days=today.weekday())
            end_of_week = start_of_week + timedelta(days=6)
            return start_of_week, end_of_week

        # Fetch events for the current week
        def fetch_week_events(calendar_id):
            start_of_week, end_of_week = get_week_dates()
            time_min = datetime.combine(start_of_week, datetime.min.time()).isoformat() + 'Z'
            time_max = datetime.combine(end_of_week, datetime.max.time()).isoformat() + 'Z'

            events_result = service.events().list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
                orderBy='startTime'
            ).execute()
            return events_result.get('items', [])

        # Display events in Streamlit
        def display_events(events):
            if not events:
                st.write("No events found for this week.")
            else:
                for event in events:
                    start_time = event['start'].get('dateTime', event['start'].get('date'))
                    end_time = event['end'].get('dateTime', event['end'].get('date'))
                    summary = event.get('summary', 'No title')
                    st.write(f"**{summary}**")
                    st.write(f"Start: {start_time}")
                    st.write(f"End: {end_time}")
                    st.write("---")


        # Streamlit app
        st.title("Studio Calendar for the Current Week")

        events = fetch_week_events(calendar_id)
        display_events(events)
        """


print('end')