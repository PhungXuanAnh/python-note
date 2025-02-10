"""
NOTE: recommended to use slack_sdk instead of slackclient
"""
import json
import traceback
from io import BytesIO

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from slack_sdk.webhook.client import WebhookClient

client = WebClient()
api_response = client.api_test()

credentials = json.loads(open("/home/xuananh/Dropbox/Work/Other/credentials_bk/slack_phungxuananh_workspace.json", "r").read())
SLACK_API_TOKEN = credentials["apps"]["xa-sample-app"]["Bot User OAuth Token"]

def send_slack_alert_to_merchant(webhook_url: str, text: str = None, blocks: list = None):
    """Send slack alert to merchant"""
    client = WebhookClient(webhook_url)
    try:
        client.send(text=text, blocks=blocks)
    except Exception as e:  # noqa
        traceback.print_exc()


def send_slack_message(channel: str, text: str):
    """Send slack alert"""
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        client.chat_postMessage(channel=channel, text=text)
    except SlackApiError as e:
        traceback.print_exc()


def send_slack_alert(channel: str, text: str):
    """Send slack alert"""
    user_id = ("<@UATVB018R>\n",)   # XuanAnh's user id
    msg = user_id + text
    send_slack_message(channel, msg)


def upload_slack_file_v1(channel: str, file_content_bytes: bytes, initial_comment: str, filename: str):
    """
        Upload slack file to a slack channel
        NOTE: to upload a file to a slack channel, the slack app must be installed to that channel,
            else you will encountered error { "ok": false, "error": "not_in_channel" }
            reference: https://stackoverflow.com/a/68475477/7639845
    """
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        with BytesIO() as b:
            b.write(file_content_bytes)
            b.seek(0)
            client.files_upload(
                channels=channel,
                initial_comment=initial_comment,
                file=b,
                filename=filename,
            ) # UserWarning: client.files_upload() may cause some issues like timeouts for relatively large files. 
            # Our latest recommendation is to use client.files_upload_v2(), which is mostly compatible and much stabler, instead.
    except SlackApiError as e:
        traceback.print_exc()
        
        

def upload_slack_file_v2(channel_id: str, file_content_bytes: bytes, initial_comment: str, filename: str):
    """
        Upload slack file to a slack channel
        NOTE: to upload a file to a slack channel, the slack app must be installed to that channel,
            else you will encountered error { "ok": false, "error": "not_in_channel" }
            reference: https://stackoverflow.com/a/68475477/7639845
    """
    client = WebClient(token=SLACK_API_TOKEN)
    try:
        with BytesIO() as b:
            b.write(file_content_bytes)
            b.seek(0)
            client.files_upload_v2(
                channel=channel_id,
                initial_comment=initial_comment,
                file=b, # file: Optional[Union[str, bytes, IOBase]] = None,
                filename=filename,
            )
    except SlackApiError as e:
        traceback.print_exc()
        

if __name__ == "__main__":
    send_slack_message(
        "#general", "aaaaaaaaaaaaaaaaaaaaaaaaaa, this message sent from slack_sdk"
    )

    # upload_slack_file_v1("#general", open("requirements.txt", "rb").read(),
    #                   initial_comment="this is attachment from XuanAnh using upload_v1",
    #                   filename="requirements.txt"
    #                   )

    # upload_slack_file_v2(
    #                     channel_id="CATQVNDJ4", # NOTE: this is id of the channel general
    #                     file_content_bytes=open("requirements.txt", "rb").read(),
    #                     initial_comment="this is attachment from XuanAnh using upload_v2",
    #                     filename="requirements.txt"
    #                 )
