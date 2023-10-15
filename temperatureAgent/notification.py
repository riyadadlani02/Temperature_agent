from twilio.rest import Client
import requests
import smtplib

ACCOUNT_SID = 'AC909f13bae06e879cdc600757b1fd62f2'
AUTH_TOKEN = '45b3c96c30fbf5a3e97a1f74a1a3d879'
SENDER_EMAIL = "anshkhurana117@gmail.com"
PASSWORD = "psvh uwau bypm lemb"


def send_whatsapp_notification(message, mobileNumber):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=message,
        to=f'whatsapp:+91{mobileNumber}'
    )


def send_email_notification(message, receiver_email):
    email_message = f"Subject: Temperature Alert\n\n{message}"
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(SENDER_EMAIL, PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, email_message)


def push_notification(message, mobileNumber, emailId):
    send_whatsapp_notification(message, mobileNumber)
    send_email_notification(message, emailId)


if __name__ == '__main__':
    send_email_notification("TEST", "sarfarajansaridev@gmail.com")
