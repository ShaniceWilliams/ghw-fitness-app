from send_emails import send_email
import database as dbs
import random
import logging.handlers

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger_file_handler = logging.handlers.RotatingFileHandler(
    "status.log",
    maxBytes=1024 * 1024,
    backupCount=1,
    encoding="utf8",
)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger_file_handler.setFormatter(formatter)
logger.addHandler(logger_file_handler)


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
    emails_sent = 0
    for email in emails:
        recipient = email["email_id"]
        url, video_title = retrieve_daily_wo_info()
        send_email(recipient, video_title, url)
        emails_sent += 1
    return emails_sent


# Add the ability to send an email out everyday - This is being managed by Github actions


def main():
    result = send_email_to_db_emails()
    logger.info(f'Number of emails sent: {result}')


if __name__ == "__main__":
    main()
