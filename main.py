import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
import argparse
import sys

from urllib.request import urlopen
from bs4 import BeautifulSoup


def extract_report(weather_station: str) -> str:
    url = (
        "http://web.directemar.cl/met/jturno/PRONOSTICOS/Cenmeteopmo/72/"
        + weather_station
        + ".txt"
    )
    html = urlopen(url).read()
    soup = BeautifulSoup(html, features="html.parser")
    mail_content = soup

    return mail_content


def compose_email(
    sender_address: str, receiver_address: str, weather_station: str
) -> MIMEMultipart:
    message = MIMEMultipart()
    message["From"] = sender_address
    message["To"] = receiver_address
    message["Subject"] = "Weahter Report - " + weather_station  # The subject line

    mail_content = extract_report(weather_station=weather_station)

    message.attach(MIMEText(mail_content, "plain", _charset="UTF-8"))

    return message


def send_email(
    sender_address: str,
    sender_pass: str,
    receiver_address: str,
    message: MIMEMultipart,
) -> None:

    # Create SMTP session for sending the mail
    session = smtplib.SMTP("smtp.gmail.com", 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address.split(","), text)
    session.quit()


def main(data, context):

    load_dotenv()
    SENDER_EMAIL = os.environ.get("SENDER_EMAIL")
    SENDER_EMAIL_PASS = os.environ.get("SENDER_EMAIL_PASS")
    RECEIVER_EMAIL = os.environ.get("RECEIVER_EMAIL")
    STATIONS = os.environ.get("STATIONS")

    for station in STATIONS.split(","):

        print(f"Composing email station {station}.")
        message = compose_email(
            sender_address=SENDER_EMAIL,
            receiver_address=RECEIVER_EMAIL,
            weather_station=station,
        )

        print(f"Sending {station} weather report to recipients.")
        send_email(
            sender_address=SENDER_EMAIL,
            sender_pass=SENDER_EMAIL_PASS,
            receiver_address=RECEIVER_EMAIL,
            message=message,
        )

        print(
            f"Report succesfully sent to all recipients for weather station {station}.\n"
        )


if __name__ == "__main__":
    main("data", "context")
