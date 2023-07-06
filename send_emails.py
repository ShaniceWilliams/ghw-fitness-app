import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from dotenv import dotenv_values

PORT = 587
EMAIL_SERVER = "smtp.office365.com"

secrets = dotenv_values(".env")

sender_email = secrets['EMAIL']
sender_pw = secrets['EMAIL_PASSWORD']


def send_email(receiver_email, video_title, video_url):
    msg = EmailMessage()
    msg["Subject"] = "Today's workout from Find Your Fitness!"
    msg["From"] = formataddr(("Find Your Fitness", f"{sender_email}"))
    msg["To"] = receiver_email

    msg.set_content(
        f"""\
        Good morning!
        
        Let's start the day with today's workout:
        
        {video_title}
        {video_url}
        
        Smash this workout to smash your goals!
        
        Find Your Fitness
        """
    )

    msg.add_alternative(
        f"""\
        <html>
            <body>
                <p>Good morning!</p>

                <p>Let's start the day with today's workout:</p>

                <a href={video_url}>{video_title}</a>
                
                <p>Smash this workout to smash your goals!</p>

                <p>Find Your Fitness</p>
            </body>
        </html>
            """, subtype="html"
    )

    with smtplib.SMTP(EMAIL_SERVER, PORT) as server:
        server.starttls()
        server.login(sender_email, sender_pw)
        server.sendmail(sender_email, receiver_email, msg.as_string())


if __name__ == "__main__":
    send_email(
        receiver_email=secrets['RECEIVER_EMAIL'],
        video_title="50 Min Fat Burning HIIT Workout | Burn 1000 Calories (Full Body, At Home)",
        video_url="https://youtu.be/1s_0rUUo0A0"

    )
