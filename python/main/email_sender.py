import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from utils import *

def send_email(sender, recipients, subject, body):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = ", ".join(recipients)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender, "btcethltcxrp")
    text = msg.as_string()
    server.sendmail(sender, recipients, text)
    server.quit()

def get_recipients():
    recipients = []
    with open("../resource/email/recipients.txt", "rb") as f:
         recipients = f.read().split("\n")
    return recipients

if __name__ == "__main__":

    body = "Hello"
    recipients = ['dhrumin.desai28@gmail.com']
    sender = "ddcryptonotification@gmail.com"
    subject = "Test"
    send_email(sender, recipients, subject, body)
