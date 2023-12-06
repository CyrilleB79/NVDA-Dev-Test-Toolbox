# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2023 Cyrille Bougot

"""Allow to execute a script when the add-on is loaded.
"""

import os
import sys
import importlib

import globalPluginHandler
import addonHandler
import globalVars
from logHandler import log


ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		ndttPath = os.path.join(globalVars.appArgs.configPath, 'ndtt')
		startupModuleName = 'ndttStartup'
		startupFileName = startupModuleName + '.py'
		startupFilePath = os.path.join(ndttPath, startupFileName)
		if os.path.isfile(startupFilePath):
			log.debug('Importing startup file {}'.format(startupFilePath))
			savedSysPath = sys.path
			sys.path.insert(0, ndttPath)
			try:
				importlib.import_module(startupModuleName)
			except Exception:
				log.error('Error while importing {}'.format(startupFilePath), exc_info=True)
			sys.path = savedSysPath
		else:
			log.debugWarning('No NDTT startup file found for path {}'.format(startupFilePath))
