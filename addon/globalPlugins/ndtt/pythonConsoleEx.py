# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2023 Cyrille Bougot

"""Provides an extension of NVDA's Python console.
"""

import os
import sys

import globalPluginHandler
import pythonConsole
import addonHandler
import globalVars
from logHandler import log

from .fileOpener import openCodeFile, testCodeFinder


ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Store here the symbol to have it available in globalPlugins.ndtt.GlobalPlugin.
	testCodeFinder = testCodeFinder

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if pythonConsole.consoleUI:
			self.pythonConsolePostInitialize()
		else:
			oldInitialize = pythonConsole.initialize

			def newInitialize():
				oldInitialize()
				self.pythonConsolePostInitialize()
				pythonConsole.initialize = oldInitialize
			pythonConsole.initialize = newInitialize

	def terminate(self, *args, **kwargs):
		try:
			del pythonConsole.consoleUI.console.namespace['openCodeFile']
		except (AttributeError, KeyError):
			pass
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	def pythonConsolePostInitialize(self):
		pythonConsole.consoleUI.console.namespace.update({'openCodeFile': openCodeFile})
		ndttPath = os.path.join(globalVars.appArgs.configPath, 'ndtt')
		startupFileName = 'consoleStartup.py'
		startupFilePath = os.path.join(ndttPath, startupFileName)
		if os.path.isfile(startupFilePath):
			log.debug('Loading console startupFile {}'.format(startupFilePath))
			stdout, stderr = sys.stdout, sys.stderr
			sys.stdout = sys.stderr = pythonConsole.consoleUI.console
			print('### Executing console startup script: {}'.format(startupFilePath))
			with open(startupFilePath, 'r') as sf:
				pythonConsole.consoleUI.console.runsource(source=sf.read(), filename=startupFileName, symbol='exec')
			print('### Console startup script executed.')
			pythonConsole.consoleUI.outputPositions.append(pythonConsole.consoleUI.outputCtrl.GetInsertionPoint())
			sys.stdout, sys.stderr = stdout, stderr
		else:
			log.debugWarning('No console startup file found for path {}'.format(startupFilePath))
