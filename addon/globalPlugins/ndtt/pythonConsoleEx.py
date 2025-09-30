# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022-2025 Cyrille Bougot

"""Provides an extension of NVDA's Python console.
"""

import os
import sys
# For Python 2.7, use the open of Python 3, allowing to specify encoding.
from io import open

import globalPluginHandler
import pythonConsole
import addonHandler
import globalVars
import config
from logHandler import log

from .fileOpener import openCodeFile, testCodeFinder


ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


NDTT_PATH = os.path.join(globalVars.appArgs.configPath, 'ndtt')
CONSOLE_STARTUP_FILE_NAME = "consoleStartup.py"
CONSOLE_HISTORY_FILE_NAME = ".pythonConsoleHistory"

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	# Store here the symbol to have it available in globalPlugins.ndtt.GlobalPlugin.
	testCodeFinder = testCodeFinder

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.consoleStartupFilePath = os.path.join(NDTT_PATH, CONSOLE_STARTUP_FILE_NAME)
		self.consoleHistoryFilePath = os.path.join(NDTT_PATH, CONSOLE_HISTORY_FILE_NAME)
		if pythonConsole.consoleUI:
			pass  # Do nothing: the Python console startup script will already have been executed.
		else:
			oldInitialize = pythonConsole.initialize

			def newInitialize():
				oldInitialize()
				self.pythonConsolePostInitialize()
				pythonConsole.initialize = oldInitialize
			if not getattr(pythonConsole.initialize, "_pythonConsolePostInitializePatch", False):
				pythonConsole.initialize = newInitialize
				pythonConsole.initialize._pythonConsolePostInitializePatch = True

	def terminate(self, *args, **kwargs):
		self.saveInputHistory()
		try:
			del pythonConsole.consoleUI.console.namespace['openCodeFile']
		except (AttributeError, KeyError):
			pass
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	def pythonConsolePostInitialize(self, alreadyOpen=False):
		pythonConsole.consoleUI.console.namespace.update({'openCodeFile': openCodeFile})
		self.loadStartupFile()
		self.loadInputHistory(alreadyOpen=alreadyOpen)
	
	def loadStartupFile(self):
		if os.path.isfile(self.consoleStartupFilePath):
			log.debug('Loading console startupFile {}'.format(CONSOLE_STARTUP_FILE_NAME))
			stdout, stderr = sys.stdout, sys.stderr
			sys.stdout = sys.stderr = pythonConsole.consoleUI.console
			print('### Executing console startup script: {}'.format(self.consoleStartupFilePath))
			with open(self.consoleStartupFilePath, 'r') as sf:
				pythonConsole.consoleUI.console.runsource(source=sf.read(), filename=CONSOLE_STARTUP_FILE_NAME, symbol='exec')
			print('### Console startup script executed.')
			try:
				# NVDA >= 2021.1
				pythonConsole.consoleUI.outputPositions.append(pythonConsole.consoleUI.outputCtrl.GetInsertionPoint())
			except AttributeError:
				pass
			sys.stdout, sys.stderr = stdout, stderr
		else:
			log.debugWarning('No console startup file found for path {}'.format(self.consoleStartupFilePath))

	def loadInputHistory(self, alreadyOpen):
		if config.conf["ndtt"]["preserveConsoleInputHistory"] and not alreadyOpen:
			try:
				with open(self.consoleHistoryFilePath, 'r', encoding="UTF-8") as f:
					pythonConsole.consoleUI.inputHistory = [l.rstrip("\n") for l in f.readlines()]
			except FileNotFoundError:
				log.debugWarning("No Python console history file found.")
			else:
				pythonConsole.consoleUI.inputHistory.append("")
				pythonConsole.consoleUI.inputHistoryPos = len(pythonConsole.consoleUI.inputHistory) - 1
				log.debug("Python console input history reloaded from {}".format(self.consoleHistoryFilePath))

	def saveInputHistory(self):
		if not config.conf["ndtt"]["preserveConsoleInputHistory"]:
			self.deleteInputHistory()
			return
		if not pythonConsole.consoleUI:
			return
		if int(sys.version[0]) >= 3:
			# Python 3+
			MkDirError = FileExistsError
		else:
			# Python 2
			MkDirError = WindowsError
		try:
			os.mkdir(NDTT_PATH)
		except MkDirError:
			pass
		else:
			log.debug("Created NDTT folder at {}".format(NDTT_PATH))
		with open(self.consoleHistoryFilePath, 'w', encoding="UTF-8") as f:
			for line in pythonConsole.consoleUI.inputHistory[-(config.conf["ndtt"]["consoleInputHistorySize"] + 1):-1]:
				f.write(line + "\n")
		log.debug("Python console input history saved at {}".format(self.consoleHistoryFilePath))
	
	def deleteInputHistory(self):
		try:
			os.remove(self.consoleHistoryFilePath)
		except FileNotFoundError:
			pass
		else:
			log.debug("Python console input history deleted at {}".format(self.consoleHistoryFilePath))
