from typing import List
from base import Provider

import jmespath
# TODO: update provider fetch_file to also return md5 hashes


class Purpur(Provider):
    """
    Fetches minecraft server jars from PurpurMC
    """
    API_ENDPOINT = "https://api.purpurmc.org/v2/purpur"

    def list_versions(self) -> List[str]:
        project_info = self.fetch_url(self.API_ENDPOINT).json()
        return jmespath.search("versions", project_info)

    def fetch(self, version: str):
        url = f"{self.API_ENDPOINT}/{version}/latest/download"
        filename = self.prepare_filepath(version)
        self.fetch_file(url, filename)
