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
import smtplib
from typing import Any
from pathlib import Path

import sys, os
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../json_sample"))
)

from json_with_c_comment import JSONWithCommentsDecoder


def send_gmail(sent_subject, sent_text):
    with open(
        "/home/xuananh/Dropbox/Work/Other/credentials_bk/google-account.json", "r"
    ) as f:
        account = json.loads(f.read(), cls=JSONWithCommentsDecoder)[0]
        gmail_user = account["email"]
        gmail_app_password = account["password"]

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
    )

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print("Email sent!")
    except Exception as exception:
        print("Error: %s!\n\n" % exception)


if __name__ == "__main__":
    sent_subject = "this is test"
    sent_text = "this is content"
    send_gmail(sent_subject, sent_text)
