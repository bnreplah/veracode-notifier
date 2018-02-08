import os
import time
import boto3
import botocore
from datetime import datetime
import veracodenotifier.actions
import veracodenotifier.notifications
from veracodenotifier.helpers.base_action import Action
from veracodenotifier.helpers.base_notification import Notification
from veracodenotifier.helpers.api import VeracodeAPI


def date_print(string):
    now = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S UTC]")
    print(now + " " + string)


def main(event, context):
    date_print("Starting...")

    if "S3-BUCKET" in os.environ and "S3-REGION" in os.environ:
        s3_bucket_name = os.environ.get("S3-BUCKET")
        s3_region = os.environ.get("S3_REGION")
        s3_client = boto3.client("s3")
    else:
        return

    api = VeracodeAPI()

    try:
        s3_client.head_bucket(Bucket=s3_bucket_name)
    except s3_client.exceptions.NoSuchBucket:
        s3_client.create_bucket(Bucket=s3_bucket_name, CreateBucketConfiguration={"LocationConstraint": s3_region})

    events = []

    date_print("Running actions...")
    for action_class in Action.actions:
        if action_class.pre_action(api, s3_client, s3_bucket_name):
            events.extend(action_class.action(api, s3_client, s3_bucket_name))
        action_class.post_action(api, s3_client, s3_bucket_name)

    date_print("Running notifications...")
    for notification_class in Notification.notifications:
        for event in events:
            notification_class.send_notification(event)


if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(300)
    except KeyboardInterrupt:
        date_print("Exiting...")
