import os
from veracodenotifier.helpers import tools
from veracodenotifier.helpers.base_action import Action


class NewApplicationProfileAction(Action):
    def __init__(self):
        self.application_profiles_file = os.path.join(os.getcwd(), "saved_data", os.path.basename(__file__)[:-3], "application_profiles.xml")
        self.saved_application_profiles = []
        self.latest_application_profiles_xml = b""
        self.events = []

    def pre_action(self, api):
        if os.path.exists(self.application_profiles_file):
            with open(self.application_profiles_file, 'rb') as f:
                self.saved_application_profiles = tools.parse_and_remove_xml_namespaces(f.read()).findall("app")

    def action(self, api):
        self.events = []
        self.latest_application_profiles_xml = api.get_app_list()
        latest_application_profiles = tools.parse_and_remove_xml_namespaces(self.latest_application_profiles_xml).findall("app")
        application_profiles_created = tools.diff(latest_application_profiles, self.saved_application_profiles, "app_name")
        for app in application_profiles_created:
            self.events.append({"type": "create", "message": "Application profile created: " + app.attrib["app_name"]})
        return self.events

    def post_action(self, api):
        save_directory = os.path.join(os.getcwd(), "saved_data", os.path.basename(__file__))[:-3]
        if not os.path.exists(save_directory):
            os.makedirs(save_directory)
        with open(os.path.join(save_directory, "application_profiles.xml"), 'wb') as f:
            f.write(self.latest_application_profiles_xml)
