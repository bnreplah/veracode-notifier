import os.path
import pkgutil
from veracodenotifier import actions
from veracodenotifier import notifications
from veracodenotifier.helpers.api import VeracodeAPI


def main():
    api = VeracodeAPI()

    actions_package_path = os.path.dirname(actions.__file__)
    action_names = [name for _, name, _ in pkgutil.iter_modules([actions_package_path])]

    events = []

    for action_name in action_names:
        getattr(actions, action_name).pre_action(api)
        events.append(getattr(actions, action_name).action(api))
        getattr(actions, action_name).post_action(api)

    notifications_package_path = os.path.dirname(notifications.__file__)
    notification_names = [name for _, name, _ in pkgutil.iter_modules([notifications_package_path])]

    for notification_name in notification_names:
        for event in events:
            getattr(notifications, notification_name).send_notification(event)


if __name__ == "__main__":
    main()
