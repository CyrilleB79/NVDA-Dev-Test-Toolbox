# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

import globalPluginHandler
import addonHandler
from baseObject import ScriptableObject
from NVDAObjects.window import Window
import scriptHandler
from scriptHandler import script
import ui
import textInfos
import speech
from speech.commands import (
	CharacterModeCommand,
	LangChangeCommand,
	BreakCommand,
	EndUtteranceCommand,
	PitchCommand,
	VolumeCommand,
	RateCommand,
	PhonemeCommand,
	CallbackCommand,
	BeepCommand,
	WaveFileCommand,
	ConfigProfileTriggerCommand
)
from logHandler import log
from treeInterceptorHandler import TreeInterceptor
import editableText
import winUser
import config
from inputCore import normalizeGestureIdentifier

from .compa import controlTypes, appDir
from .fileOpener import openSourceFile, getNvdaCodePath

import re
import os


# Save NVDA translations before setting the add-on's translations
nvdaTranslations = _

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


# Regexp strings for log message headers:
RES_ANY_LEVEL_NAME = r'[A-Z]+'
RES_CODE_PATH = r'[^\r\n]+'
RES_TIME = r'[^\r\n]+'
RES_THREAD_NAME = r'[^\r\n]+'
RES_THREAD = r'\d+'
RES_MESSAGE_HEADER = (
	rf"^(?P<level>{{levelName}}) - "
	rf"(?P<codePath>{RES_CODE_PATH}) "
	rf"\((?P<time>{RES_TIME})\)"
	rf"( - (?P<threadName>{RES_THREAD_NAME}) \((?P<thread>{RES_THREAD})\))?"
	":"
)

RE_MESSAGE_HEADER = re.compile(RES_MESSAGE_HEADER.format(levelName=RES_ANY_LEVEL_NAME))

# Regexps for Io messages:
RE_MSG_SPEAKING = re.compile(r'^Speaking (?P<seq>\[.+\])')
RE_MSG_BEEP = re.compile(r'^Beep at pitch (?P<freq>[0-9.]+), for (?P<duration>\d+) ms, left volume (?P<leftVol>\d+), right volume (?P<rightVol>\d+)') 
RE_MSG_INPUT = re.compile(r'^Input: (?P<device>.+?):(?P<key>.+)')
RE_MSG_TYPED_WORD = re.compile(r'^typed word: (?P<word>.+)')
RE_MSG_BRAILLE_REGION = re.compile(r'Braille regions text: \[.*\]')
RE_MSG_BRAILLE_DOTS = re.compile(r'^Braille window dots:.*')
RE_MSG_TIME_SINCE_INPUT = re.compile(r'^\d+.\d* sec since input')

# Regexps for speech sequence commands
RE_CANCELLABLE_SPEECH = re.compile(
	r"CancellableSpeech \("
	r"(cancelled|still valid)"
	r"(, devInfo<.+>)?"
	r"\)"
	r"((?=\])|, )"
)
RE_CALLBACK_COMMAND = re.compile(r'CallbackCommand\(name=say-all:[A-Za-z]+\)((?=\])|, )')

# Regexps of log line containing a file path and a line number.
RE_NVDA_FILEPATH = re.compile(r'^File "(?P<path>[^:"]+\.py)c?", line (?P<line>\d+)(?:, in .+)?$')
RE_EXTERNAL_FILEPATH = re.compile(r'^File "(?P<path>[A-Z]:\\[^"]+\.py)", line (?P<line>\d+)(?:, in .+)?$')

#zzz # Regexps of console output line containing an object definition
#zzz RE_NVDA_HELP = re.compile(r'^File "(?P<path>[^:"]+\.py)c?", line (?P<line>\d+)(?:, in .+)?$')



class LogMessageHeader:
	def __init__(self, level, codePath, time, threadName=None, thread=None):
		self.level = level
		self.codePath = codePath
		self.time = time
		self.threadName = threadName
		self.thread = thread
		
	@classmethod
	def makeFromLine(cls, text):
		"""Create a LogMessageHeader from a header line"""
		match = RE_MESSAGE_HEADER.match(text)
		if not match:
			raise LookupError
		return cls(match['level'], match['codePath'], match['time'], match['threadName'], match['thread'])

