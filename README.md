# Strava Activities to Google Calendar
#### **Video Demo**:  https://www.youtube.com/watch?v=Riux6qk9Vrk
#### Technologies and frameworks: Python
#### **Description**
#### Purpose:
Strava is an application that you can use to keep track of athletic activities, such as running, biking, skiing, hiking, etc.  It will track your activity via GPS and at the end of the activity it will show you various statistics/characteristics of your activity, such as time, distance, elevation gain, temperature, calories burned, average watts, average speed, etc.  

Google calendar has an API that allows you to add events through code, rather than through their interface. I have manual been adding my strava activities to my google calendar so I can see what I have done in my calendar.

The purpose of this application is to retrieve recorded activities and selected related statistics/characteristics from Strava using their API and post the activities to a Google Calendar using their API.  This is something that I was doing manually. 
#### Files:
* project.py: main progam file with the following functions:
    -Retrieve an access token from Strava
    -Use that access token retrieve the last 20 activities with the following fields: id, date, time, name, type, distance, and elevation
    -Retrieve credentials from Google Calendar
    -Post activities to Google Calendar with the following fields: id, summary, description (start dateTime, end dateTime)
* requirements.txt: contains dependencies
* test_project.py: contains unit tests for project.py functions