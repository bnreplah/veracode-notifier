import os
from helpers import tools
from helpers.base_action import Action


class DeletedApplicationProfilesAction(Action):
    def __init__(self):
        self.file_name = os.path.basename(__file__)[:-3] + "/application_profiles.xml"
        self.saved_application_profiles = []
        self.latest_application_profiles_xml = b""

    def pre_action(self, api, s3client, s3bucket):
        try:
            saved_application_profiles_xml = s3client.get_object(Bucket=s3bucket, Key=self.file_name)["Body"].read()
            self.saved_application_profiles = tools.parse_and_remove_xml_namespaces(saved_application_profiles_xml).findall("app")
        except s3client.exceptions.NoSuchKey:
            pass

    def action(self, api, s3client, s3bucket):
        events = []
        self.latest_application_profiles_xml = api.get_app_list()
        latest_application_profiles = tools.parse_and_remove_xml_namespaces(self.latest_application_profiles_xml).findall("app")
        application_profiles_deleted = tools.diff(self.saved_application_profiles, latest_application_profiles, "app_id")
        for app in application_profiles_deleted:
            message = {
                "simple": "Application Profile Deleted." +
                          "\nName: " + app.attrib["app_name"],
                "title": "Application Profile Deleted",
                "text": "Name: " + app.attrib["app_name"]
            }
            events.append({"type": "delete", "message": message})
        return events

    def post_action(self, api, s3client, s3bucket):
        s3client.put_object(Bucket=s3bucket, Key=self.file_name, Body=self.latest_application_profiles_xml)
