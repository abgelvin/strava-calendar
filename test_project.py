import unittest
from  unittest import mock, TestCase
import requests
import responses
import json
# import mock
from project import get_access_token, get_activities, connect_to_google, post_events



class TestProject(TestCase):

    # @classmethod
    # def setUpClass(cls):
    #     cls.base_URL = 'https://www.strava.com/api/v3/athlete/activities'
    #     with open('./fixtures/strava_test_auth_fixture.json', 'r') as auth_fixture_input:
    #         cls.mock_valid_auth_json = json.loads(auth_fixture_input.read())
    #     cls.app = get_activities(cls.mock_valid_auth_json['refresh_token'])

    #     with open('./fixtures/google_test_auth_fixture.json', 'r') as auth_fixture_input:
    #         cls.mock_valid_auth_json = json.loads(auth_fixture_input.read())
    #     with open('./fixtures/google_test_event_fixture.py', 'r') as auth_fixture_return:
    #         cls.mock_valid_return_py = auth_fixture_return.read()
    #     cls.app = post_events(cls.mock_valid_return_py, cls.mock_valid_auth_json)
    #     print(cls.mock_valid_return_py)

    # def test_get_activities_success(self):
    #    auth_endpoint = self.base_URL
    #    mock_strava_auth = responses.Response(
    #        method='POST',
    #        url=auth_endpoint,
    #        json=self.mock_valid_auth_json,
    #        status=200,
    #        content_type='application/json'
    #    )
    #    responses.add(mock_strava_auth)

    def test_post_events(self):
        with mock.patch('project.post_events') as mock_creds:

            events = [{'id': 8834079783, 'date': '2023-04-04T23:26:30Z', 'time': 2378, 'name': 'Zwift - Ocean Lava Cliffside Loop in Watopia', 'type': 'VirtualRide', 'distance': 19378.0, 'elevation': 156.0}]
            event_added = {'id': 8834079783, 'summary': 'Zwift - Ocean Lava Cliffside Loop in Watopia', 'description': 'VirtualRide\ndistance: 12 miles\nelevation: 512 feet', 'start': {'dateTime': '2023-04-04T23:26:30Z'}, 'end': {'dateTime': '2023-04-05T00:06:08Z'}}
            actual_result = post_events(events, mock_creds)  
            expected_result = Exception(print(f'Event added: {event_added}'))

            self.assertEqual(actual_result, expected_result)

        




if __name__ == '__main__':
    unittest.main()