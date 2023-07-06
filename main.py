from datetime import date
from send_emails import send_email
import database as dbs
import random
import time
import datetime as dt
from dotenv import dotenv_values

secrets = dotenv_values()


def get_workouts():
    return dbs.all_workouts()


def retrieve_daily_wo_info():
    workouts = get_workouts()
    n = len(workouts)
    index = random.randint(0, n - 1)
    wo = workouts[index]
    dbs.update_workout_today(wo, insert=True)
    url = "https://youtu.be/" + wo["video_id"]
    video_title = wo['title']
    return url, video_title


# Retrieve emails from database and sends email to each
def send_email_to_db_emails():
    emails = dbs.all_emails()
    for email in emails:
        recipient = email["email_id"]
        url, video_title = retrieve_daily_wo_info()
        send_email(recipient, video_title, url)


# Add the ability to send an email out everyday



def main():
    send_email_to_db_emails()


if __name__ == "__main__":
    main()
