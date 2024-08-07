import logging
import requests
import sys
import traceback
import json


class SlackWebhookHandler(logging.Handler):
    def __init__(self, webhook_url):
        self.webhook_url = webhook_url        
        logging.Handler.__init__(self)
        
    def emit(self, record):
        msg = self.format(record)
        headers = {'Content-type': 'application/json'}
        try:
            requests.post(url=self.webhook_url, headers=headers, json={"text": msg})
        except:
            traceback.print_exc()
        

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO,
                    format='%(name)-12s %(asctime)s  %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    stream=sys.stdout)

    logger1 = logging.getLogger('logger1')
    logger2 = logging.getLogger('logger2')

    #======================================== add handler =============================
    """
        1. How to get webhook, go to: https://api.slack.com/apps
        2. Choose your app in below of website
        3. Choose `Incomming Webhooks`
        4. Choose `Activate Incoming Webhooks`
        5. Choose `Add New Webhook to Workspace`
        
        For example: webhook in below json file for app xa-sample-app
            you can access webhook management off xa-sample-app by this link: https://api.slack.com/apps/A052Z4HGNT1/incoming-webhooks?success=1
            
        NOTE: webhook only for 1 channel, if you want to send message to multiple channel, using slackclient with Bot User OAuth Token
    """
    WEBHOOK_URL = json.loads(open("/home/xuananh/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json", "r").read())["webhook"]
    slack_webhook_handler = SlackWebhookHandler(webhook_url=WEBHOOK_URL)
    slack_webhook_handler.setLevel(logging.INFO)
    slack_webhook_handler.setFormatter(logging.Formatter(
                            '`%(name)-12s` - [%(asctime)s] - `%(levelname)-3s`: %(message)s'))
    logging.getLogger("logger1").addHandler(slack_webhook_handler)
    #========================================

    logger1.error('11111111111111111111, this message sent using webhook')
    logger2.error('22222222222222222222')
    logging.error('00000000000000000000')


