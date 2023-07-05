import harperdb
from dotenv import dotenv_values

secrets = dotenv_values(".env")
# Dotenv_values must be used for Harper db as there is a .env file that the harper package uses so loadenv does not work.

db = harperdb.HarperDB(
    url=secrets["URL"],
    username=secrets["USERNAME"],
    password=secrets["PASSWORD"]
)

SCHEMA = "fitness_app"
TABLE = "workouts"
TABLE_TODAY = "todays_workout"


# Inserts the specified data into the specified schema and table. Data must be in a list
def insert_workout(workout_data):
    return db.insert(SCHEMA, TABLE, [workout_data])


# Deletes the specified data based on the video id from the specified schema and table. Data must be in a list.
def delete_workout(workout_id):
    return db.delete(SCHEMA, TABLE, [workout_id])


# Uses SQL statement to show all data from the specified schema and table.
def all_workouts():
    return db.sql(f"SELECT * FROM {SCHEMA}.{TABLE}")


# Uses SQL statement to show the data for the video of the day from the specified schema and table.
def get_todays_workout():
    return db.sql(f"SELECT * FROM {SCHEMA}.{TABLE_TODAY} WHERE id = 0")


# Function to update which record is considered the workout for the day based on the workout video_id
def update_workout_today(workout_data, insert=False):
    workout_data['id'] = 0
    if insert:
        return db.insert(SCHEMA, TABLE_TODAY, [workout_data])
    return db.update(SCHEMA, TABLE_TODAY, [workout_data])


import yt_api

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
secrets = dotenv_values(".env")
yt = yt_api.connect_yt(secrets)
video_url = "https://youtu.be/fPJVkF_9jmI"
video = yt_api.get_video_id(video_url)
infos = yt_api.parse_yt_data(yt, video)
print(infos)
insert_workout(infos)
workouts = all_workouts()
print(workouts)