class LogMessage:
	def __init__(self, header, msg):
		self.header = header
		self.msg = msg.strip()
	
	def getSpeakMessage(self, mode):
		if self.header.level == 'IO':
			match = RE_MSG_SPEAKING.match(self.msg)
			if match:
				try:
					txtSeq = match['seq']
				except Exception:
					log.error(f"Sequence cannot be spoken: {match['seq']}")
					return self.msg
				txtSeq = RE_CANCELLABLE_SPEECH.sub('', txtSeq)
				txtSeq = RE_CALLBACK_COMMAND.sub('', txtSeq)
				seq = eval(txtSeq)
				# Ignore CallbackCommand and ConfigProfileTriggerCommand to avoid producing errors or unexpected side effect.
				seq = [c for c in seq if not isinstance(c, (CallbackCommand, ConfigProfileTriggerCommand))]
				return seq
				
			match = RE_MSG_BEEP.match(self.msg)
			if match:
				return [BeepCommand(
					float(match['freq']),
					int(match['duration']),
					int(match['leftVol']),
					int(match['rightVol']),
				)]
			
			# Check for input gesture:
			match = RE_MSG_INPUT.match(self.msg)
			if match:
				return f"Input: {match['key']}, {match['device']}"
			
			match = RE_MSG_TYPED_WORD.match(self.msg)
			if match:
				return self.msg
			
			match = RE_MSG_BRAILLE_REGION.match(self.msg)
			if match:
				return self.msg
			
			match = RE_MSG_BRAILLE_DOTS.match(self.msg)
			if match:
				return self.msg
			
			match = RE_MSG_TIME_SINCE_INPUT.match(self.msg)
			if match:
				return self.msg
			
			# Unknown message format; to be implemented.
			raise NotImplementedError(f'Message not implemented: {self.msg}')
			
		elif self.header.level == 'ERROR':
			msgList = self.msg.split('\r')
			try:
				idxTraceback = msgList.index('Traceback (most recent call last):')
			except ValueError:
				return self.msg
			else:
				errorMsg = '\r'.join(msgList[:idxTraceback])
				errorDesc = msgList[-1]
				return '\n'.join([errorDesc, errorMsg])
		else:
			return self.msg
	
	def speak(self, reason, mode):
		seq = self.getSpeakMessage(mode)
		if isinstance(seq, str):
			seq = [seq]
		if mode == 'Message':
			seq = [self.header.level, ', ', *seq]
		speech.speak(seq)
	
	@classmethod
	def makeFromTextInfo(cls, info, atStart=False):
		info = info.copy()
		if not atStart:
			raise NotImplemented
		info.expand(textInfos.UNIT_LINE)
		header = LogMessageHeader.makeFromLine(info.text.strip())
		info.collapse(end=True)
		infoMsg = info.copy()
		infoLine = info.copy()
		infoLine.expand(textInfos.UNIT_LINE)
		while info.move(textInfos.UNIT_LINE, direction=1):
			infoLine = info.copy()
			infoLine.expand(textInfos.UNIT_LINE)
			if RE_MESSAGE_HEADER.search(infoLine.text.rstrip()):
				#infoMsg.end = infoLine.start
				infoMsg.setEndPoint(infoLine, 'endToStart')
				break
		else:
			infoMsg.end = infoLine.end
		msg = infoMsg.text
		return cls(header, msg)	


