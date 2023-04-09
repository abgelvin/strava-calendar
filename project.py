import requests
import os
from dotenv.main import dotenv_values
import urllib3
from datetime import datetime
from dateutil.relativedelta import relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError



urllib3.disable_warnings()
config = dotenv_values('dev.env')
CLIENT_ID = config['CLIENT_ID']
CLIENT_SECRET = config['CLIENT_SECRET']
REFRESH_TOKEN = config['REFRESH_TOKEN']
GOOGLE_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/calendar.events']



def main():
    access_token = get_access_token()
    events = get_activities(access_token)
    creds = connect_to_google()
    post_events(events, creds)


# Use refresh token to get return new access token for Strava
def get_access_token():
    auth_url = 'http://www.strava.com/oauth/token'
    payload = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'refresh_token': REFRESH_TOKEN,
        'grant_type': 'refresh_token',
        'f': 'json'
    }

    try:
        res = requests.post(auth_url, data=payload, verify=False)
        # print(f'strava result: {res.json()}')
        access_token = res.json()['access_token']
        return access_token
    except Exception as e:
        print(f'Error: {e}')


# Get list of last 20 activities using access token, return list of event objects
def get_activities(token):
    events = []
    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    header = {'Authorization': 'Bearer ' + token}
    param = {'page': 1, 'per_page': 20}
    try:
        mydata_set = requests.get(activities_url, headers=header, params=param).json()
        for i in range(20):
            event = {
                'id': mydata_set[i]['id'],
                'date': mydata_set[i]['start_date'],
                'time': mydata_set[i]['elapsed_time'],
                'name': mydata_set[i]['name'],
                'type': mydata_set[i]['type'],
                'distance': mydata_set[i]['distance'],
                'elevation': mydata_set[i]['total_elevation_gain']
            }
            events.append(event)
        # print(events)
        return events
    except Exception as e:
        print(f'Error: {e}')


# Get connection credentials to connect to google calendar API -- if token expired, delete token.json file to get new one
def connect_to_google():
    creds = None
    try:
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds
    except Exception:
        print('Token expired. Delete token.json file to get new token.')


 # Post Strava events to google calendar
def post_events(events, creds):
    calendarId = 'a9212d383316c207ef1a3f964280300349c3b1e9c0820e8698c8fdb871d2f6c7@group.calendar.google.com'
    service = build('calendar', 'v3', credentials=creds)

    for event in events:

        # Convert meters to miles and feet
        miles = round(event['distance'] / 1609.344)
        feet = round(event['elevation'] * 3.280839895)

        # Create end_time string from start time and elapsed time
        end_time = str(datetime.strptime(event['date'], '%Y-%m-%dT%H:%M:%SZ') + relativedelta(seconds=+event['time']))
        date, time  = end_time.split(' ')
        end_time = f'{date}T{time}Z'

        # Create event objects for calendar
        description = f"{event['type']}\ndistance: {miles} miles\nelevation: {feet} feet"
        event_to_add = {
            'id': event['id'],
            'summary': event['name'],
            'description': description,
            'start': {
                'dateTime': event['date']
            },
            'end': {
                'dateTime': end_time
            }
        }
        # print(f'event to add: {event_to_add}')
               
        send_event(service, calendarId, event['id'], event_to_add)
        

def send_event(service, calendar_id, event_id, body):
    try:
        results = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        print(f"Already uploaded: {results['summary']}")
    except HttpError:
        service.events().insert(calendarId=calendar_id, body=body).execute()
        print(f'Event added: {body}')






if __name__ == '__main__':
    main()

















# GETTING ACCESS AND REFRESH TOKEN FROM ONE-TIME USE CODE FOR STRAVA
# url = 'https://strava.com/oauth/token'
# payload = {
#     'client_id': client_id,
#     'client_secret': client_secret,
#     'code': '1b52f6cdac340f33577a54f5f00769db37277c43',
#     'grant_type': 'authorization_code'
# }

# res = requests.post(url, payload)
# refresh_token = res.json()['refresh_token']
# print(refresh_token)

# URL TO GET ONE-TIME USE CODE
# http://www.strava.com/oauth/authorize?client_id=104626&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=activity:read_all