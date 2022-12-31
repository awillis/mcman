from typing import List
from pathlib import Path
from base import Provider

import os
import json
import jmespath
import logging


class Mojang(Provider):
	"""
	Fetches minecraft server jars from Mojang
	"""
	MANIFEST_URI = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"

	def _load_manifest(self):
		if "manifest" not in self:
			self.manifest = self.fetch_url(self.MANIFEST_URI).json()

	def list_versions(self) -> List[str]:
		self._load_manifest()
		return jmespath.search("versions[?type=='release'].id", self.manifest)

	def fetch(self, version: str):
		self._load_manifest()
		version_url = jmespath.search(f"versions[?id=='{version}']|[0].url", self.manifest)
		version_manifest = self.fetch_url(version_url).json()
		server = jmespath.search(f"downloads.server", version_manifest)
		filename = self.prepare_filepath(version)

		(size, checksums) = self.fetch_file(server.url, filename)
		if server.size != size:
			logging.error(f"file size is {size}, expected {server.size}")

		if server.sha1 != checksums.get("sha1"):
			logging.error(f"sha1 checksum mismatch")

		logging.info("By downloading minecraft server software from Mojang, you agree to the EULA found at https://account.mojang.com/documents/minecraft_eula")