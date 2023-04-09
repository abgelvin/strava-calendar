import unittest
from unittest.mock import patch, Mock
from project import get_access_token, post_events



class TestProject(unittest.TestCase):

    def test_get_access_token(self):
        fake_access_token = 'abc'
        return_dict = {"access_token": fake_access_token}
        
        mock = Mock()
        mock.return_value.json.return_value = return_dict
        with patch('project.requests.post', mock) as _:
            response = get_access_token()

        assert response == fake_access_token
    
    
    def test_get_activities(self):
        mock = Mock()
        with patch('project.requests.get', mock) as _:
            assert mock.assert_called_once


    def test_post_events(self):
        events = [{'id': 8822112517, 'date': '2023-04-02T20:56:21Z', 'time': 3583, 'name': 'Toward Ouray', 'type': 'Ride', 'distance': 20335.7, 'elevation': 186.0}]
        mock_build = Mock()
        mock_send = Mock()

        with patch('project.build', mock_build) as _, patch('project.send_event', mock_send) as _:
            response = post_events(events, None)
            print(f'response: {response}')
            assert mock_send.call_count == len(events)










if __name__ == '__main__':
    unittest.main()