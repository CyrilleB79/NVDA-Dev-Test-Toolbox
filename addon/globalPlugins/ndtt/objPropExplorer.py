# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019-2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import inspect
import os
import re
import threading
try:
	from html import escape
except ImportError:  # NVDA 2019.2.1 and below
	escape = lambda x: x
import time

import globalPluginHandler
import ui
import api
from .compa import controlTypesCompatWrapper as controlTypes
from .compa import matchDict
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


def makeOpenClassLink(objClass, file):
	# JavaScript to be executed when a link is clicked
	# It uses the FilesystemObject to write a file
	js=r"""
	var fh = new ActiveXObject('Scripting.FileSystemObject').CreateTextFile('{file}', 2, true);
	fh.Write('{objClass}');
	fh.close();
	""".format(
		file=file,
		objClass=objClass,
	)
	js=r"""
	function saveFile(strFullPath, strContent) {{
	 var fso = new ActiveXObject('Scripting.FileSystemObject');
	 var utf8Enc = new ActiveXObject('Utf8Lib.Utf8Enc');
	 var flOutput = fso.CreateTextFile(strFullPath, true); //true for overwrite
	 flOutput.BinaryWrite(utf8Enc.UnicodeToUtf8(strContent));
	 flOutput.Close();
	}};
	saveFile('{file}', '{objClass}');
	""".format(
			file=file,
			objClass=objClass,
		)
	cmd = r"c:\windows\system32\calc.exe"
	cmd = r'echo tototiti > h:\out.txt'
	cmd = r'cmd /c echo zzzz > h:\out.txt'
	cmd = r'cmd /c echo {className} > h:\out.txt'.format(className=objClass)
	cmd = r'cmd /c /q echo {className} > h:\out.txt'.format(className=objClass)
	js= r"new ActiveXObject('WScript.shell').run('{cPath}');".format(cPath=cmd.replace('\\', '\\\\'))
	retString = '''<a href="#" onclick="{js}">{objClass}</a>'''.format(
		js=js,
		objClass=objClass,
	)
	log.info(retString)
	return retString

def mkhi(itemType, htmlContent, attribDic={}):
	"""Creates an HTML item encapsulating other htmlContent with itemType tag with the attributes in attribDic.
	If the content to encapsulate is single text, use mkhiText instead.
	"""
	sAttribs = ''.join(' {n}={v}'.format(n=n, v=v) for n, v in attribDic.items())
	return '<{itemType}{sAttribs}>{htmlContent}</{itemType}>'.format(
		itemType=itemType,
		sAttribs=sAttribs,
		htmlContent=htmlContent,
		
		
	)


def mkhiText(itemType, textContent, attribDic={}):
	"""Creates an HTML item encapsulating a single text with itemType tag with the attributes in attribDic.
	"""

	sAttribs = ''.join(' {n}={v}'.format(n=n, v=v) for n, v in attribDic.items())
	return '<{itemType}{sAttribs}>{text}</{itemType}>'.format(
		itemType=itemType,
		sAttribs=sAttribs,
		text=escape(textContent),
		
	)

class ObjectOpenerThread(threading.Thread):
	def __init__(self, file, *args, **kw):
		super(ObjectOpenerThread, self).__init__(*args, **kw)
		self.daemon = True
		self.file = file
		self.closePipe = threading.Event()

	def run(self):
		import ctypes
		import sys
		
		PIPE_ACCESS_DUPLEX = 0x00000003
		PIPE_TYPE_MESSAGE = 0x00000004
		PIPE_READMODE_MESSAGE = 0x00000002
		PIPE_WAIT = 0x00000000
		INVALID_HANDLE_VALUE = -1
		
		CreateNamedPipe = ctypes.windll.kernel32.CreateNamedPipeW
		ConnectNamedPipe = ctypes.windll.kernel32.ConnectNamedPipe
		ReadFile = ctypes.windll.kernel32.ReadFile
		WriteFile = ctypes.windll.kernel32.WriteFile
		
		pipe_name = r'\\.\pipe\mypipe'
		
		pipe_handle = CreateNamedPipe(
		    pipe_name,
		    PIPE_ACCESS_DUPLEX,
		    PIPE_TYPE_MESSAGE | PIPE_READMODE_MESSAGE | PIPE_WAIT,
		    1, 65536, 65536, 0, None
		)
		
		if pipe_handle == INVALID_HANDLE_VALUE:
		    log.error('Cannot create named pipe')
		    return

		ConnectNamedPipe(pipe_handle, None)
		while True:
		    buffer = ctypes.create_string_buffer(1024)
		    bytes_read = ctypes.c_ulong(0)
		
		    #zzz success = ReadFile(pipe_handle, buffer, len(buffer), ctypes.byref(bytes_read), None)
		    success = ReadFile(pipe_handle, buffer, 10, ctypes.byref(bytes_read), None)
		    
		    if success:
		        data = buffer.value[:bytes_read.value].decode('utf-8')
		        import core
		        def f():
		        	import time
		        	time.sleep(1)
		        	ui.message(data)
		        core.callLater(0, f)
		        if data == "exit":
		            return
		    else:
		        log.error("Failed to read named pipe.")
		        return


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
			lambda o: str(type(o).mro()).replace('>, <', '>,\r\n<').replace('[<', '<', 1).replace('>]', '>')
		)
	]

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.index = 0
		self.customObjectReporting = False
		self.orig_speakObject = speech.speakObject
		speech.speakObject = self.customSpeakObjectFactory()
		self.file = os.path.join(
			os.environ['tmp'],
			'nvda_test_ipc.txt',
		)
		self.file = r'h:\out.txt'
		self.objOpenerThread = ObjectOpenerThread(name="NDTT Object opener", file=self.file)
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
		log.info('display last info')
		lastInfoTypeHtml = mkhiText(
			'pre',
			'{}:'.format(self.lastInfoType),
		)
		canOpenSource = True  #zzz
		RE_PYTHON_CLASS = r"<(?:(?:class)|(?:type)) '(?P<class>[^']+)'>"
		if canOpenSource and self.lastInfoType in ['pythonClass', 'pythonClassMRO']:
			log.info('class or mro')
			infoList = []
			for line in self.lastInfo.split('\r\n'):
				m = re.match(RE_PYTHON_CLASS, line)
				if not m:
					raise RuntimeError('Unexpected Python class: "{}"'.format(line))
				objClass = matchDict(m)['class']
				start, end = m.span(1)
				info = mkhi(
					'p',
					escape(m.string[:start]) + makeOpenClassLink(matchDict(m)['class'], file=self.file) + escape(m.string[end:]),
				)
				infoList.append(info)
			lastInfoHtml = '\r\n'.join(infoList)
		else:
			log.info('others')
			lastInfoHtml = mkhi('pre', self.lastInfo)
		secureBrowseableMessage(
			'{infoType}{info}'.format(infoType=lastInfoTypeHtml, info=lastInfoHtml),
			title=BM_WINDOW_TITLE,
			isHtml=True,
		)

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
