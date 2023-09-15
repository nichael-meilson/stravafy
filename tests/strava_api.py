import json
from src.app.adapters.strava_api_adapter import StravaAPIAdapter

if __name__ == "__main__":
    adapter = StravaAPIAdapter()
    landed_activities = adapter.get_strava_activities("2023-09-01", "2023-09-15")
    modelled_activities = adapter.model_strava_activities(landed_activities)
    activities = adapter.get_strava_activity_streams(modelled_activities)
    print(activities)
    # with open('tests/strava_activities.json', 'r') as file:
    #     activities = json.load(file)
    #     activities = activities[0:5]
    #     adapter.get_strava_activity_streams(activities)

       