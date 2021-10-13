# -*- coding: UTF-8 -*-
# NVDA Debug & Test Tools add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

import addonHandler
from logHandler import log
import config
import ui

import os
import sys
import shlex
import threading
import subprocess

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


class ConfigError(Exception): pass

class SourceFileOpener(threading.Thread):

	def __init__(self, path, line, *args, **kw):
		super().__init__(*args, **kw)
		self.path = path
		self.line = line
		self.opener = config.conf['ndtt']['sourceFileOpener']
		if not self.opener.strip():
			raise ConfigError('NoOpenerDefined')
		self.cmd = self.opener.format(path=self.path, line=self.line)
		if not os.path.isfile(shlex.split(self.cmd)[0]):
			raise ConfigError('NoEditorFileFound')		

	def run(self):
		try:
			ret = subprocess.run(
				self.cmd,
				check=True,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
			)
		except Exception:
			log.debug('Error when executing the following command:\n{cmd}'.format(cmd=self.cmd))
			raise

def openSourceFile(path, line):
	if not os.path.isfile(path):
		ui.message(_('File not found: {file}'.format(file=path)))
		return
	try:
		SourceFileOpener(path, line).start()
	except ConfigError as e:
		ui.message(_('Configuration error: {err}. Please see the documentation to configure this feature.').format(err=e.args[0]))
		raise e


def getNvdaCodePath():
	if getattr(sys,'frozen',None):
		# NVDA executable
		nvdaSourcePath = config.conf['ndtt']['nvdaSourcePath'].strip()
		if nvdaSourcePath:
			return nvdaSourcePath
		else:
			ui.message(_('No path configured for NVDA sources; please see documentation to configure it.'))
			return None
	else:
		# NVDA running from source
		return appDir
