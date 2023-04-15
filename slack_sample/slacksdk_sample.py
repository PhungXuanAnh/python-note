import json
import traceback
from slack_sdk.webhook.client import WebhookClient


credentials = json.loads(open("/home/xuananh/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json", "r").read())
SLACK_API_TOKEN = credentials["apps"]["test-app1"]["Bot User OAuth Token"]

def send_slack_alert_to_merchant(webhook_url: str, text: str = None, blocks: list = None):
    """Send slack alert to merchant"""
    client = WebhookClient(webhook_url)
    try:
        client.send(text=text, blocks=blocks)
    except Exception as e:  # noqa
        traceback.print_exc()
