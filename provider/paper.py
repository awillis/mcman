from typing import List
from base import Provider

import jmespath
import logging

class Paper(Provider):
    """
    Fetches minecraft server jars from PaperMC
    """
    API_ENDPOINT = "https://api.papermc.io/v2/projects/paper"

    def list_versions(self) -> List[str]:
        project_info = self.fetch_url(self.API_ENDPOINT).json()
        return jmespath.search("versions", project_info)

    def fetch(self, version: str):
        version_info = self.fetch_url(f"{self.API_ENDPOINT}/versions/{version}").json()
        latest = jmespath.search("builds[-1]", version_info)
        build_info = self.fetch_url(f"{self.API_ENDPOINT}/versions/{version}/builds/{latest}").json()
        application = jmespath.search("downloads.application", build_info)

        if "name" in application:
            url = f"{self.API_ENDPOINT}/versions/{version}/builds/{latest}/downloads/{application.name}"
            filename = self.prepare_filepath(version)
            self.fetch_file(url, filename)
        else:
            logging.error("unable to determine application name")
