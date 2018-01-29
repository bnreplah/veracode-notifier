import os
import time
import boto3
import botocore
from datetime import datetime
import actions
import notifications
from helpers.base_action import Action
from helpers.base_notification import Notification
from helpers.api import VeracodeAPI


def date_print(string):
    now = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S UTC]")
    print(now + " " + string)


def main():
    date_print("Starting...")
    api = VeracodeAPI()

    s3_bucket_name = "veracode-notifier-" + os.environ.get("VID")
    s3_region = os.environ.get("S3_REGION")
    s3 = boto3.client('s3')
    try:
        s3.head_bucket(Bucket=s3_bucket_name)
    except botocore.exceptions.ClientError as e:
        error_code = int(e.response['Error']['Code'])
        if error_code == 404:
            s3.create_bucket(Bucket=s3_bucket_name, CreateBucketConfiguration={"LocationConstraint": s3_region})

    events = []

    date_print("Running actions...")
    for action_class in Action.actions:
        if action_class.pre_action(api, s3, s3_bucket_name):
            events.extend(action_class.action(api, s3, s3_bucket_name))
        action_class.post_action(api, s3, s3_bucket_name)

    date_print("Running notifications...")
    for notification_class in Notification.notifications:
        for event in events:
            notification_class.send_notification(event)


def lambda_handler(event, context):
    main()
    date_print("Exiting...")


if __name__ == "__main__":
    try:
        while True:
            main()
            time.sleep(300)
    except KeyboardInterrupt:
        date_print("Exiting...")
