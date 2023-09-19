from src.app.adapters.spotify_api_adapter import SpotifyAPIAdapter

if __name__ == "__main__":
    adapter = SpotifyAPIAdapter()
    landed_tracks = adapter.get_recently_played_tracks(start=1693526400, end=1694940153)
    modelled_tracks = adapter.model_tracks(landed_tracks)
    tracks = adapter.get_track_metadata(modelled_tracks)
    print(tracks)
    # landed_activities = adapter.get_strava_activities("2023-09-01", "2023-09-15")
    # modelled_activities = adapter.model_strava_activities(landed_activities)
    # activities = adapter.get_strava_activity_streams(modelled_activities)
    # print(activities)
       