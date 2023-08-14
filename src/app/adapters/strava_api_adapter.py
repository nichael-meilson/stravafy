import requests

class StravaAPIAdapter:
    def get_strava_data():
        session = requests.session()
        resp = session.get("https://google.com")
        return resp.json()