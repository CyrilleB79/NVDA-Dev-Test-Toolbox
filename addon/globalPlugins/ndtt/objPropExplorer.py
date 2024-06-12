# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019-2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import inspect
import os
import re
import threading
from html import escape

import globalPluginHandler
import ui
import api
from .compa import controlTypesCompatWrapper as controlTypes
# Import normal controlTypes and not the wrapper only to be used for older versions of NVDA.
import controlTypes as oldControlTypes
from logHandler import log
import addonHandler
import scriptHandler
from scriptHandler import script
import speech

from .securityUtils import secureBrowseableMessage

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Translators: The title of the browseable message displayed by the object propoerty explorer command.
BM_WINDOW_TITLE = _("Object property explorer")


def _createDicControlTypesConstantes(prefix):
	dic = {}
	attributes = dir(oldControlTypes)
	for name in attributes:
		if name.startswith(prefix):
			dic[getattr(oldControlTypes, name)] = name[len(prefix):]
	return dic


_DIC_ROLES = _createDicControlTypesConstantes('ROLE_')
_DIC_STATES = _createDicControlTypesConstantes('STATE_')


def getRoleInfo(o):
	try:
		# NVDA 2021.2+ where controlTypes.Role and controlTypes.State are enums.
		return '{} ({})'.format(o.role.name, o.role.value)
	except AttributeError:
		# Pre-NVDA 2021.2 where controlTypes.ROLE_ and controlTypes.STATE_ are constants
		return '{} ({})'.format(_DIC_ROLES[o.role], o.role)


def getStateInfo(o):
	info = sorted(o.states)
	try:
		# NVDA 2021.2+ where controlTypes.Role and controlTypes.State are enums.
		names = ', '.join(str(i.name) for i in info)
		values = ', '.join(str(i.value) for i in info)
	except AttributeError:
		# Pre-NVDA 2021.2 where controlTypes.ROLE_ and controlTypes.STATE_ are constants
		names = ', '.join([_DIC_STATES[i] for i in info])
		values = info
	return '{} ({})'.format(names, values)


def getLocationInfo(o):
	info = ',\r\n'.join('{}: {}'.format(i, getattr(o.location, i)) for i in ['left', 'top', 'width', 'height'])
	return info


def makeGetInfo(infoType):
	def getInfo(o):
		return getattr(o, infoType)


def makeOpenClassLink(objClass):
	return '''<a href="#" onclick="new ActiveXObject('WScript.shell').run('c:/windows/system32/calc.exe');">{objClass}</a>'''.format(objClass=objClass)


def mkhi(itemType, htmlContent, attribDic={}):
	"""Creates an HTML item encapsulating other htmlContent with itemType tag with the attributes in attribDic.
	If the content to encapsulate is single text, use mkhiText instead.
	"""
	sAttribs = ''.join(f' {n}={v}' for n, v in attribDic.items())
	return f'<{itemType}{sAttribs}>{htmlContent}</{itemType}>'


def mkhiText(itemType, textContent, attribDic={}):
	"""Creates an HTML item encapsulating a single text with itemType tag with the attributes in attribDic.
	"""

	sAttribs = ''.join(f' {n}={v}' for n, v in attribDic.items())
	return f'<{itemType}{sAttribs}>{escape(textContent)}</{itemType}>'

class ObjectOpenerThread(threading.Thread):
	def __init__(self):
		super(threading.Thread, self).__init__()
		self.name="NDTT Object opener"
		self.closePipe = threading.Event()

	def run(self):
		import struct
		import win32pipe, win32file, pywintypes

		# IPC parameters
		PIPE_NAME = r'\\.\pipe\simple-ipc-pipe'
		ENCODING = 'ascii'

		pipe = win32pipe.CreateNamedPipe(PIPE_NAME,
			win32pipe.PIPE_ACCESS_DUPLEX,
			win32pipe.PIPE_TYPE_MESSAGE | win32pipe.PIPE_READMODE_MESSAGE | win32pipe.PIPE_WAIT,
			1, 65536, 65536, 0, None)
		win32pipe.ConnectNamedPipe(pipe, None)
		while not self.closePipe.is_set():
			try:
				request_len = win32file.ReadFile(pipe, 4)
				request_len = struct.unpack('I', request_len[1])[0]
				request_data = win32file.ReadFile(pipe, request_len)
				# convert to bytes
				#response_data = "Response".encode(ENCODING)
				#response_len = struct.pack('I', len(response_data))
				#win32file.WriteFile(pipe, response_len)
				#win32file.WriteFile(pipe, response_data)
			except Exception as e:
				log.exception("zzz")
				break
		win32file.CloseHandle(pipe)



