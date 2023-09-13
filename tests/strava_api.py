import json
from src.app.adapters.strava_api_adapter import StravaAPIAdapter

if __name__ == "__main__":
    adapter = StravaAPIAdapter()
    # activities = adapter.get_strava_athlete_activities()
    with open('/home/michael/stravafy/tests/strava_activities.json', 'r') as file:
        activities = json.load(file)
        adapter.get_strava_activity_timeseries(activities)

       