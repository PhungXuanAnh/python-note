import json
import traceback
from io import BytesIO
from slack import WebClient
from slack.errors import SlackApiError


credentials = json.loads(open("/home/xuananh/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json", "r").read())
SLACK_API_TOKEN = credentials["apps"]["test-app1"]["Bot User OAuth Token"]

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
        
        
send_slack_alert("#general", "aaaaaaaaaaaaaaa")