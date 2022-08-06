# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 Cyrille Bougot

"""Provides an extension of NVDA's Python console.
"""

import os
import sys
import re
import inspect

import globalPluginHandler
import pythonConsole
from logHandler import log
from scriptHandler import script
import addonHandler
import globalVars
from logHandler import log

from .fileOpener import openSourceFile, getNvdaCodePath

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

def getCodeFileAndLine(obj):
	"""Opens the source code that has been used to construct the object passed as parameter.
	"""
	
	path = None
	line = None
	try:
		# For functions and methods
		try:
			# When using @functools.wraps target the original function decorated by the wrapper
			# rather than the function defined in the wrapper's code.
			obj = obj.__wrapped__
		except AttributeError:
			pass
		path = obj.__code__.co_filename
	except AttributeError:
		pass
	else:
		line = obj.__code__.co_firstlineno
	if not path:
		try:
			# For classes and modules
			path = inspect.getabsfile(obj)
		except TypeError:
			try:
				# For objects
				path = inspect.getabsfile(obj.__class__)
			except TypeError:
				pass
		if path:
			path = re.sub(r'^.+\\library.zip\\(.+.py)[co]?$', r'\1', path)
		if hasattr(obj, '__package__'):
			# For module
			line = 1
		else:
			# For classes, objects
			if not inspect.isclass(obj):
				# For obj, take its class
				obj = obj.__class__
			try:
				className = obj.__qualname__
			except AttributeError:
			# Python 2: __name__ instead of __qualname__
				className = obj.__class__.__name__
			className = className.split('.')[-1]
	if not path:
		return None
	if path.endswith('.pyc') or path.endswith('.pyo'):
		path = path[:-1]
	if ':' not in path:
		nvdaPath = getNvdaCodePath()
		path = os.path.join(nvdaPath, path)
	if not line:
		reClassLine = r'\s*class\s+{}'.format(className)
		reComp = re.compile(reClassLine)
		with open(path, 'r', encoding='utf8') as f:
			for (n, l) in enumerate(f):
				if reComp.match(l):
					line = n + 1
					break
			else:
				log.warning('Class definition line not found:\n{}'.format(reClassLine))
				line = 1
	return path, line
	
def openCodeFile(obj):
	res = getCodeFileAndLine(obj)
	if res is None:
		log.error('Unsupported object type: {}'.format(type(obj)))
		return
	path, line = res
	openSourceFile(path, line)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

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

	@staticmethod
	def testCodeFinder():
		""" A test function for the `getCodeFileAndLine` function.
		To execute it, open NVDA's Python console and run the following command:
		globalPlugins.ndtt.GlobalPlugin.testCodeFinder()
		"""
		
		nvdaCodePath = getNvdaCodePath()
		if not nvdaCodePath:
			return
		import config
		import api
		from gui import logViewer
		import appModules
		from appModules import excel as appModules_excel
		import globalCommands
		objList = [
			# Module
			(api, nvdaCodePath + r'\api.py', 1),
			# Module-level function
			(api.getFocusObject, nvdaCodePath + r'\api.py', 69),
			# Module-level function with wrapper
			(logViewer.activate, nvdaCodePath + r'\gui\logViewer.py', 108),
			# Class definition
			(globalCommands.GlobalCommands, nvdaCodePath + r'\globalCommands.py', 99),
			# Definition of the class of an object
			(globalCommands.commands, nvdaCodePath + r'\globalCommands.py', 99),
			# Method definition in a class
			(globalCommands.GlobalCommands.script_cycleAudioDuckingMode, nvdaCodePath + r'\globalCommands.py', 103),
			# Method definition of an object
			(globalCommands.commands.script_cycleAudioDuckingMode, nvdaCodePath + r'\globalCommands.py', 103),
			# Package
			(appModules, nvdaCodePath + r'\appModules\__init__.py', 1),
			# Module in subfolder
			(appModules_excel, nvdaCodePath + r'\appModules\excel.py', 1),
		]
		hasErrorOccurred = False
		for obj, file, line in objList:
			file1, line1 = getCodeFileAndLine(obj)
			if file.lower() == file1.lower() and (line != 1) == (line1 != 1):
				pass
			else:
				log.error('FileRef: {} - {}\nFileGCP: {} - {}'.format(file, line, file1, line1))
				hasErrorOccurred = True
		import ui
		import core
		if hasErrorOccurred:
			msg = 'Test failed; see the log for details'
		else:
			msg = 'Test successful'
		core.callLater(0, lambda: ui.message(msg))
	
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
			sys.stdout, sys.stderr = stdout, stderr
		else:
			log.debug('No console startup file found for path {}'.format(startupFilePath))
