from typing import List
from hashlib import sha1, sha256, md5
from pathlib import Path
from requests import get, Response
from constant import PROVIDER_DIR, TIMEOUT, CHUNK_SIZE

import os
import logging


class Provider:
	"""
	Represents a minecraft server provider.
	List available versions of the server.jar.
	Set up a systemd unit instance of the server and version
	"""

	def list_versions(self) -> List[str]:
		"""

		:return:
		"""
		raise NotImplementedError

	def fetch(self, version: str):
		"""
		Fetches server.jar from provider api endpoint
		:param version: Minecraft server version
		:return:
		"""
		raise NotImplementedError

	@classmethod
	def _format_filename(cls, version: str) -> Path:
		return Path(PROVIDER_DIR).joinpath(cls.__name__.lower()).joinpath(version).joinpath("server.jar")

	@classmethod
	def exists(cls, version: str) -> bool:
		return cls._format_filename(version).exists()

	@classmethod
	def prepare_filepath(cls, version: str) -> str:
		filename = cls._format_filename(version)
		filename.parent.mkdir(parents=True, exist_ok=True)
		return filename.as_posix()

	@staticmethod
	def fetch_url(url: str) -> Response:
		response = Response()
		try:
			response = get(url, timeout=TIMEOUT)
		except requests.RequestException as err:
			logging.critical(f"unable to retrieve {url}: {err}")
		return response

	@staticmethod
	def fetch_file(url, filename: str) -> (int, dict):
		sha1sum = sha1()
		sha256sum = sha256()
		md5sum = md5()
		try:
			with get(url, stream=true, timeout=TIMEOUT) as r:
				r.raise_for_status()
				with open(filename, mode="wb") as f:
					for chunk in r.iter_content(chunk_size=CHUNK_SIZE):
						f.write(chunk)
						sha1sum.update(chunk)
						sha256sum.update(chunk)
						md5sum.update(chunk)
		except requests.RequestException as err:
			logging.critical(f"unable to retrieve {url}: {err}")

		checksums = {
			"sha1": sha1sum.digest(),
			"sha256": sha256sum.digest(),
			"md5": md5sum.digest()
		}

		return os.stat(filename).st_size, checksums
