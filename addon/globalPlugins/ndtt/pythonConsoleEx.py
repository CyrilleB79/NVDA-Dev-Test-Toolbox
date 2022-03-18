# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2022 Cyrille Bougot

"""Provides an extension of NVDA's Python console.
"""

from .fileOpener import openSourceFile, getNvdaCodePath

import globalPluginHandler
import pythonConsole
from logHandler import log

import os
import re
import inspect


def openCodeFile(obj):
	"""Opens the source code that has been used to construct the object passed as parameter.
	"""
	
	path = None
	line = None
	try:
		# For functions and methods
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
			try:
				# For classes
				className = obj.__qualname__
			except AttributeError:
				# For objects
				className = obj.__class__.__qualname__
			className = className.split('.')[-1]
	if not path:
		print('Unsupported object type: {}'.format(type(obj)))
		return
	if path.endswith('.pyc') or path.endswith('.pyo'):
		path = path[:-1]
	if ':' not in path:
		nvdaPath = getNvdaCodePath()
		path = os.path.join(nvdaPath, path)
	if not line:
		reClassLine = re.compile(r'\s*class\s+{}'.format(className))
		with open(path, 'r') as f:
			for (n, l) in enumerate(f):
				if reClassLine.match(l):
					line = n + 1
					break
			else:
				log.warning('Class definition line not found')
				line = 1
	openSourceFile(path, line)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if pythonConsole.consoleUI:
			pythonConsole.consoleUI.console.namespace.update({'openCodeFile': openCodeFile})
		else:
			oldInitialize = pythonConsole.initialize
			def newInitialize():
				oldInitialize()
				pythonConsole.consoleUI.console.namespace.update({'openCodeFile': openCodeFile})
				pythonConsole.initialize = oldInitialize
			pythonConsole.initialize = newInitialize

	def terminate(self, *args, **kwargs):
		try:
			del pythonConsole.consoleUI.console.namespace['openCodeFile']
		except (AttributeError, KeyError):
			pass
		super(GlobalPlugin, self).terminate(*args, **kwargs)
