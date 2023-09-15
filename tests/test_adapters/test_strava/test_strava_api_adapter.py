import pytest
from unittest.mock import Mock, patch
from src.app.adapters.strava_api_adapter import StravaAPIAdapter

# Mock the webbrowser module
webbrowser = Mock()

# Mock the requests module
requests = Mock()
requests.Session = Mock()

# Mock the StravaAuthHandler class
class MockStravaAuthHandler:
    def handle_request(self):
        pass

class TestStravaAPIAdapter:

    @pytest.fixture
    def strava_adapter(self):
        with patch('src.app.adapters.webbrowser', webbrowser):
            with patch('src.strava_api_adapter.StravaAuthHandler', MockStravaAuthHandler):
                return StravaAPIAdapter()

    def test_authorize_strava_api(self, strava_adapter):
        # Mock the response from Strava
        mock_response = Mock()
        mock_response.json.return_value = {'access_token': 'test_access_token'}
        requests.post.return_value = mock_response

        # Ensure the access token is obtained
        access_token = strava_adapter.authorize_strava_api()
        assert access_token == 'test_access_token'

    def test_get_strava_activities(self, strava_adapter):
        # Mock the response from Strava
        mock_response = Mock()
        mock_response.json.return_value = [{'id': 1, 'type': 'Run'}, {'id': 2, 'type': 'Ride'}]
        strava_adapter.session.get.return_value = mock_response

        # Ensure activities are retrieved
        activities = strava_adapter.get_strava_activities('2023-01-01', '2023-01-31')
        assert len(activities) == 2
        assert activities[0]['type'] == 'Run'
        assert activities[1]['type'] == 'Ride'

    def test_model_strava_activities(self, strava_adapter):
        # Mock input data
        input_activities = [{'id': 1, 'athlete': {'id': 101}, 'type': 'Run', 'timezone': 'UTC', 'start_date': '2023-01-01', 'suffer_score': 50},
                            {'id': 2, 'athlete': {'id': 102}, 'type': 'Ride', 'timezone': 'UTC', 'start_date': '2023-01-02', 'suffer_score': 60}]

        # Ensure activities are modeled correctly
        activities = strava_adapter.model_strava_activities(input_activities)
        assert len(activities) == 2
        assert activities[0].id == 1
        assert activities[0].athlete_id == 101
        assert activities[0].activity_type == 'Run'
        assert activities[0].timezone == 'UTC'
        assert activities[0].start_date == '2023-01-01'
        assert activities[0].suffer_score == 50
        assert activities[1].id == 2
        assert activities[1].athlete_id == 102
        assert activities[1].activity_type == 'Ride'
        assert activities[1].timezone == 'UTC'
        assert activities[1].start_date == '2023-01-02'
        assert activities[1].suffer_score == 60

    def test_get_strava_activity_streams(self, strava_adapter):
        # Mock input data
        input_activities = [{'id': 1}, {'id': 2}]
        mock_response = Mock()
        mock_response.json.return_value = [{'type': 'time', 'data': [1, 2, 3]}, {'type': 'heartrate', 'data': [120, 130, 140]}]
        strava_adapter.session.get.return_value = mock_response

        # Ensure activity streams are retrieved and set correctly
        activities = strava_adapter.get_strava_activity_streams(input_activities)
        assert len(activities) == 2
        assert activities[0].streams == [{'type': 'time', 'data': [1, 2, 3]}, {'type': 'heartrate', 'data': [120, 130, 140]}]
        assert activities[1].streams == [{'type': 'time', 'data': [1, 2, 3]}, {'type': 'heartrate', 'data': [120, 130, 140]}]

