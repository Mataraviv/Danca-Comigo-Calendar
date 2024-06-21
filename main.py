print('start')
from datetime import date, datetime, time
import pytz
import streamlit as st
from google.oauth2 import service_account
from googleapiclient.discovery import build
import json


# Define the scope for Google Calendar API
SCOPES = ['https://www.googleapis.com/auth/calendar']

# Retrieve the service account credentials from secrets
service_account_info = st.secrets["google_calendar"]["service_account"]

# Parse the JSON string from the TOML file
credentials_info = json.loads(service_account_info)

# Create credentials object using the parsed service account information
credentials = service_account.Credentials.from_service_account_info(credentials_info, scopes=SCOPES)

# Build the Google Calendar API service
service = build('calendar', 'v3', credentials=credentials)

calendar_id = 'dancemati@gmail.com'

today_date = date.today()
####################################################################################################

def fetch_events_now():
    now = datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(
        calendarId=calendar_id,
        maxResults=3,
        singleEvents=True,
        timeMin=now,
        orderBy='startTime').execute()
    return events_result.get('items', [])

def print_events(events):
    if not events:
        print('No upcoming events found.')
    for event in events:
        status = event['status']
        start_utc = event['start'].get('dateTime', event['start'].get('date'))
        end_utc = event['end'].get('dateTime', event['end'].get('date'))

        start_datetime = datetime.fromisoformat(start_utc)
        end_datetime = datetime.fromisoformat(end_utc)

        start_utc = start_datetime.astimezone(pytz.utc).isoformat()
        end_utc = end_datetime.astimezone(pytz.utc).isoformat()

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
        print(f"{status}Event {summary}: Start time UTC: {start_utc}, Start time local: {start_local}.\n End time UTC: {end_utc}, End time local: {end_local}.\n duration: {length}")


events_now = fetch_events_now()
#  print_events(events_now)

######################################################################################################


def fetch_events(calendar_id,start_time,end_time):
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=start_time +'Z',
        timeMax=end_time +'Z',
        singleEvents=True,
        orderBy='startTime').execute()
    return events_result.get('items', [])


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


def book_studio(calendar_id, start_time, end_time, summary, description, user_email):
    event = {
        'summary': summary,
        'description': f'My email {user_email}\n\n {description}' ,
        'start': {
            'dateTime': start_time + 'Z',
            'timeZone': 'UTC',
        },
        'end': {
            'dateTime': end_time + 'Z',
            'timeZone': 'UTC',
        },
        'guestsCanModify': False,
        'status': 'tentative'
    }
    event_result = service.events().insert(calendarId=calendar_id, body=event).execute()
    return event_result


######################################################################################################
print('streamlit')


if 'stage' not in st.session_state:
    st.session_state.stage = 0
if 'str_start_datetime' not in st.session_state:
    st.session_state.str_start_datetime = ''
if 'str_end_datetime' not in st.session_state:
    st.session_state.str_end_datetime = ''
if 'date' not in st.session_state:
    st.session_state.date = ''
if 'start_time' not in st.session_state:
    st.session_state.start_time = ''
if 'end_time' not in st.session_state:
    st.session_state.end_time = ''

def set_stage(stage):
    st.session_state.stage = stage


logo_path = './Current Logo.png'
pricing_path = './pricing.png'
link = "http://www.danca-comigo.com/"
A, B, C, D, E = st.columns(5)
with B:
    st.image(logo_path, width=400)

st.markdown("<h1 style='text-align: center; color: #c65dd4;'>Studio Availability Checker</h1>", unsafe_allow_html=True)

