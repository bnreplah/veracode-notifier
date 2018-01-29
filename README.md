# README needs updating for this branch

# Install

    git clone https://github.com/ctcampbell/veracode-notifier.git

Install Veracode module veracode-api-signing (speak to your Veracode Solution Architect for this file)

    pip install veracode_api_signing-17.0.0-py2.py3-none-any.whl

API credentials must be enabled on a Veracode account and placed in `~/.veracode/credentials`

    [default]
    veracode_api_key_id = <YOUR_API_KEY_ID>
    veracode_api_key_secret = <YOUR_API_KEY_SECRET>

File permissions should be set appropriately

    chmod 600 ~/.veracode/credentials

Install other dependencies

    pip install -r requirements.txt

# Usage

In the example Slack notification the webhook URL is read from environment variables, so one way to run the app would be:

    cd veracode-notifier/
    SLACK_WEBHOOK_URL=<your_slack_webhook_url> python -m veracodenotifier.main
    
# Development

Any .py file placed in `veracodenotifier/actions` or `veracodenotifier/notifications` will be loaded as an action or notification plugin.

Actions are changes in the Veracode platform that results in an event stream being generated. To create a new one, add a .py file to the `actions` folder containing a class that inherits from `veracodenotifier.helpers.base_action.Action`. This class must implement the `pre_action()`, `action()`, and `post_action()` methods, which will each be passed an instance of `VeracodeAPI` as found in `veracodenotifier.helpers.api`. The `action()` method must return a list of events, each event being a dictionary with a `message` key/value pair.

Notifications take an event and post the event as a message to a service of your choice. To create a new one, add a .py file to the `notifications` folder containing a class that inherits from `veracodenotifier.helpers.base_notification.Notification`. This class must implement the `send_notification()` method which takes an event and does something with it.
