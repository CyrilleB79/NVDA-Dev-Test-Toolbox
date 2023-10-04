# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from logHandler import log
import addonHandler
import config
import ui
import core
import shellapi
from winUser import SW_SHOWNORMAL

from .compa import appDir

import os
import sys
import threading
import subprocess
import ctypes
import inspect
import re
try:
	import importlib
except ImportError:
	# NVDA2019.2: although importlib seems documented for Python2, it is not present in Python's version of NVDA.
	# We will use __import__ instead as done in NVDA source code.
	pass
# For Python 2.7, open the open of Python 3, allowing to specify encoding.
from io import open

if sys.version_info.major >= 3:
	# Python 3+
	stringTypes = (str,)
else:
	# Python 2
	stringTypes = (str, unicode)  # noqa F821

addonHandler.initTranslation()


class FileOpenerError(Exception):
	"""An error that can be raised in the Python console and caught to report a message in the log reader.
	"""

	# Possible error types
	ET_CONFIG_NO_NVDA_SOURCE_PATH_DEFINED = 1
	ET_CONFIG_NO_OPENER_DEFINED = 2
	ET_CONFIG_OPENER_DEFINITION_WRONG_FORMAT = 3
	ET_CONFIG_EDITOR_NOT_FOUND = 4
	ET_OBJECT_NOT_FOUND = 10
	ET_FILE_NOT_FOUND = 11

	MESSAGE_DIC = {
		ET_CONFIG_NO_NVDA_SOURCE_PATH_DEFINED: (
			'No NVDA source path defined in configuration',
			# Translators: A message reported when trying to open a source file.
			_('No path configured for NVDA sources; please see documentation to configure it.'),
		),
		ET_CONFIG_NO_OPENER_DEFINED: (
			'No open file command defined in configuration',
			# Translators: A message reported when trying to open a source file.
			_('No open file command configured; please see documentation to configure it.'),
		),
		ET_CONFIG_OPENER_DEFINITION_WRONG_FORMAT: (
			'Wrong format for the open file command defined in configuration',
			_(
				# Translators: A message reported when trying to open a source file.
				'Wrong format for the open file command in the configuration; '
				'please see documentation to configure it.'
			),
		),
		ET_CONFIG_EDITOR_NOT_FOUND: (
			'Editor not found {}',
			# Translators: A message reported when trying to open a source file.
			_('Editor not found at {}; please check your configuration.'),
		),
		ET_OBJECT_NOT_FOUND: (
			'Object not found: {}',
			# Translators: A message reported when trying to open a source file.
			_('Object not found: {}'),
		),
		ET_FILE_NOT_FOUND: (
			'File not found {}',
			# Translators: A message reported when trying to open a source file.
			_('File not found: {}'),
		)
	}

	def __init__(self, errorType, value=None):
		self.errorType = errorType
		self.value = value

	def __str__(self):
		msg = self.MESSAGE_DIC[self.errorType][0]
		if self.value is not None:
			msg = msg.format(self.value)
		return '{msg} [ErrorType: {et}]'.format(
			msg=msg,
			et=self.errorType,
		)

	def getUserFriendlyMessage(self):
		msg = self.MESSAGE_DIC[self.errorType][1]
		if self.value is not None:
			msg = msg.format(self.value)
		return msg


class SourceFileOpener(threading.Thread):

	def __init__(self, path, line, *args, **kw):
		super(SourceFileOpener, self).__init__(*args, **kw)
		self.path = path
		self.line = line
		self.opener = config.conf['ndtt']['sourceFileOpener']
		if not self.opener.strip():
			raise FileOpenerError(FileOpenerError.ET_CONFIG_NO_OPENER_DEFINED)
		try:
			self.cmd = self.opener.format(path=self.path, line=self.line)
		except KeyError:
			raise FileOpenerError(FileOpenerError.ET_CONFIG_OPENER_DEFINITION_WRONG_FORMAT, self.opener)
		cmdLineItems = win_CommandLineToArgvW(self.cmd)
		self.editor = cmdLineItems[0]
		self.parameters = subprocess.list2cmdline(cmdLineItems[1:])
		if not os.path.isfile(self.editor):
			raise FileOpenerError(FileOpenerError.ET_CONFIG_EDITOR_NOT_FOUND, self.editor)

	def run(self):
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


