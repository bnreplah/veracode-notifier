from veracodenotifier import actions
from veracodenotifier import notifications
from veracodenotifier.helpers.base_action import Action
from veracodenotifier.helpers.base_notification import Notification
from veracodenotifier.helpers.api import VeracodeAPI


def main():
    events = []
    api = VeracodeAPI()

    for action_class in Action.actions:
        action_class.pre_action(api)
        events.extend(action_class.action(api))
        action_class.post_action(api)

    for notification_class in Notification.notifications:
        for event in events:
            notification_class.send_notification(event)


if __name__ == "__main__":
    main()
