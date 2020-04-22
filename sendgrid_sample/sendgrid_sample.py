"""
Step 1: Create api key: 
        https://app.sendgrid.com/settings/api_keys
        https://sendgrid.com/docs/ui/account-and-settings/api-keys/

Step 2: Create and verify Sender Authentication (Single Sender Verification): 
        https://app.sendgrid.com/settings/sender_auth
        https://sendgrid.com/docs/ui/sending-email/sender-verification/
        for example: Sender Verification using email: test@example.com
        then in request body, field from_email: test@example.com

Step 3: using SendGrid's Python Library:
    pip install sendgrid
    https://github.com/sendgrid/sendgrid-python
    https://app.sendgrid.com/guide/integrate/langs/python
    Getting started: https://sendgrid.com/docs/API_Reference/api_getting_started.html

Step 4: debug by call api directly
    https://sendgrid.com/docs/API_Reference/Web_API_v3/Mail/index.html

    curl --location --request POST 'https://api.sendgrid.com/v3/mail/send' \
        --header 'authorization: Bearer YOUR_API_KEY' \
        --header 'content-type: application/json' \
        --header 'Content-Type: text/plain' \
        --data-raw '{
            "personalizations":[
                {
                    "to":[
                            {
                                "email":"receiver@gmail.com",
                                "name":"Receiver Name"
                                
                            }
                        ],
                    "subject":"Hello, World!"
                    
                }
            ],
            "from":
                {
                    "email":"test@example.com",
                    "name":"Test Name"
                },
            "reply_to":
                {
                    "email":"test@example.com",
                    "name":"Test Name"
                },
            "content": [
                {
                    "type": "text/plain",
                    "value": "this is test email"
                }
                ]
        }'
"""


from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

with open('/home/xuananh/Dropbox/Work/Other/sendgrid-api-key-test', 'r') as f:
    SENDGRID_API_KEY = f.read()

message = Mail(
    from_email='xuan.anh.phung@advesa.com',
    to_emails='phungxuananh1991@gmail.com',
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(SENDGRID_API_KEY)
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    import traceback
    traceback.print_exc()