class LogReader:

	SEARCHERS = {k: re.compile(RES_MESSAGE_HEADER.format(levelName=k.upper())) for k in (
		'Debug',
		'Error',
		'Info',
		'DebugWarning',
		'Io',
		'Warning',
	)}
	SEARCHERS.update({
		'Message': RE_MESSAGE_HEADER,
		'Output': re.compile(RES_MESSAGE_HEADER.format(levelName='IO')),
	})
	
	def __init__(self, obj):
		self.obj = obj
		self.ti = obj.makeTextInfo(textInfos.POSITION_CARET)
		self.ti.collapse()
	
	def moveToHeader(self, direction, searchType):
		while self.ti.move(textInfos.UNIT_LINE, direction):
			tiLine = self.ti.copy()
			tiLine.expand(textInfos.UNIT_LINE)
			regexp = self.__class__.SEARCHERS[searchType]
			if regexp.search(tiLine.text.rstrip()):
				break
		else:
			# Translators: Reported when pressing a quick navigation command in the log.
			ui.message(_('No more item'))
			return
		self.ti.updateSelection()
		LogMessage.makeFromTextInfo(self.ti, atStart=True).speak(reason=controlTypes.OutputReason.CARET, mode=searchType)


class LogContainer(ScriptableObject):
	isLogViewer = False
	
	enableTable = {}

	def moveToHeaderFactory(dir, searchType):
		if dir == 1:
			# Translators: Input help mode message for log navigation commands. {st} will be replaced by the search type (Io, Debug, Message, etc.
			description = _( "Move to next logged message of type {st}.").format(st=searchType)
		elif dir == -1:
			# Translators: Input help mode message for log navigation commands. {st} will be replaced by the search type (Io, Debug, Message, etc.
			description = _("Move to previous logged message of type {st}.").format(st=searchType)
		else:
			raise ValueError('Unexpected direction value: {dir}'.format(dir=dir))
		@script(
			description=description,
			category=ADDON_SUMMARY,
		)
		def script_moveToHeader(self,gesture):
			reader = LogReader(self)
			reader.moveToHeader(direction=dir, searchType=searchType)
		return script_moveToHeader
	
	QUICK_NAV_SCRIPT_INFO = {
		'd': ('Debug', moveToHeaderFactory),
		'e': ('Error', moveToHeaderFactory),
		'f': ('Info', moveToHeaderFactory),
		'g': ('DebugWarning', moveToHeaderFactory),
		'i': ('Io', moveToHeaderFactory),
		'm': ('Message', moveToHeaderFactory),
		'w': ('Warning', moveToHeaderFactory),
	}
	
	for qn, (searchType, scriptMaker) in QUICK_NAV_SCRIPT_INFO.items():
		locals()['script_moveToNext{st}'.format(st=searchType)] = scriptMaker(1, searchType)
		locals()['script_moveToPrevious{st}'.format(st=searchType)] = scriptMaker(-1, searchType)
	
	def initialize(self):
		if not hasattr(self, 'scriptTable'):
			self.scriptTable = {}
			for qn, (searchType, scriptMaker) in self.QUICK_NAV_SCRIPT_INFO.items():
				gestureId = normalizeGestureIdentifier('kb:' + qn)
				self.scriptTable[gestureId] = 'script_moveToNext{st}'.format(st=searchType)
				gestureId = normalizeGestureIdentifier('kb:shift+' + qn)
				self.scriptTable[gestureId] = 'script_moveToPrevious{st}'.format(st=searchType)
			self.scriptTable['kb:c'] = 'script_openSourceFile'
	
	def getLogReaderCommandScript(self, gesture):
		if self.isLogReaderEnabled:
			for gestureId in gesture.normalizedIdentifiers:
				try:
					return getattr(self, self.scriptTable[gestureId])
				except KeyError:
					pass
		return None
	
	@property
	def isLogReaderEnabled(self):
		return LogContainer.enableTable.get(self.getWindowHandle(), self.isLogViewer)
		
	@isLogReaderEnabled.setter
	def isLogReaderEnabled(self, value):
		LogContainer.enableTable[self.getWindowHandle()] = value
	
	def getWindowHandle(self):
		""" Returns the handle of the window containing this LogContainer.
		For treeInterceptors, the handle of the root documente is returned.
		"""
		
		try:
			return self.windowHandle
		except AttributeError:
			return self.rootNVDAObject.windowHandle
	
	@script(
		# Translators: Input help mode message for Toggle log Reader script.
		description=_("Activate or deactivate log Reader commands."),
		category=ADDON_SUMMARY,
		gesture = "kb:nvda+control+alt+L",
	)
	def script_toggleReaderCommands(self, enabled):
		self.isLogReaderEnabled = not self.isLogReaderEnabled
		if self.isLogReaderEnabled:
			# Translators: A message reported when toggling log reader commands.
			msg = _("Log Reader commands enabled.")
		else:
			# Translators: A message reported when toggling log reader commands.
			msg = _("Log Reader commands disabled.")
		ui.message(msg)
	
	@script(
		# Translators: Input help mode message for Open source file script.
		description=_("Open the source code file whose path is located at the caret's position."),
		category=ADDON_SUMMARY,
	)
	def script_openSourceFile(self, gesture):
		ti = self.makeTextInfo('caret')
		ti.collapse()
		ti.expand(textInfos.UNIT_LINE)
		line = ti.text.strip()
		path = None
		match = RE_NVDA_FILEPATH.match(line)
		if match:
			nvdaSourcePath = getNvdaCodePath()
			if not nvdaSourcePath:
				return
			path = os.path.join(nvdaSourcePath, match['path'])
		if not path:
			match = RE_EXTERNAL_FILEPATH.match(line)
			if match:
				path = match['path']
		if not path:
			# Translators: A message reported when trying to open the source code from the current line.
			ui.message(_('No file path found on this line.'))
			return
		line = match['line']
		openSourceFile(path, line)

