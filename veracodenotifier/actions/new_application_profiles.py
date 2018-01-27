import os
from veracodenotifier.helpers import tools
from veracodenotifier.helpers.base_action import Action


class NewApplicationProfilesAction(Action):
    def __init__(self):
        self.save_directory = os.path.join(os.getcwd(), "saved_data", os.path.basename(__file__))[:-3]
        self.saved_application_profiles_file = os.path.join(self.save_directory, "application_profiles.xml")
        self.saved_application_profiles = []
        self.latest_application_profiles_xml = b""

    def pre_action(self, api):
        if os.path.exists(self.saved_application_profiles_file):
            with open(self.saved_application_profiles_file, 'rb') as f:
                self.saved_application_profiles = tools.parse_and_remove_xml_namespaces(f.read()).findall("app")

    def action(self, api):
        events = []
        self.latest_application_profiles_xml = api.get_app_list()
        latest_application_profiles = tools.parse_and_remove_xml_namespaces(self.latest_application_profiles_xml).findall("app")
        application_profiles_created = tools.diff(latest_application_profiles, self.saved_application_profiles, "app_id")
        for app in application_profiles_created:
            events.append({"type": "create", "message": "Application profile created: " + app.attrib["app_name"]})
        return events

    def post_action(self, api):
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        with open(self.saved_application_profiles_file, 'wb') as f:
            f.write(self.latest_application_profiles_xml)
