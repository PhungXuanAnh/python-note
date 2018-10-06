# -*- coding: utf-8 -*-
'''
Turn off Tùy chọn cài đặt về quyền truy cập cho các ứng dụng kém an toàn tai link:
https://myaccount.google.com/lesssecureapps
'''
import json
import smtplib


def send_gmail(sent_subject, sent_text):
    with open('/home/xuananh/Dropbox/Work/Other/gmail-account.json', 'r') as f:
        account = json.loads(f.read())[0]
        gmail_user = account['email']
        gmail_app_password = account['password']

    sent_from = gmail_user
    sent_to = ['phungxuananh1991@gmail.com', 'phungxuananh1991+1@gmail.com']

    email_text = '\r\n'.join(['To: {}'.format(", ".join(sent_to)),
                              'From: {}'.format(sent_from),
                              'Subject: {}'.format(sent_subject),
                              '', sent_text])

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_app_password)
        server.sendmail(sent_from, sent_to, email_text)
        server.close()

        print('Email sent!')
    except Exception as exception:
        print("Error: %s!\n\n" % exception)


if __name__ == '__main__':
    sent_subject = 'this is test'
    sent_text = 'this is content'
    send_gmail(sent_subject, sent_text)
