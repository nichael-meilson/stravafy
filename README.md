# stravafy

# Run in Docker:
1. `cd` into `stravafy/src`
2. `docker-compose up --build`
3. Check the API Swagger docs: `localhost:8000/docs`


# Authorize Strava or Spotify
1. In a web browser URL: `localhost:8000/api/auth/strava` or `localhost:8000/api/auth/spotify`
2. Token is stored on the server; you can now use the other endpoints



### ISSUES
* Spotify will only let you get the last 50 recently played tracks, no matter the time inputs you give
* Wildly annoying

### TODO
* Run a DB container
* Change token storage to DB
* Set up Strava webhook that triggers the app when a new Strava activity is loaded
* Save activity data to DB
* Get last 50 Spotify tracks played when the activity is loaded to the DB
* Save track data to DB
* NOTE: this creates a limitation that we can only analyze the last 50 tracks played, with no workaround

