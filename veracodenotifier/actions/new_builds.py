import os
from veracodenotifier.helpers import tools
from veracodenotifier.helpers.base_action import Action


class NewBuildsAction(Action):
    def __init__(self):
        self.save_directory = os.path.join(os.getcwd(), "saved_data", os.path.basename(__file__))[:-3]
        self.saved_application_builds_file = os.path.join(self.save_directory, "app_builds.xml")
        self.saved_application_builds = []
        self.latest_application_builds_xml = b""

    def pre_action(self, api):
        if os.path.exists(self.saved_application_builds_file):
            with open(self.saved_application_builds_file, 'rb') as f:
                self.saved_application_builds = tools.parse_and_remove_xml_namespaces(f.read()).findall("application/build")

    def action(self, api):
        events = []
        self.latest_application_builds_xml = api.get_app_builds()
        latest_application_builds = tools.parse_and_remove_xml_namespaces(self.latest_application_builds_xml).findall("application/build")
        application_builds_created = tools.diff(latest_application_builds, self.saved_application_builds, "build_id")
        for build in application_builds_created:
            events.append({"type": "create", "message": "Build created. Submitter: " + build.attrib["submitter"] +
                                                        ", scan name: " + build.attrib["version"] +
                                                        ", results ready: " + build.attrib["results_ready"]})
        return events

    def post_action(self, api):
        if not os.path.exists(self.save_directory):
            os.makedirs(self.save_directory)
        with open(self.saved_application_builds_file, 'wb') as f:
            f.write(self.latest_application_builds_xml)