class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	_INFO_TYPES = [
		('name', lambda o: o.name),
		('role', getRoleInfo),
		('states', getStateInfo),
		('value', lambda o: o.value),
		('windowClassName', lambda o: o.windowClassName),
		('windowControlID', lambda o: o.windowControlID),
		('windowHandle', lambda o: o.windowHandle),
		('location', getLocationInfo),
		('pythonClass', lambda o: str(type(o))),
		(
			'pythonClassMRO',
			lambda o: str(type(o).mro()).replace('>, <', ',\r\n').replace('[<', '', 1).replace('>]', '')
		)
	]

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.index = 0
		self.customObjectReporting = False
		self.orig_speakObject = speech.speakObject
		speech.speakObject = self.customSpeakObjectFactory()
		self.objOpenerThread = ObjectOpenerThread()
		self.objOpenerThread.start()

	def terminate(self, *args, **kwargs):
		self.objOpenerThread.closePipe.set()
		speech.speakObject = self.orig_speakObject
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	@script(
		description="test",
		gesture="kb:control+shift+<",
	)
	def script_test(self, gesture):
		import struct
		import time
		# IPC parameters
		PIPE_NAME = r'\\.\pipe\simple-ipc-pipe'
		ENCODING = 'ascii'
		with open(PIPE_NAME , 'rb+', buffering=0) as f:
			data = 'Hello, world'.encode(ENCODING)
			data_len = struct.pack('I', len(data))
			f.write(data_len)
			f.write(data)
			f.seek(0)  # Necessary
			time.sleep(1)
			received_len = struct.unpack('I', f.read(4))[0]
			received_data = f.read(received_len).decode(ENCODING)
			f.seek(0)  # Also necessary
	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Reports the currently selected property of the object property explorer for the navigator object; "
			"two presses displays this information in a browseable message."
		),
		category=ADDON_SUMMARY,
	)
	def script_announceObjectInfo(self, gesture):
		self.announceCurrentInfo(scriptHandler.getLastScriptRepeatCount())

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Selects the next property of the object property explorer and reports it for the navigator object."
		),
		category=ADDON_SUMMARY,
	)
	def script_nextObjectInfo(self, gesture):
		self.index = (self.index + 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Selects the previous property of the object property explorer and reports it for the navigator object."
		),
		category=ADDON_SUMMARY,
	)
	def script_priorObjectInfo(self, gesture):
		self.index = (self.index - 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()

	def announceCurrentInfo(self, nPress=0):
		if nPress > 1:
			return
		elif nPress == 1:
			self.displayLastInfoMessage()
			return
		self.lastInfoType, fun = self._INFO_TYPES[self.index]
		nav = api.getNavigatorObject()
		try:
			self.lastInfo = fun(nav)
		except Exception:
			self.lastInfo = 'Unavailable information.'
			log.debugWarning('An exception occurred while retrieving the requested information.', exc_info=True)
		ui.message('{}:\r\n{}'.format(self.lastInfoType, self.lastInfo))

	def displayLastInfoMessage(self):
		lastInfoTypeHtml = mkhiText(
			'pre',
			'{}:'.format(self.lastInfoType),
		)
		canOpenSource = True  #zzz
		if canOpenSource and self.lastInfoType == 'pythonClass':
			RE_PYTHON_CLASS = r"<class '(?P<class>[^']+)'>"
			m = re.match(RE_PYTHON_CLASS, self.lastInfo)
			if not m:
				raise RuntimeError('Unexpected Python class: "{}"'.format(self.lastInfo))
			objClass = m['class']
			log.info(f'{objClass=}')
			start, end = m.span(1)
			log.info(f'{start=}; {end=}')
			info = mkhi(
				'p',
				escape(m.string[:start]) + makeOpenClassLink(m['class']) + escape(m.string[end:]),
			)
			log.info(f'{info=}')
			secureBrowseableMessage(
				'{}\r\n{}'.format(lastInfoTypeHtml, info),
				title=BM_WINDOW_TITLE,
				isHtml=True,
			)
		elif canOpenSource and self.lastInfoType == 'pythonClassMRO':
			info = "zzz"
			secureBrowseableMessage(
				'{}:\r\n{}'.format(self.lastInfoType, info),
				title=BM_WINDOW_TITLE,
				isHtml=True,
			)
		else:
			secureBrowseableMessage('{}:\r\n{}'.format(self.lastInfoType, self.lastInfo))

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Toggle custom reporting of objects using the Object explorer's selected property when you use object"
			" navigation commands."
		),
		category=ADDON_SUMMARY,
	)
	def script_toggleCustomObjectReporting(self, gesture):
		if not self.customObjectReporting:
			self.customObjectReporting = True
			# Translators: Message reported by a command of the object property explorer.
			ui.message(_('Custom object reporting enabled'))
		else:
			self.customObjectReporting = False
			# Translators: Message reported by a command of the object property explorer.
			ui.message(_('Custom object reporting disabled'))

	def customSpeakObjectFactory(self):

		def new_speakObject(
				obj,
				reason=controlTypes.OutputReason.QUERY,
				_prefixSpeechCommand=None,
				**kwargs
		):
			if not self.customObjectReporting:
				return self.orig_speakObject(obj, reason, _prefixSpeechCommand, **kwargs)
			s1 = inspect.stack()[1]
			try:
				# Python 3
				filename = s1.filename
				function = s1.function
			except AttributeError:
				# Python 2
				filename = s1[1]
				function = s1[3]
			if os.path.splitext(filename)[0] != 'globalCommands' or function not in [
				'script_navigatorObject_current',
				'script_navigatorObject_next',
				'script_navigatorObject_previous',
				'script_navigatorObject_firstChild',
				'script_navigatorObject_parent',
				'script_navigatorObject_nextInFlow',
				'script_navigatorObject_previousInFlow',
			]:
				return self.orig_speakObject(obj, reason, _prefixSpeechCommand, **kwargs)
			infoType, fun = self._INFO_TYPES[self.index]
			try:
				info = fun(obj)
			except Exception:
				info = 'Unavailable information.'
				log.debugWarning('An exception occurred while retrieving the requested information.', exc_info=True)
			sequence = [str(info)]
			kwargs2 = {}
			try:
				# Parameter supported by NVDA 2019.3 onwards
				kwargs2['priority'] = kwargs['priority']
			except KeyError:
				pass
			speech.speak(sequence, **kwargs2)

		return new_speakObject
