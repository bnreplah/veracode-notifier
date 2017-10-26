import os
import requests
import json


def send_notification(event):
    if event is not None:
        slack_webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
        payload = {"text": ": ".join(event.values())}
        requests.post(slack_webhook_url, data=json.dumps(payload))
