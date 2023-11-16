CREATE TABLE "strava_activity" (
  "activity_id" int PRIMARY KEY,
  "user_id" int,
  "activity_type" varchar,
  "timezone" varchar,
  "start_date" timestamp,
  "suffer_score" decimal,
  "heartrate" int[],
  "time" int[],
  "distance" int[]
);

CREATE TABLE "spotify_track" (
  "track_id" int PRIMARY KEY,
  "title" varchar,
  "artist" varchar[],
  "album" varchar,
  "release_date" varchar,
  "track_length" int,
  "acousticness" float,
  "danceability" float,
  "energy" float,
  "instrumentalness" float,
  "speechiness" float,
  "tempo" float,
  "valence" float
);

CREATE TABLE "strava_spotify_link" (
  "link_id" int PRIMARY KEY,
  "activity_id" int,
  "track_id" int,
  "played_at" timestamp
);

CREATE TABLE "user" (
  "user_id" int PRIMARY KEY,
  "strava_token" varchar,
  "spotify_token" varchar,
  "user_pass" varchar
);

ALTER TABLE "strava_spotify_link" ADD FOREIGN KEY ("activity_id") REFERENCES "strava_activity" ("activity_id");

ALTER TABLE "strava_spotify_link" ADD FOREIGN KEY ("track_id") REFERENCES "spotify_track" ("track_id");

ALTER TABLE "strava_activity" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("user_id");
