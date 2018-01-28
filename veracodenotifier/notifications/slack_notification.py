import os
import requests
import json
from helpers.base_notification import Notification


class SlackNotification(Notification):
    def __init__(self):
        self.slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        self.colours = {
            "create": "#00AA00",
            "update": "0000AA",
            "delete": "AA0000"
        }

    def send_notification(self, event):
        payload = {
            "attachments": [
                    {
                        "fallback": event["message"]["simple"],
                        "title": event["message"]["title"],
                        "title_link": "https://analysiscenter.veracode.com/",
                        "text": event["message"]["text"],
                        "color": self.colours[event["type"]]
                    }
            ]
        }
        requests.post(self.slack_webhook_url, data=json.dumps(payload))
