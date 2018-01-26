import time
from veracodenotifier import actions
from veracodenotifier import notifications
from veracodenotifier.helpers.base_action import Action
from veracodenotifier.helpers.base_notification import Notification
from veracodenotifier.helpers.api import VeracodeAPI


def main():
    print("Starting...")
    events = []
    api = VeracodeAPI()

    try:
        while True:
            print("Running actions...")
            for action_class in Action.actions:
                action_class.pre_action(api)
                events.extend(action_class.action(api))
                action_class.post_action(api)

            print("Running notifications...")
            for notification_class in Notification.notifications:
                for event in events:
                    notification_class.send_notification(event)

            time.sleep(500)

    except KeyboardInterrupt:
        print("Exiting...")


if __name__ == "__main__":
    main()
