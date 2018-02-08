# Install

    git clone https://github.com/ctcampbell/veracode-notifier.git

Install dependencies (in a virtualenv)

    pip install -r requirements.txt

# Usage

The project is designed to be deployed into AWS as a Lambda function. [Set up your AWS credentials first](https://aws.amazon.com/blogs/security/a-new-and-standardized-way-to-manage-credentials-in-the-aws-sdks/).

To use Zappa to deploy, create a `zappa_settings.json` file in the root directory:

```json
{
    "production": {
        "aws_region": "<YOUR-PREFERRED-AWS-REGION>",
        "profile_name": "default",
        "project_name": "veracode-notifier",
        "runtime": "python3.6",
        "s3_bucket": "<YOUR-UNIQUE-S3-BUCKET-NAME>",
        "apigateway_enabled": false,
        "timeout_seconds": 300,
        "keep_warm": false,
        "events": [{
            "function": "veracodenotifier.main.main",
            "expression": "rate(1 minute)"
        }],
        "aws_environment_variables": {
            "VERACODE_API_KEY_ID": "<YOUR-VERACODE-API-KEY-ID>",
            "VERACODE_API_KEY_SECRET": "<YOUR-VERACODE-API-KEY-SECRET>",
            "S3_REGION": "<YOUR-PREFERRED-AWS-REGION>",
            "S3_BUCKET": "<YOUR-UNIQUE-S3-BUCKET-NAME>",
            "SLACK_WEBHOOK_URL": "<YOUR-SLACK-INCOMING-WEBHOOK-URL>"
        }
    }
}
``` 

Then run `zappa deploy production` to configure in AWS. The config above will run the Lambda once a minute.

It's worth pointing out that the default AWS permissions that will be attached to the Lambda are very permissive. You may want to look into the [Zappa docs](https://github.com/Miserlou/Zappa#using-custom-aws-iam-roles-and-policies-for-deployment) to configure something more appropriate.
    
# Development

Any .py file placed in `veracodenotifier/actions` or `veracodenotifier/notifications` will be loaded as an action or notification plugin.

Actions are changes in the Veracode platform that results in an event stream being generated. To create a new one, add a .py file to the `actions` folder containing a class that inherits from `veracodenotifier.helpers.base_action.Action`. This class must implement the `pre_action()`, `action()`, and `post_action()` methods, which will each be passed an instance of `VeracodeAPI` as found in `veracodenotifier.helpers.api`. The `action()` method must return a list of events, each event being a dictionary with a `message` key/value pair.

Notifications take an event and post the event as a message to a service of your choice. To create a new one, add a .py file to the `notifications` folder containing a class that inherits from `veracodenotifier.helpers.base_notification.Notification`. This class must implement the `send_notification()` method which takes an event and does something with it.
