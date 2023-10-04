# stravafy

# Run API in Docker:
1. `cd` into `stravafy/src`
2. `docker-compose up --build`
3. Check the API Swagger docs: `localhost:8000/docs`


## Authorize Strava or Spotify
1. In a web browser URL: `localhost:8000/api/auth/strava` or `localhost:8000/api/auth/spotify`
2. Token is stored on the server; you can now use the other endpoints



### ISSUES
* Spotify will only let you get the last 50 recently played tracks, no matter the time inputs you give
* Wildly annoying

### TODO
* Create user sessions somehow
    * Set up Strava webhook that triggers the app when a new Strava activity is loaded for a user based on their IDs
    * Create a user model
* Move encryption secret somewhere secure (DB?)
    * Related: Audit token handling
* Add a DB (Postgres?)
    * Run a DB container
    * Create DB interface
    * Create schema based on current models
    * Change token storage to DB
    * Set up token refresh (Maybe?)
    * Save activity data to DB
    * Get last 50 Spotify tracks played when the activity is loaded to the DB
    * Save track data to DB
* NOTE: this creates a limitation that we can only analyze the last 50 tracks played from the point in time the Strava activity is loaded to the DB, with no workaround
* NOTE: For this to work in a practical sense, it actually needs to be deployed somewhere


### TODO (long-term)
* Deployment
    * Write tests that are actually good lol
    * Fork `main` branch to `dev` and `test`
    * Set git rules to `read-only` on `main`
    * Precommit hooks with `black`, `pep8`, `mypy`, etc...
    * IaC
        * OpenTF?
    * CI/CD
        * Jenkins server? Circle CI? Cloud specific?
* Front-End
    * ... Dash?
    * Learn typescript?

