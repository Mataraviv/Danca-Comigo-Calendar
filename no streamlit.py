
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
        print(f"{status}Event {summary}: Start time UTC: {start_utc}, Start time local: {start_local}.\n End time UTC: {end_utc}, End time local: {end_local}.\n duration: {length}")


events_now = fetch_events_now()
#  print_events(events_now)

######################################################################################################
"""
start_time_local = '2024-06-20T07:00:00'
local_time_s = datetime.strptime(start_time_local, '%Y-%m-%dT%H:%M:%S')
iso_datetime_start = local_time_s.astimezone(pytz.utc)
str_datetime_start = iso_datetime_start.strftime('%Y-%m-%dT%H:%M:%S')

end_time_local = '2024-06-20T08:00:00'
local_time_e = datetime.strptime(end_time_local, '%Y-%m-%dT%H:%M:%S')
iso_datetime_end = local_time_e.astimezone(pytz.utc)
str_datetime_end = iso_datetime_end.strftime('%Y-%m-%dT%H:%M:%S')

available = check_availability(calendar_id, str_datetime_start, str_datetime_end)
if available:
    print('The Studio is available.')

    summary = 'Event Summary'
    description = 'Event Description'
    event = book_studio(
        calendar_id, str_datetime_start, str_datetime_end,
        summary, description, user_email)
    if event:
        print(f'Your booking request has been sent! from {start_time_local} till {end_time_local}')
        print(f'Booking link: {event["htmlLink"]}')
    else:
        print('Failed to book the studio. Please check your inputs and try again.')

else:
    print('Sorry. The Studio is not available.')
"""