import os
from helpers import tools
from helpers.base_action import Action


class NewBuildsAction(Action):
    def __init__(self):
        self.file_name = os.path.basename(__file__)[:-3] + "/application_builds.xml"
        self.saved_application_builds = []
        self.latest_application_builds_xml = b""
        self.last_run_date = "01/01/1970"

    def pre_action(self, api, s3client, s3bucket):
        try:
            saved_application_builds_object = s3client.get_object(Bucket=s3bucket, Key=self.file_name)
            saved_application_builds_xml = saved_application_builds_object["Body"].read()
            self.last_run_date = saved_application_builds_object["LastModified"].strftime('%m/%d/%Y')
            self.saved_application_builds = tools.parse_and_remove_xml_namespaces(saved_application_builds_xml).findall("application/build")
            return True
        except s3client.exceptions.NoSuchKey:
            self.latest_application_builds_xml = api.get_app_builds(self.last_run_date)
            return False

    def action(self, api, s3client, s3bucket):
        events = []
        self.latest_application_builds_xml = api.get_app_builds(self.last_run_date)
        latest_application_builds = tools.parse_and_remove_xml_namespaces(self.latest_application_builds_xml).findall("application/build")
        application_builds_created = tools.diff(latest_application_builds, self.saved_application_builds, "build_id")
        for build in application_builds_created:
            message = {
                "simple": "Build Created." +
                          "\nBuild ID: " + build.attrib["build_id"] +
                          "\nSubmitter: " + build.attrib["submitter"] +
                          "\nScan name: " + build.attrib["version"] +
                          "\nResults ready: " + build.attrib["results_ready"],
                "title": "Build Created",
                "text": "\nBuild ID: " + build.attrib["build_id"] +
                        "\nSubmitter: " + build.attrib["submitter"] +
                        "\nScan name: " + build.attrib["version"] +
                        "\nResults ready: " + build.attrib["results_ready"]
            }
            events.append({"type": "create", "message": message})
        return events

    def post_action(self, api, s3client, s3bucket):
        s3client.put_object(Bucket=s3bucket, Key=self.file_name, Body=self.latest_application_builds_xml)
