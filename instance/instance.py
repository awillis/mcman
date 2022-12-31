import logging

from provider import Provider
from constant import INSTANCE_DIR, DEFAULT_ENVIRONMENT
from pathlib import Path

import os
import shutil
import pystemd

class Instance:
	"""
	Manages minecraft server instances.
	"""
	def __init__(self, name: str, provider: Provider, version: str):

		# perform regex check on name, should be all lower with underscore
		self.name = name
		self.provider = provider
		self.version = version

	def __repr__(self) -> str:
		return f"{type(self).__name__}(name={self.name}, provider={self.provider.name()}, version={self.version})"

	def build(self):

		if not self.provider.exists(self.version):
			self.provider.fetch(self.version)

		# create instance directory by name
		instance_dir = Path(INSTANCE_DIR).joinpath(self.name)
		instance_dir.mkdir(parents=True, exist_ok=True)

		# add symlink from instance directory server.jar to provider
		try:
			os.symlink(
				self.provider.path(self.version),
				instance_dir.joinpath("server.jar")
			)
		except Exception as err:
			logging.error(err)
			exit(1)

		# copy default environment options to instance
		instance_env = instance_dir.joinpath("environment")
		try:
			shutil.copy(DEFAULT_ENVIRONMENT, instance_env)
		except Exception as err:
			logging.error(err)
			exit(1)

		# determine service socket and update firewall and selinux mapping
		# place service ip and port in env file
		# mojang instances need eula=true
		# place safe server.properties file in instance dir

	def start(self):
		pass
		# use pystemd to start systemd service