def openSourceFile(path, line=1):
	if not os.path.isfile(path):
		raise FileOpenerError(FileOpenerError.ET_FILE_NOT_FOUND, path)
	SourceFileOpener(path, line).start()


class CodeLocator(object):
	def __init__(self, obj):
		self.obj = obj

	def getCodeLocation(self):
		"""Returns the file path and the line of the source code that has been used to construct the object of
		this locator. If no information can be found on the object, returns None.
		"""

		if inspect.isfunction(self.obj) or inspect.ismethod(self.obj):
			loc = self.getCodeLocationForFunctionOrMethod()
		elif inspect.isclass(self.obj):
			loc = self.getCodeLocationForClass()
		elif inspect.ismodule(self.obj):
			loc = self.getCodeLocationForModule()
		else:
			loc = self.getObjectCodePath()
		path, line = loc
		return path, line

	def getCodeLocationForFunctionOrMethod(self):
		try:
			# When using @functools.wraps target the original function decorated by the wrapper
			# rather than the function defined in the wrapper's code.
			self.obj = self.obj.__wrapped__
		except AttributeError:
			pass
		path = inspect.getsourcefile(self.obj)
		path = self.convertToSourcePath(path)
		line = self.obj.__code__.co_firstlineno
		return path, line

	def getCodeLocationForClass(self):
		path = self.getModuleOrClassCodePath()
		if not path:
			return None
		path = self.convertToSourcePath(path)
		try:
			className = self.obj.__qualname__
		except AttributeError:  # Python 2: __name__ instead of __qualname__
			className = self.obj.__name__
		className = className.split('.')[-1]
		line = self.findClassDefinitionLine(className, path)
		return path, line

	def getCodeLocationForModule(self):
		path = self.getModuleOrClassCodePath()
		if not path:
			return None
		path = self.convertToSourcePath(path)
		line = 1
		return path, line

	@staticmethod
	def convertToSourcePath(path):
		path = re.sub(r'^.+\\library.zip\\(.+.py)[co]?$', r'\1', path)
		if ':' not in path:
			nvdaPath = getNvdaCodePath()
			return os.path.join(nvdaPath, path)
		else:
			return path

	@staticmethod
	def findClassDefinitionLine(className, path):
		reClassLine = r'\s*class\s+{}'.format(className)
		reComp = re.compile(reClassLine)
		with open(path, 'r', encoding='utf8') as f:
			for (n, l) in enumerate(f):
				if reComp.match(l):
					return n + 1
			log.warning('Class definition line not found:\n{}'.format(reClassLine))
			return 1

	def getModuleOrClassCodePath(self):
		if inspect.ismodule(self.obj):
			modName = self.obj.__name__
		elif inspect.isclass(self.obj):
			modName = self.obj.__module__
		else:
			raise RuntimeError('Unexpected object type: {}'.format(type(self.obj)))
		if modName == '__main__':
			return 'nvda.pyw'
		try:
			src = inspect.getsourcefile(self.obj)
			if src:
				return src
		except TypeError:
			# inspect.getsourcefile raises TypeError for builtin classes.
			pass
		raise FileOpenerError(FileOpenerError.ET_OBJECT_NOT_FOUND, modName)

	def getObjectCodePath(self):
		return CodeLocator(self.obj.__class__).getCodeLocationForClass()