class EditableTextLogContainer(LogContainer):
	def initOverlayClass(self):
		self.initialize()

class LogViewerLogContainer(EditableTextLogContainer):
	isLogViewer = True

class DocumentWithLog(Window):

	def _get_treeInterceptorClass(self):
		cls = super(DocumentWithLog, self)._get_treeInterceptorClass()
		bases = (DocumentWithLogTreeInterceptor, cls)
		name = f'Mixed_[{"+".join([x.__name__ for x in bases])}]'
		newCls = type(name, bases, {"__module__": __name__})
		return newCls
	
	
class DocumentWithLogTreeInterceptor(TreeInterceptor, LogContainer):
	def __init__(self, *args, **kw):
		super(DocumentWithLogTreeInterceptor, self).__init__(*args, **kw)
		self.initialize()

_getObjScript_original = scriptHandler._getObjScript
def _getObjScript_patched(obj, gesture, globalMapScripts, *args, **kw):
	""" This function patches scriptHandler._getObjScript in order to return a log reader command script
	if one matches the gesture before searching the global gesture maps for a match.
	"""
	
	if isinstance(obj, LogContainer):
		try:
			script = obj.getLogReaderCommandScript(gesture)
			if script:
				return script
		except Exception:  # Prevent a faulty add-on from breaking script handling altogether (#5446)
			log.exception()
	return _getObjScript_original(obj, gesture, globalMapScripts, *args, **kw)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		scriptHandler._getObjScript = _getObjScript_patched
		LogContainer.enableTable = {}
		
	def terminate(self, *args, **kwargs):
		scriptHandler._getObjScript = _getObjScript_original
		super(GlobalPlugin, self).terminate(*args, **kwargs)
	
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
	# Note: chooseNVDAObjectOverlayClasses needs to be explicitely called in the mother class; else, NVDA will skip it.
		for cls in clsList:
			if issubclass(cls, editableText.EditableText):
				isEditable = True
				break
		else:
			isEditable = False
		if isEditable:
			isLogViewer = False
			hParent = winUser.getAncestor(obj.windowHandle, winUser.GA_PARENT)
			if hParent:
				text = winUser.getWindowText(hParent)
				isLogViewer = text == nvdaTranslations("NVDA Log Viewer")
			if isLogViewer:
				clsList.insert(0, LogViewerLogContainer)
			else:
				clsList.insert(0, EditableTextLogContainer)
		if obj.role == controlTypes.Role.DOCUMENT:
			clsList.insert(0, DocumentWithLog)
