import time
from datetime import datetime
from veracodenotifier import actions
from veracodenotifier import notifications
from veracodenotifier.helpers.base_action import Action
from veracodenotifier.helpers.base_notification import Notification
from veracodenotifier.helpers.api import VeracodeAPI


def dateprint(string):
    now = datetime.utcnow().strftime("[%Y-%m-%d %H:%M:%S UTC]")
    print(now + " " + string)


def main():
    dateprint("Starting...")
    api = VeracodeAPI()

    try:
        while True:
            events = []

            dateprint("Running actions...")
            for action_class in Action.actions:
                action_class.pre_action(api)
                events.extend(action_class.action(api))
                action_class.post_action(api)

            dateprint("Running notifications...")
            for notification_class in Notification.notifications:
                for event in events:
                    notification_class.send_notification(event)

            time.sleep(500)

    except KeyboardInterrupt:
        dateprint("Exiting...")


if __name__ == "__main__":
    main()
