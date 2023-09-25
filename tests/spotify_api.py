from src.app.adapters.spotify_api_adapter import SpotifyAPIAdapter

if __name__ == "__main__":
    adapter = SpotifyAPIAdapter()
    landed_tracks = adapter.get_recently_played_tracks(start="2023-09-20", end="2023-09-24")
    modelled_tracks = adapter.model_tracks(landed_tracks)
    tracks = adapter.get_track_metadata(modelled_tracks)
    print(tracks)