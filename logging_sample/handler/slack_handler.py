"""
HOW TO GET SLACK TOKEN API

1. Login to your workspacke: https://slack.com/signin
2. Acess url: https://api.slack.com/custom-integrations/legacy-tokens
3. Đi đến phần Legacy token generator để lấy token

"""

import json
import logging
from slacker_log_handler import SlackerLogHandler, NoStacktraceFormatter

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='/tmp/stream_handler_test.txt',
                    filemode='a')

# Create slack handler
'NOTE: get api_key from here: https://api.slack.com/custom-integrations/legacy-tokens'

with open('/home/xuananh/Dropbox/Work/Other/slack-token-api-key.json', "r") as in_file:
    SLACK_API_KEY = json.load(in_file)['phungxuananh']

'''NOTE: tham so channel co the co hoac khong co # dang truoc cung duoc'''
slack_handler = SlackerLogHandler(api_key=SLACK_API_KEY,
                                  channel='general', stack_trace=True, username='xuananh')

# Create logger
logger = logging.getLogger('debug_application')
logger.addHandler(slack_handler)

# OPTIONAL: Define a log message formatter.
# If you have set stack_trace=True, any exception stack traces will be included as Slack message attachments.
# You therefore need to use NoStacktraceFormatter as a base to exclude the trace from the main message text.
formatter = NoStacktraceFormatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
slack_handler.setFormatter(formatter)

# Define the minimum level of log messages you want to send to Slack
slack_handler.setLevel(logging.DEBUG)

# Test logging
logger.error("Debug message from slack!")