if st.session_state.stage == 0:
    with st.form(key='Check Availability'):
        st.session_state.date = st.date_input('Date', value=today_date, min_value=today_date, label_visibility='visible',format="DD/MM/YYYY").isoformat()
        col1, col2 = st.columns(2)
        with col1:
            start_time_input = st.time_input('Start Time',time(8, 0),step=900,label_visibility='visible')
            st.session_state.start_time = start_time_input.isoformat()
        with col2:
            end_time_input = st.time_input('End Time', time(9, 0),step=900,label_visibility='visible')
            st.session_state.end_time = end_time_input.isoformat()


        def valid_end_time_fun(start_time, end_time):
            if end_time <= start_time:
                st.error('End time must be later than start time.')
                return False
            else:
                st.success('Time range is valid.')
                # st.write(f'Start Time: {start_time} End Time: {end_time} On {date}')
                return True


        valid_end_time = valid_end_time_fun(st.session_state.start_time, st.session_state.end_time)
        submit_button_1 = st.form_submit_button(label='Check Availability')

    if valid_end_time and submit_button_1:
        start_datetime = datetime.combine(datetime.fromisoformat(st.session_state.date).date(), start_time_input)
        start_datetime_utc = start_datetime.astimezone(pytz.utc)
        st.session_state.str_start_datetime = start_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S')
        end_datetime = datetime.combine(datetime.fromisoformat(st.session_state.date).date(), end_time_input)
        end_datetime_utc = end_datetime.astimezone(pytz.utc)
        st.session_state.str_end_datetime = end_datetime_utc.strftime('%Y-%m-%dT%H:%M:%S')

        available = check_availability('dancemati@gmail.com', st.session_state.str_start_datetime, st.session_state.str_end_datetime)

        if available:
            st.success('The Studio is available. :dancer:')
            with st.expander(":heavy_dollar_sign: See Pricing :heavy_dollar_sign:"):
                st.image(pricing_path)
            st.button('Proceed to Booking', on_click=set_stage, args=(1,))

        else:
            st.error('Sorry. The Studio is not available.')
            st.title("The upcoming event in the Studio:")
            def fetch_events_time(start_datetime):
                events_result = service.events().list(
                    calendarId=calendar_id,
                    maxResults=3,
                    singleEvents=True,
                    timeMin=start_datetime + 'Z',
                    orderBy='startTime').execute()
                return events_result.get('items', [])
            def display_events(events):
                if not events:
                    st.write("No events found for this week.")
                else:
                    for event in events:
                        start_utc = event['start'].get('dateTime', event['start'].get('date'))
                        end_utc = event['end'].get('dateTime', event['end'].get('date'))
                        start_datetime = datetime.fromisoformat(start_utc)
                        end_datetime = datetime.fromisoformat(end_utc)
                        summary = event.get('summary', 'No title')
                        if start_datetime.tzinfo is not None:
                            start_local = start_datetime.astimezone().isoformat()
                            end_local = end_datetime.astimezone().isoformat()
                            g = end_datetime - start_datetime
                            length = g.total_seconds() / 3600
                            st.write(f"**{summary}**")
                            st.write(f'Date: {start_local[:10]}')
                            st.write(f"Start: {start_local[11:16]}")
                            st.write(f"End: {end_local[11:16]}")
                            st.write(f"Length: {length} hours")
                            st.write("---")
                        else:
                            length = "all day"
                            st.write(f"**{summary}**")
                            st.write(f'Date: {start_local[:10]}')
                            st.write(f"Length: {length}")
                            st.write("---")
            events = fetch_events_time(st.session_state.str_start_datetime)
            display_events(events)


if st.session_state.stage == 1:
    st.write(f'Your Booking is from {st.session_state.start_time} till {st.session_state.end_time} on {st.session_state.date}')
    with st.form(key='booking_form'):
        user_email = st.text_input('Enter your email', value="")
        summary = st.text_input('Event Summary', 'Enter your Booking Request')
        description = st.text_area('Event Description', 'Enter your Event Description')
        submit_button_2 = st.form_submit_button(label='Book Studio')

    if submit_button_2:
        event = book_studio(
            calendar_id, st.session_state.str_start_datetime, st.session_state.str_end_datetime,
            summary, description, user_email)
        if event:
            st.write(f'Your booking request has been sent! from {st.session_state.start_time} till {st.session_state.end_time} on {st.session_state.date}')
            st.write(f'Booking link: {event["htmlLink"]}')
            st.balloons()
        else:
            st.error('Failed to book the studio. Please check your inputs and try again.')
                

print('end')
        
