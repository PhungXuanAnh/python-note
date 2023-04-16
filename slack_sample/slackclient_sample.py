import json
import traceback
from io import BytesIO
from slack import WebClient
from slack.errors import SlackApiError

"""
    How to get app token and set scope for app, below is steps for setting app xa-sample-app 
        with app id is A052Z4HGNT1 

    1. Create your app as normal, go to https://api.slack.com/apps, choose app xa-sample-app or access this link: https://api.slack.com/apps/A052Z4HGNT1
        to go to management page of this app
    2. Go to General, or access this link https://api.slack.com/apps/A052Z4HGNT1/general? to see general config of app
        Choose Install your app to install your app to a slack workspace
        Or you also go here to install your app https://api.slack.com/apps/A052Z4HGNT1/install-on-team?
    3. Go to OAuth & Permissions or access this link https://api.slack.com/apps/A052Z4HGNT1/oauth?
        a. Move to Scopes part, 
            Move to User Token Scopes, add scope that you want to add, refer list of scopes: https://api.slack.com/scopes
        b. Move to OAuth Tokens for Your Workspace part
            Copy token in Bot User OAuth Token text box, this token will be use by slackclient 
"""
credentials = json.loads(open("/home/xuananh/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json", "r").read())
SLACK_API_TOKEN = credentials["apps"]["xa-sample-app"]["Bot User OAuth Token"]

def send_slack_alert(channel: str, text: str):
    """Send slack alert"""
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        traceback.print_exc()


def upload_slack_file(channel: str, file_content_bytes: bytes, text: str):
    """Upload slack file"""
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        with BytesIO() as b:
            b.write(file_content_bytes)
            b.seek(0)
            client.files_upload(
                channels=channel,
                initial_comment=text,
                file=b,
                filename="file",
            )
    except SlackApiError as e:
        traceback.print_exc()
        
        
send_slack_alert("#general", "aaaaaaaaaaaaaaaaaaaaaaaaaa, this message sent from slackclient")