def openObject(objPath):
	try:
		importFunction = importlib.import_module
	except NameError:
		# NVDA 2019.2.1: Although importlib is documented for Python 2, it is not present in NVDA's Python
		# for this version. Thus use __import__ instead, as done in core code.
		importFunction = __import__
	tokens = objPath.split('.')
	for iToken in range(len(tokens)):
		modName = '.'.join(tokens[0:iToken + 1])
		objName = '.'.join(tokens[iToken + 1:])
		try:
			mod = importFunction(modName)
		# Python 2 raise ImportError for non-existing modules; Python 3 raises ModuleNotFoundError instead.
		# Since ModuleNotFoundError inherits from ImportError we filter on ImportError
		except ImportError:
			continue
		try:
			openObjectInModule(objName, mod)
			return
		except FileOpenerError:
			continue
	else:
		raise FileOpenerError(FileOpenerError.ET_OBJECT_NOT_FOUND, objPath)


def openObjectInModule(objName, mod):
	tokens = objName.split('.')
	obj = mod
	try:
		for attr in tokens:
			obj = getattr(obj, attr)
	except AttributeError:
		raise FileOpenerError(FileOpenerError.ET_OBJECT_NOT_FOUND, mod.__name__ + '.' + objName)
	openCodeFile(obj)


def openCodeFile(obj):
	"""Opens the source code defining the object passed as parameter.
	The parameter may be:
	- a Python object
		`openCodeFile(gui.settingsDialogs.SettingsPanel)`
	- a string containing the name of a Python object
		`openCodeFile("gui.settingsDialogs.SettingsPanel")`
	"""

	if isinstance(obj, stringTypes):
		openObject(obj)
		return
	path, line = CodeLocator(obj).getCodeLocation()
	openSourceFile(path, line)


def getNvdaCodePath():
	if getattr(sys, 'frozen', None):
		# NVDA executable
		nvdaSourcePath = config.conf['ndtt']['nvdaSourcePath'].strip()
		if nvdaSourcePath:
			return nvdaSourcePath
		else:
			raise FileOpenerError(FileOpenerError.ET_CONFIG_NO_NVDA_SOURCE_PATH_DEFINED)
	else:
		# NVDA running from source
		return appDir


def win_CommandLineToArgvW(cmd):
	nargs = ctypes.c_int()
	ctypes.windll.shell32.CommandLineToArgvW.restype = ctypes.POINTER(ctypes.c_wchar_p)
	lpargs = ctypes.windll.shell32.CommandLineToArgvW(cmd, ctypes.byref(nargs))
	args = [lpargs[i] for i in range(nargs.value)]
	if ctypes.windll.kernel32.LocalFree(lpargs):
		raise AssertionError
	return args


def testCodeFinder():
	""" A test function for the `CodeLocator` class.
	To execute it, open NVDA's Python console and run the following command:
	globalPlugins.ndtt.GlobalPlugin.testCodeFinder()
	"""

	nvdaCodePath = getNvdaCodePath()
	if not nvdaCodePath:
		return
	import api
	from gui import logViewer
	import appModules
	from appModules import excel as appModules_excel
	import globalCommands
	import __main__

	objList = [
		# Module
		(api, nvdaCodePath + r'\api.py', 1),
		# Main module
		(__main__, nvdaCodePath + r'\nvda.pyw', 1),
		# Module-level function
		(api.getFocusObject, nvdaCodePath + r'\api.py', 69),
		# Module-level function with wrapper
		(logViewer.activate, nvdaCodePath + r'\gui\logViewer.py', 108),
		# Class definition
		(globalCommands.GlobalCommands, nvdaCodePath + r'\globalCommands.py', 99),
		# Class definition in main module
		(__main__.NoConsoleOptionParser, nvdaCodePath + r'\nvda.pyw', 93),
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
		file1, line1 = CodeLocator(obj).getCodeLocation()
		if file.lower() == file1.lower() and (line != 1) == (line1 != 1):
			log.debug('Checked {} successfully.'.format(obj))
		else:
			log.error('FileRef: {} - {}\nFileGCP: {} - {}'.format(file, line, file1, line1))
			hasErrorOccurred = True
	if hasErrorOccurred:
		msg = 'Test failed; see the log for details'
	else:
		msg = 'Test successful'
	core.callLater(0, lambda: ui.message(msg))
