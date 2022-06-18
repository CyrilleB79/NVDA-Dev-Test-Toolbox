# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

from logHandler import log
import config
import ui
import globalVars

from .compa import appDir

import os
import sys
import shlex
import threading
import subprocess


class ConfigError(Exception): pass

class SourceFileOpener(threading.Thread):

	def __init__(self, path, line, *args, **kw):
		super(SourceFileOpener, self).__init__(*args, **kw)
		self.path = path
		self.line = line
		self.opener = config.conf['ndtt']['sourceFileOpener']
		if not self.opener.strip():
			raise ConfigError('NoOpenerDefined')
		try:
			self.cmd = self.opener.format(path=self.path, line=self.line)
		except KeyError:
			raise ConfigError('BadOpenerDefinition')		
		cmdLineItems = shlex.split(self.cmd)
		self.editor = cmdLineItems[0]
		self.parameters = subprocess.list2cmdline(cmdLineItems[1:])
		if sys.version_info.major < 3:
			self.editor = self.editor.decode("mbcs")
			self.parameters = self.parameters.decode("mbcs")
		if not os.path.isfile(self.editor):
			raise ConfigError('NoEditorFileFound')		

	def run(self):
		try:
			ret = subprocess.call(
				self.cmd,
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
			)
		except Exception:
			log.debug('Error when executing the following command:\n{cmd}'.format(cmd=self.cmd))
			raise

	def run(self):
		import shellapi
		from winUser import SW_SHOWNORMAL
		try:
			shellapi.ShellExecute(
				hwnd=None,
				operation=None,
				file=self.editor,
				parameters=self.parameters,
				directory=None,
				showCmd=SW_SHOWNORMAL
			)
		except Exception:
			log.debug('Error when executing the following command:\n{cmd}'.format(cmd=self.cmd))
			raise


def openSourceFile(path, line):
	if not os.path.isfile(path):
		# Translators: A message reported when trying to open a source file.
		ui.message(_('File not found: {file}'.format(file=path)))
		return
	try:
		SourceFileOpener(path, line).start()
	except ConfigError as e:
		# Translators: A message reported when trying to open a source file.
		ui.message(_('Configuration error: {err}. Please see the documentation to configure this feature.').format(err=e.args[0]))
		raise e


def getNvdaCodePath():
	if getattr(sys,'frozen',None):
		# NVDA executable
		nvdaSourcePath = config.conf['ndtt']['nvdaSourcePath'].strip()
		if nvdaSourcePath:
			return nvdaSourcePath
		else:
			# Translators: A message reported when trying to open a source file.
			ui.message(_('No path configured for NVDA sources; please see documentation to configure it.'))
			return None
	else:
		# NVDA running from source
		return appDir
