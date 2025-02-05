# -*- coding: utf-8 -*-
"""
Send gmail using  App password. 
    You must got to Google account. Security tab: https://myaccount.google.com/security
    Active 2 Step Verification. 
    After this new option under "Signing in to Google" the "App passwords" option will be activated. 
    Just create one app password and use as password to authenticate
References: https://stackoverflow.com/questions/72478573/sending-and-email-using-python-problem-causes-by-last-google-policy-update-on
"""
import json
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from json_sample.json_with_comment import JSONWithCommentsDecoder


def send(sent_subject, sent_text):
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_app_password = os.environ.get("GMAIL_APP_PW")
    sent_from = gmail_user
    sent_to = ["phungxuananh1991+python_app@gmail.com"]

    email_text = "\r\n".join(
        [
            "To: {}".format(", ".join(sent_to)),
            "From: {}".format(sent_from),
            "Subject: {}".format(sent_subject),
            "",
            sent_text,
        ]
    ).encode("utf-8")

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print("Email sent!")
    except Exception as exception:
        print("Error: %s!\n\n" % exception)


def send_html_email():
    gmail_user = os.environ.get("GMAIL_USER")
    gmail_app_password = os.environ.get("GMAIL_APP_PW")
    sent_from = gmail_user
    sent_to = "phungxuananh1991+python_app@gmail.com"
    # Create message container - the correct MIME type is multipart/alternative.

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Link"
    msg["From"] = sent_from
    msg["To"] = sent_to

    # Create the body of the message (a plain-text and an HTML version).
    text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.python.org"
    html = """\
    <html>
    <head></head>
    <body>
        <p>Hi!<br>
        How are you?<br>
        Here is the <a href="http://www.python.org">link</a> you wanted.
        </p>
    </body>
    </html>
    """

    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.ehlo()
    server.login(gmail_user, gmail_app_password)
    server.sendmail(sent_from, sent_to, msg.as_string())
    server.close()


if __name__ == "__main__":
    # sent_subject = "this is test"
    # sent_text = "this is content"
    # send(sent_subject, sent_text)
    send_html_email()
