from src.app.adapters.strava_api_adapter import StravaAPIAdapter

if __name__ == "__main__":
    adapter = StravaAPIAdapter()
    activities = adapter.get_strava_athlete_activities()
