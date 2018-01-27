import os
import requests
import json
from veracodenotifier.helpers.base_notification import Notification


class SlackNotification(Notification):
    def __init__(self):
        self.slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")

    def send_notification(self, event):
        payload = {"text": event["message"]}
        requests.post(self.slack_webhook_url, data=json.dumps(payload))
