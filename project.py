import requests
import os
from dotenv.main import dotenv_values
import urllib3
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
SCOPES = ['https://www.googleapis.com/auth/calendar']

access_token = None
events = []

def main():
    while True:
        try:            
            events = get_activities(access_token)
            break
        except Exception as e:
            print(e)
            access_token = get_access_token()

    try: 
        creds = connect_to_google()
    except Exception as e:
        print(e)
    
    post_events(events, creds)
            

# Use refresh token to get return new access token
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
        access_token = res.json()['access_token']
        return access_token
    except Exception as e:
        print(f'Error: {e}')


# Get list of last 20 activities using access token, return list of event objects
def get_activities(token):
    activities_url = 'https://www.strava.com/api/v3/athlete/activities'
    header = {'Authorization': 'Bearer ' + token}
    param = {'page': 1, 'per_page': 20}
    try:
        mydata_set = requests.get(activities_url, headers=header, params=param).json()
        for i in range(20):
            event = {
                'id': mydata_set[i]['id'],
                'date': mydata_set[i]['start_date'],
                'name': mydata_set[i]['name'],
                'type': mydata_set[i]['type'],
                'distance': mydata_set[i]['distance'],
                'elevation': mydata_set[i]['total_elevation_gain']
            }
            events.append(event)
        return events
    except Exception as e:
        print(f'Error: {e}')


# Get connection credentials to connect to google calendar API
def connect_to_google():
    creds = None
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


 # Post Strava events to google calendar
def post_events(events, creds):
    calendarId = 'a9212d383316c207ef1a3f964280300349c3b1e9c0820e8698c8fdb871d2f6c7@group.calendar.google.com'
    service = build('calendar', 'v3', credentials=creds)

    for event in events:

        # Convert meters to miles and feet
        miles = round(event['distance'] / 1609.344)
        feet = round(event['elevation'] * 3.280839895)

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
                'dateTime': event['date']
            }
        }
        
        # Check to see if event with id already exists, if not, add that event to the calendar
        try:
            results = service.events().get(calendarId=calendarId, eventId=event['id']).execute()
            print(results['summary'])
        except HttpError:
            event = service.events().insert(calendarId=calendarId, body=event_to_add).execute()
            print(f'event added: {event_to_add}')

            


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