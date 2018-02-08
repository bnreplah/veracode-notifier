import os
from veracodenotifier.helpers import tools
from veracodenotifier.helpers.base_action import Action


class NewBuildsAction(Action):
    def __init__(self):
        self.file_name = os.path.basename(__file__)[:-3] + "/application_builds.xml"
        self.saved_application_builds = []
        self.latest_application_builds_xml = b""
        self.last_run_date = "01/01/1970"

    def pre_action(self, api, s3_client, s3_bucket):
        try:
            saved_application_builds_object = s3_client.get_object(Bucket=s3_bucket, Key=self.file_name)
            saved_application_builds_xml = saved_application_builds_object["Body"].read()
            self.last_run_date = saved_application_builds_object["LastModified"].strftime('%m/%d/%Y')
            self.saved_application_builds = tools.parse_and_remove_xml_namespaces(saved_application_builds_xml).findall("application/build")
            return True
        except s3_client.exceptions.NoSuchKey:
            self.latest_application_builds_xml = api.get_app_builds(self.last_run_date)
            return False

    def action(self, api, s3_client, s3_bucket):
        events = []
        self.latest_application_builds_xml = api.get_app_builds(self.last_run_date)
        latest_application_builds_list = tools.parse_and_remove_xml_namespaces(self.latest_application_builds_xml)
        latest_application_builds = latest_application_builds_list.findall("application/build")
        application_builds_created = tools.diff(latest_application_builds, self.saved_application_builds, "build_id")
        for build in application_builds_created:
            app = latest_application_builds_list.find('.//build[@build_id="' + build.attrib["build_id"] + '"]...')
            title = app.attrib["app_name"] + " build created"
            text = "\nName: " + build.attrib["version"] + \
                   "\nBuild ID: " + build.attrib["build_id"] + \
                   "\nSubmitter: " + build.attrib["submitter"] + \
                   "\nStatus: " + build.find("analysis_unit").attrib["status"]
            message = {
                "simple": title + text,
                "title": title,
                "text": text
            }
            events.append({"type": "create", "message": message})
        return events

    def post_action(self, api, s3_client, s3_bucket):
        s3_client.put_object(Bucket=s3_bucket, Key=self.file_name, Body=self.latest_application_builds_xml)
