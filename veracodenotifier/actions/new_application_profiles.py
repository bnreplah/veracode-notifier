import os
from veracodenotifier.helpers import tools
from veracodenotifier.helpers.base_action import Action


class NewApplicationProfilesAction(Action):
    def __init__(self):
        self.file_name = os.path.basename(__file__)[:-3] + "/application_profiles.xml"
        self.saved_application_profiles = []
        self.latest_application_profiles_xml = b""

    def pre_action(self, api, s3client, s3bucket):
        try:
            saved_application_profiles_xml = s3client.get_object(Bucket=s3bucket, Key=self.file_name)["Body"].read()
            self.saved_application_profiles = tools.parse_and_remove_xml_namespaces(saved_application_profiles_xml).findall("app")
            return True
        except s3client.exceptions.NoSuchKey:
            self.latest_application_profiles_xml = api.get_app_list()
            return False

    def action(self, api, s3client, s3bucket):
        events = []
        self.latest_application_profiles_xml = api.get_app_list()
        latest_application_profiles = tools.parse_and_remove_xml_namespaces(self.latest_application_profiles_xml).findall("app")
        application_profiles_created = tools.diff(latest_application_profiles, self.saved_application_profiles, "app_id")
        for app in application_profiles_created:
            message = {
                "simple": "Application profile created" +
                          "\nName: " + app.attrib["app_name"] +
                          "\nApp ID: " + app.attrib["app_id"],
                "title": "Application profile created",
                "text": "Name: " + app.attrib["app_name"] +
                        "\nApp ID: " + app.attrib["app_id"]
            }
            events.append({"type": "create", "message": message})
        return events

    def post_action(self, api, s3client, s3bucket):
        s3client.put_object(Bucket=s3bucket, Key=self.file_name, Body=self.latest_application_profiles_xml)
