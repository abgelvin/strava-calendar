# Strava Activities to Google Calendar
#### **Video Demo**:  https://www.youtube.com/watch?v=Riux6qk9Vrk
#### Technologies and frameworks: Python
#### **Description**
#### Purpose:
The purpose of this application is to retrieve recorded activities and various related statistics/characteristics from Strava using their API and post the activities to a Google Calendar using their API.  This is something that I was doing manually. 
#### Files:
* project.py: main progam file with the following functions:
    -Retrieve an access token from Strava
    -Use that access token retrieve the last 20 activities with the following fields: id, date, time, name, type, distance, and elevation
    -Retrieve credentials from Google Calendar
    -Post activities to Google Calendar with the following fields: id, summary, description (start dateTime, end dateTime)
* requirements.txt: contains dependencies
* test_project.py: contains unit tests for project.py functions