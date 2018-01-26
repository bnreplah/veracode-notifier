# Usage

In the example Slack notification the webhook URL is read from environment variables, so one way to run the app would be:

    cd veracode-notifier/
    SLACK_WEBHOOK_URL=<your_slack_webhook_url> python -m veracodenotifier.main
    
# Development

Any .py file placed in `veracodenotifier/actions` or `veracodenotifier/notifications` will be loaded as an action or notification plugin.

Actions are changes in the Veracode platform that results in an event stream being generated. To create a new one, add a .py file to the `actions` folder containing a class that inherits from `veracodenotifier.helpers.base_action.Action`. This class must implement the `pre_action()`, `action()`, and `post_action()` methods, which will each be passed an instance of `VeracodeAPI` as found in `veracodenotifier.helpers.api`. The `action()` method must return a list of events, each event being a dictionary. Dictionary values will be concatenated to a message string. Dictionary keys may be used at some point in the future development of this app but currently are not.

Notifications take an event and post the event as a message to a service of your choice. To create a new one, add a .py file to the `notifications` folder containing a class that inherits from `veracodenotifier.helpers.base_notification.Notification`. This class must implement the `send_notification()` method which takes an event and does something with it.
