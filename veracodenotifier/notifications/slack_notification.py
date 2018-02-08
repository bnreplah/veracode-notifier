import os
import requests
import json
from veracodenotifier.helpers.base_notification import Notification


class SlackNotification(Notification):
    def __init__(self):
        self.slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        self.colours = {
            "create": "#8FBC48",
            "update": "#00B3E6",
            "delete": "#D73185"
        }

    def send_notification(self, event):
        payload = {
            "attachments": [
                    {
                        "fallback": event["message"]["simple"],
                        "title": event["message"]["title"],
                        "text": "```" + event["message"]["text"] + "```",
                        "color": self.colours[event["type"]]
                    }
            ]
        }
        requests.post(self.slack_webhook_url, data=json.dumps(payload))
