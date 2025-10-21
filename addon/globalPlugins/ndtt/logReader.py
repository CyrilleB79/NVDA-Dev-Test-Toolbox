# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2025 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler
import addonHandler
from baseObject import ScriptableObject
from NVDAObjects.window import Window
import scriptHandler
from scriptHandler import script
import globalPlugins
import ui
import textInfos
from keyLabels import localizedKeyLabels
import speech
try:
	from speech.commands import (  # noqa: F401 - may be used in the evaluated speech sequence
		CallbackCommand,
		BeepCommand,
		ConfigProfileTriggerCommand,
	)
	from speech.commands import (  # noqa: F401 - may be used in the evaluated speech sequence
		CharacterModeCommand,
		LangChangeCommand,
		BreakCommand,
		EndUtteranceCommand,
		PitchCommand,
		VolumeCommand,
		RateCommand,
		PhonemeCommand,
		WaveFileCommand,
	)
	preSpeechRefactor = False
except ImportError:
	# NVDA <= 2019.2.1
	from speech import (  # noqa: F401 - may be used in the evaluated speech sequence
		CharacterModeCommand,
		LangChangeCommand,
		BreakCommand,
		# EndUtteranceCommand,
		PitchCommand,
		VolumeCommand,
		RateCommand,
		PhonemeCommand,
		# CallbackCommand,
		# BeepCommand,
		# WaveFileCommand,
		# ConfigProfileTriggerCommand,
	)
	preSpeechRefactor = True
from logHandler import log
import logHandler
from treeInterceptorHandler import TreeInterceptor
import editableText
import winUser
from inputCore import normalizeGestureIdentifier
import gui.logViewer
import api
import treeInterceptorHandler
from appModules.nvda import AppModule as NVDAAppModule

from .compa import controlTypesCompatWrapper as controlTypes
from .compa import matchDict
from .fileOpener import (
	openSourceFile,
	openObject,
	getNvdaCodePath,
	FileOpenerError,
)
from .securityUtils import secureBrowseableMessage

import re
import os


addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


# Regexp strings for log message headers:
RES_ANY_LEVEL_NAME = r'[A-Z]+'
RES_CODE_PATH = r'[^\r\n]+'
RES_TIME = r'\d+:\d+:\d+.\d+'
RES_THREAD_NAME = r'[^\r\n]+'
RES_THREAD = r'\d+'
RES_MESSAGE_HEADER = (
	r"^(?P<level>{levelName}) - "
	+ r"(?P<codePath>{cp}) ".format(cp=RES_CODE_PATH)
	+ r"\((?P<time>{t})\)".format(t=RES_TIME)
	+ r"( - (?P<threadName>{thrName}) \((?P<thread>{thr})\))?".format(thrName=RES_THREAD_NAME, thr=RES_THREAD)
	+ ":"
)

RE_MESSAGE_HEADER = re.compile(RES_MESSAGE_HEADER.format(levelName=RES_ANY_LEVEL_NAME))
RE_ERROR_HEADER = re.compile(RES_MESSAGE_HEADER.format(levelName='ERROR|CRITICAL'))

# Regexps for Io messages:
RE_MSG_SPEAKING = re.compile(r'^Speaking (?P<seq>\[.+\])')
RE_MSG_BEEP = re.compile(
	r'^Beep at pitch (?P<freq>[0-9.]+), for (?P<duration>\d+) ms, '
	r'left volume (?P<leftVol>\d+), right volume (?P<rightVol>\d+)'
)
RE_MSG_INPUT = re.compile(r'^Input: (?P<device>.+?):(?P<key>.+)')
RE_MSG_TYPED_WORD = re.compile(r'^typed word: (?P<word>.+)')
RE_MSG_BRAILLE_REGIONS = re.compile(r'^Braille regions text: \[(?P<seq>.*)\]')
RE_MSG_BRAILLE_DOTS = re.compile(r'^Braille window dots:(?P<dots>.*)')
RE_MSG_TIME_SINCE_INPUT = re.compile(r'^(?P<time>\d+.\d*) sec since input')

# Regexps for speech sequence commands
RE_CANCELLABLE_SPEECH = re.compile(
	r"CancellableSpeech \("
	r"(cancelled|still valid)"
	r"(, devInfo<.+>)?"
	r"\)"
	r"((?=\])|, )"
)
RE_CALLBACK_COMMAND = re.compile(r'CallbackCommand\(name=say-all:[A-Za-z]+\)((?=\])|, )')

RE_THREAD_STACK_BLOCK = re.compile(r"Python stack for thread (?P<threadNum>\d+) \((?P<threadName>[^\r\n]+)\):")

# Regexps of log line containing a file path and a line number.
RE_STACK_TRACE_LINE = re.compile(
	r'^File "(?:(?P<path>(?P<drive>(?:[A-Z]:\\)?)[^<>:"]+\.pyw?)[co]?|(?P<specPath><[^>"]+>))", line (?P<line>\d+)(?:, in (?P<scope>.+))?$'
)
RE_ERROR_INDICATOR_LINE = re.compile(
	r"(?P<leadingSpaces>[\t ]*)(?P<leadingCtxLoc>~*)(?P<loc>\^+)(?P<tailingCtxLoc>~*)"
)

# Regexps of input help log line
RE_INPUT_HELP = re.compile(
	r'Input help: gesture (?P<identifier>.+)'
	r', bound to script (?P<scriptName>.+)'
	r' on (?P<scriptLocation>.+)'
)

TYPE_STR = type('')

NDTT_MARKER_STRING = '-- NDTT marker {} --'
RE_MSG_MARKER = re.compile(NDTT_MARKER_STRING.format(r'\d+'))

# Block types:
THREAD_STACK = "ThreadStack"
TRACEBACK_STACK = "TracebackStack"
DEV_INFO_BLOCK = "DevInfoBlock"


def noFilter(msg):
	"""A pass all filter function"""

	return True


class LogMessageHeader(object):
	def __init__(self, level, codePath, time, threadName=None, thread=None):
		self.level = level
		self.codePath = codePath
		self.time = time
		self.threadName = threadName
		self.thread = thread

	@classmethod
	def makeFromLine(cls, text):
		"""Create a LogMessageHeader from a header line"""
		match = matchDict(RE_MESSAGE_HEADER.match(text))
		if not match:
			raise LookupError
		return cls(match['level'], match['codePath'], match['time'], match['threadName'], match['thread'])


class ThreadStackHeader(object):
	def __init__(self, threadName=None, threadNum=None):
		self.threadName = threadName
		self.threadNum = threadNum

	@classmethod
	def makeFromLine(cls, text):
		"""Create a ThreadStackHeader from a header line"""

		match = matchDict(RE_THREAD_STACK_BLOCK.match(text))
		if not match:
			raise LookupError
		return cls(match["threadName"], match["threadNum"])


class TracebackStackHeader(object):
	@classmethod
	def makeFromLine(cls, text):
		pass


class LogSection(object):

	def __init__(self, ti, header, content):
		self.ti = ti
		self.header = header
		self.content = content[:-1] if content.endswith("\r") else content

	@classmethod
	def makeFromTextInfo(cls, info, atStart=False):
		ti = info.copy()
		info = info.copy()
		if not atStart:
			raise NotImplementedError
		if cls.headerType is not None:
			info.expand(textInfos.UNIT_LINE)
			header = cls.headerType.makeFromLine(info.text.strip())
			info.collapse(end=True)
		else:
			header = None
		infoContent = info.copy()
		while info.move(textInfos.UNIT_LINE, direction=1):
			infoLine = info.copy()
			infoLine.expand(textInfos.UNIT_LINE)
			if not cls.isLineInContent(infoLine.text.rstrip()):
				# Next line equivalent to:
				# infoContent.end = infoLine.start
				# but usable in older NVDA versions (e.g. 2019.2)
				infoContent.setEndPoint(infoLine, 'endToStart')
				break
		else:
			infoLine = info.copy()
			infoLine.expand(textInfos.UNIT_LINE)
			# Next line equivalent to:
			# infoContent.end = infoLine.end
			# but usable in older NVDA versions (e.g. 2019.2)
			infoContent.setEndPoint(infoLine, 'endToEnd')
		msg = infoContent.text
		ti.setEndPoint(infoContent, "endToEnd")
		return cls(ti, header, msg)

	@classmethod
	def isLineInContent(cls, line):
		return not RE_MESSAGE_HEADER.search(line)


class LogMessage(LogSection):

	headerType = LogMessageHeader

	def blockType(self):
		for (blockType, BlockClass) in BLOCK_TYPE_PARAMS.items():
			if BlockClass.containsThisBlockType(self.content):
				return blockType
		return None

	def getSpeakMessage(self, mode):
		if self.header.level == 'IO':
			return self.getSpeakIoMessage(mode)
		elif self.header.level == 'ERROR':
			return self.getSpeakErrorMessage()
		else:
			return self.content

	def getSpeakIoMessage(self, mode):
		match = matchDict(RE_MSG_SPEAKING.match(self.content))
		if match:
			try:
				txtSeq = match['seq']
			except Exception:
				log.error("Sequence cannot be spoken: {seq}".format(seq=match['seq']))
				return self.content
			txtSeq = RE_CANCELLABLE_SPEECH.sub('', txtSeq)
			txtSeq = RE_CALLBACK_COMMAND.sub('', txtSeq)
			seq = eval(txtSeq)
			# Ignore CallbackCommand and ConfigProfileTriggerCommand to avoid producing errors or unexpected
			# side effects.
			if not preSpeechRefactor:
				seq = [c for c in seq if not isinstance(c, (CallbackCommand, ConfigProfileTriggerCommand))]
			if LogContainer.translateLog:
				seq2 = []
				for s in seq:
					if isinstance(s, str):
						seq2.append(self._translate(s))
					else:
						seq2.append(s)
				seq = seq2
			return seq

		match = matchDict(RE_MSG_BEEP.match(self.content))
		if match:
			return [BeepCommand(
				float(match['freq']),
				int(match['duration']),
				int(match['leftVol']),
				int(match['rightVol']),
			)]

		# Check for input gesture:
		match = matchDict(RE_MSG_INPUT.match(self.content))
		if match:
			if mode == 'Input':
				prefix = ""
			else:
				prefix = "Input: "
			return "{prefix}{key}, {device}".format(
				prefix=prefix,
				key=match['key'],
				device=match['device'],
			)

		match = matchDict(RE_MSG_TYPED_WORD.match(self.content))
		if match:
			return self.content

		match = matchDict(RE_MSG_BRAILLE_REGIONS.match(self.content))
		if match:
			if mode == 'Braille':
				prefix = ""
			else:
				prefix = "Braille: "
			txtSeq = match["seq"]
			# Add optional end comma so that the string is recognized as a tuple, no matter its number of substrings.
			seq = eval(txtSeq + ",")
			if LogContainer.translateLog:
				seq = [self._translate(item) for item in seq]
			return "{prefix}{text}".format(
				prefix=prefix,
				text=" ".join(seq),
			)

		match = matchDict(RE_MSG_BRAILLE_DOTS.match(self.content))
		if match:
			return self.content

		match = matchDict(RE_MSG_TIME_SINCE_INPUT.match(self.content))
		if match:
			return self.content

		# Unknown message format; to be implemented.
		log.debugWarning('Message not implemented: {content}'.format(content=self.content))
		return self.content

	def getSpeakErrorMessage(self):
		msgList = self.content.split('\r')
		try:
			idxTraceback = msgList.index('Traceback (most recent call last):')
		except ValueError:
			return self.content
		else:
			errorMsg = '\r'.join(msgList[:idxTraceback])
			errorDesc = msgList[-1]
			return '\n'.join([errorDesc, errorMsg])

	@staticmethod
	def _translate(text):
		it = [p for p in globalPluginHandler.runningPlugins if p.__module__ == 'globalPlugins.instantTranslate'][0]
		return it.translateAndCache(text, it.lang_from, it.lang_to).translation

	def speak(self, reason, mode):
		seq = self.getSpeakMessage(mode)
		if isinstance(seq, TYPE_STR):
			seq = [seq]
		if (
			mode == 'Message'
			or (mode == 'Error' and self.header.level == 'CRITICAL')
		):
			seq = [self.header.level, ', '] + seq
		speech.speak(seq)


class ThreadStack(LogSection):

	headerType = ThreadStackHeader

	@staticmethod
	def containsThisBlockType(msg):
		return msg.split("\r")[0] == "Listing stacks for Python threads:"

	@staticmethod
	def blockStartIdentifier():
		return RE_THREAD_STACK_BLOCK

	@classmethod
	def isLineInContent(cls, line):
		if not super(ThreadStack, cls).isLineInContent(line):
			return False
		return not RE_THREAD_STACK_BLOCK.search(line)

	def speak(self, reason):
		seq = ["{name}; thread {num}".format(name=self.header.threadName, num=self.header.threadNum)]
		speech.speak(seq)


class TracebackStack(LogSection):

	headerType = TracebackStackHeader
	
	@staticmethod
	def containsThisBlockType(msg):
		return "Traceback (most recent call last):" in msg.split("\r")

	@staticmethod
	def blockStartIdentifier():
		return re.compile(r"Traceback \(most recent call last\):")
	
	@classmethod
	def isLineInContent(cls, line):
		if not super(TracebackStack, cls).isLineInContent(line):
			return False
		return not cls.blockStartIdentifier().search(line)

	def speak(self, reason):
		contentLines = self.content.split("\r")
		if len(contentLines) > 3 and contentLines[-3:] == ["", "During handling of the above exception, another exception occurred:", ""]:
			del contentLines[-3:]
		errorMsg = contentLines[-1]
		seq = ["Traceback for {errorMsg}".format(errorMsg=errorMsg)]
		speech.speak(seq)


class DevInfoBlock(LogSection):

	headerType = None

	@staticmethod
	def containsThisBlockType(msg):
		return "Developer info for navigator object:" in msg.split("\r")

	@staticmethod
	def blockStartIdentifier():
		return re.compile(r"^(?:(?:name: )|(?:appModule:)|(?:windowHandle: )|(?:IAccessibleObject: )|(?:UIAElement: ))")

	@classmethod
	def isLineInContent(cls, line):
		if not super(DevInfoBlock, cls).isLineInContent(line):
			return False
		return not cls.blockStartIdentifier().search(line)

	def speak(self, reason):
		contentLines = self.content.split("\r")
		seq = [contentLines[0]]
		speech.speak(seq)



BLOCK_TYPE_PARAMS = {
	THREAD_STACK: ThreadStack,
	TRACEBACK_STACK: TracebackStack,
	DEV_INFO_BLOCK: DevInfoBlock,
}


class TracebackFrame(object):
	def __init__(
		self,
		path,
		line,
		scope,
		srcLine=None,
		errLocation=None,
		errContextLocation=None,
	):
			self.path = path
			self.line = line
			self.scope = scope
			self.srcLine = srcLine
			self.errLocation = errLocation
			self.errContextLocation = errContextLocation

	@classmethod
	def makeFromTextInfo(cls, info, atStart=False):
		info = info.copy()
		if not atStart:
			raise NotImplementedError
		info.expand(textInfos.UNIT_LINE)
		match = matchDict(RE_STACK_TRACE_LINE.search(info.text.strip()))
		if not match:
			raise RuntimeError("Unable to parse stack trace line.")
		drive = match['drive']
		path = match['path']
		specPath = match["specPath"]
		line = match['line']
		scope = match['scope']

		info.move(textInfos.UNIT_LINE, direction=1)
		info.expand(textInfos.UNIT_LINE)
		sourceCodeLine = info.text.rstrip("\r")

		info.move(textInfos.UNIT_LINE, direction=1)
		info.expand(textInfos.UNIT_LINE)
		match = matchDict(RE_ERROR_INDICATOR_LINE.search(info.text.rstrip()))
		if not match:
			errLocation = None
			errContextLocation = None
		else:
			nLeadingSpaces = len(match["leadingSpaces"])
			nLeadingCtxLoc = len(match["leadingCtxLoc"])
			nLoc = len(match["loc"])
			nTailingCtxLoc = len(match["tailingCtxLoc"])
			ctxLocStart = nLeadingSpaces
			locStart = ctxLocStart + nLeadingCtxLoc
			locEnd = locStart + nLoc
			ctxLocEnd = locEnd + nTailingCtxLoc
			errLocation = (locStart, locEnd)
			errContextLocation = (ctxLocStart, ctxLocEnd)
		
		return cls(
			path=path,
			line=line,
			scope=scope,
			srcLine=sourceCodeLine,
			errLocation=errLocation,
			errContextLocation=errContextLocation,
		)


class LogReader(object):

	SEARCHERS = {k: re.compile(RES_MESSAGE_HEADER.format(levelName=k.upper())) for k in (
		'Debug',
		# 'Error', # Error added separately since needs to take into account ERROR and CRITICAL
		'Info',
		'DebugWarning',
		'Io',
		'Warning',
	)}
	SEARCHERS.update({
		"Message": RE_MESSAGE_HEADER,
		"Error": RE_ERROR_HEADER,
		"Input": re.compile(RES_MESSAGE_HEADER.format(levelName="IO")),
		"Speech": re.compile(RES_MESSAGE_HEADER.format(levelName="IO")),
		"Braille": re.compile(RES_MESSAGE_HEADER.format(levelName="IO")),
		"Marker": re.compile(RES_MESSAGE_HEADER.format(levelName="INFO")),
	})

	def __init__(self, obj):
		self.obj = obj
		
	def caretTextInfo(self):
		ti = self.obj.makeTextInfo(textInfos.POSITION_CARET)
		ti.collapse()
		return ti

	def searchForMessage(
			self,
			direction,
			searchType,
			filterFun,
			position=None,
	):
		if position:
			ti = position
		else:
			ti = self.caretTextInfo().copy()
		n=0
		while ti.move(textInfos.UNIT_LINE, direction):
			tiLine = ti.copy()
			tiLine.expand(textInfos.UNIT_LINE)
			regexp = self.__class__.SEARCHERS[searchType]
			if regexp.search(tiLine.text.rstrip()):
				msg = LogMessage.makeFromTextInfo(
					ti,
					atStart=True
				)
				if filterFun(msg):
					break
		else:
			return None
		return msg

	def moveToMessage(
		self,
		direction,
		searchType,
		filterFun,
	):
		msg = self.searchForMessage(
			direction,
			searchType,
			filterFun,
		)
		if msg is None:
			# Translators: Reported when pressing a quick navigation command in the log.
			ui.message(_('No more item'))
			return
		msgTi = msg.ti.copy()
		msgTi.collapse()
		msgTi.updateSelection()
		msg.speak(reason=controlTypes.OutputReason.CARET, mode=searchType)
	
	def getCurrentMessage(self):
		ti = self.caretTextInfo().copy()
		tiLine = self.caretTextInfo().copy()
		tiLine.expand(textInfos.UNIT_LINE)
		if tiLine.text.strip():
			# Go forward 1 character to be sure not to be at the beginning of the line in case we are already on a
			# message header
			ti.move(textInfos.UNIT_CHARACTER, 1)
		return self.searchForMessage(
			direction=-1,
			searchType="Message",
			filterFun=noFilter,
			position=ti,
		)

	def searchForBlock(self, direction, blockType):
		BlockClass = BLOCK_TYPE_PARAMS[blockType]
		reBlockStart = BlockClass.blockStartIdentifier()
		tiLine = self.caretTextInfo().copy()
		tiLine.expand(textInfos.UNIT_LINE)
		if RE_MESSAGE_HEADER.search(tiLine.text.rstrip()) and direction == -1:
			return None
		block = None
		ti = self.caretTextInfo()
		while ti.move(textInfos.UNIT_LINE, direction):
			tiLine = ti.copy()
			tiLine.expand(textInfos.UNIT_LINE)
			if RE_MESSAGE_HEADER.search(tiLine.text.rstrip()):
				break
			if reBlockStart.search(tiLine.text.rstrip()):
				block = BlockClass.makeFromTextInfo(
					ti,
					atStart=True
				)
				break
		return block

	def moveToBlock(self, direction, blockType):
		block = self.searchForBlock(direction, blockType)
		if block is None:
			# Translators: Reported when pressing a quick navigation command in the log.
			ui.message(_("No more block"))
			return
		blockTi = block.ti.copy()
		blockTi.collapse()
		blockTi.updateSelection()
		block.speak(reason=controlTypes.OutputReason.CARET)
		

	def goToError(self, select=False, includeContext=False):
		nReadLines = 0
		ti = self.caretTextInfo().copy()
		# 3 lines = 1 with file path/line number, 1 with source code, 1 with error location indication
		while nReadLines < 3:
			ti.expand(textInfos.UNIT_LINE)
			if RE_STACK_TRACE_LINE.search(ti.text.strip()):
				tbFrame = TracebackFrame.makeFromTextInfo(
					ti,
					atStart=True
				)
				if tbFrame.errLocation is None:
				# Translators: Reported when pressing the Go to error command in the log
					ui.message(_("No error indicator for this frame"))
					return
				ti.move(textInfos.UNIT_LINE, 1)
				ti.updateCaret()
				api.processPendingEvents(True)
				speech.cancelSpeech()
				if includeContext:
					selStart = tbFrame.errContextLocation[0]
					selEnd = tbFrame.errContextLocation[1]
				else:
					selStart = tbFrame.errLocation[0]
					selEnd = tbFrame.errLocation[1]
				ti.move(textInfos.UNIT_CHARACTER, selStart)
				ti.collapse()
				ti.move(textInfos.UNIT_CHARACTER, selEnd - selStart, "end")
				if select:
					ti.updateSelection()
				else:
					text = ti.text
					ti.collapse()
					ti.updateCaret()
					speech.speak([text])
				return
			elif RE_MESSAGE_HEADER.search(ti.text.rstrip()):
				break
			ti.collapse()
			ti.move(textInfos.UNIT_LINE, -1)
			nReadLines += 1
		# Translators: Reported when pressing the go to error command in a traceback line.
		ui.message(_("No traceback here"))


class LogContainer(ScriptableObject):
	isLogViewer = False

	enableTable = {}
	translateLog = False

	def moveToMessageFactory(
			dir,
			searchType,
			filterFun,
	):
		if dir == 1:
			# Translators: Input help mode message for log navigation commands. {st} will be replaced by
			# the search type (Io, Debug, Message, etc.
			description = _("Moves to the next logged message of type {st}.").format(st=searchType)
		elif dir == -1:
			# Translators: Input help mode message for log navigation commands. {st} will be replaced by the
			# search type (Io, Debug, Message, etc.
			description = _("Moves to the previous logged message of type {st}.").format(st=searchType)
		else:
			raise ValueError('Unexpected direction value: {dir}'.format(dir=dir))

		@script(
			description=description,
			category=ADDON_SUMMARY,
		)
		def script_moveToMessage(self, gesture):
			reader = LogReader(self)
			reader.moveToMessage(direction=dir, searchType=searchType, filterFun=filterFun)
		return script_moveToMessage

	QUICK_NAV_SCRIPT_INFO = {
		"b": ("Braille", lambda msg: RE_MSG_BRAILLE_REGIONS.match(msg.content)),
		"d": ("Debug", noFilter),
		"e": ("Error", noFilter),
		"f": ("Info", noFilter),
		"g": ("DebugWarning", noFilter),
		"i": ("Io", noFilter),
		"k": ("Marker", lambda msg: RE_MSG_MARKER.match(msg.content)),
		"m": ("Message", noFilter),
		"n": ("Input", lambda msg: RE_MSG_INPUT.match(msg.content)),
		"s": ("Speech", lambda msg: RE_MSG_SPEAKING.match(msg.content)),
		"w": ("Warning", noFilter),
	}

	for qn, (searchType, filterFun) in QUICK_NAV_SCRIPT_INFO.items():
		locals()['script_moveToNext{st}'.format(st=searchType)] = moveToMessageFactory(1, searchType, filterFun)
		locals()['script_moveToPrevious{st}'.format(st=searchType)] = moveToMessageFactory(-1, searchType, filterFun)

	def initialize(self):
		if not hasattr(self, 'scriptTable'):
			self.scriptTable = {}
			for qn, (searchType, filterFun) in self.QUICK_NAV_SCRIPT_INFO.items():
				gestureId = "kb:" + qn
				self.scriptTable[gestureId] = 'script_moveToNext{st}'.format(st=searchType)
				gestureId = "kb:shift+" + qn
				self.scriptTable[gestureId] = 'script_moveToPrevious{st}'.format(st=searchType)
			self.scriptTable["kb:control+e"] = "script_goToError"
			self.scriptTable["kb:b"] = "script_moveToNextBlock"
			self.scriptTable["kb:shift+b"] = "script_moveToPreviousBlock"
			self.scriptTable["kb:control+t"] = "script_toggleLogTranslation"
			self.scriptTable["kb:c"] = "script_openSourceFile"
			self.scriptTable["kb:control+h"] = "script_displayLogReaderHelp"

	def getLogReaderCommandScript(self, gesture):
		if self.isLogReaderEnabled:
			try:
				normalizedScriptTable = self._normalizedScriptTable
			except AttributeError:
				normalizedScriptTable = {normalizeGestureIdentifier(g): n for (g, n) in self.scriptTable.items()}
				self._normalizedScriptTable = normalizedScriptTable
			for gestureId in gesture.normalizedIdentifiers:
				try:
					return getattr(self, normalizedScriptTable[gestureId])
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
		For treeInterceptors, the handle of the root document is returned.
		"""

		try:
			return self.windowHandle
		except AttributeError:
			return self.rootNVDAObject.windowHandle

	def toggleLogReadingCommands(self):
	
		self.isLogReaderEnabled = not self.isLogReaderEnabled
		if self.isLogReaderEnabled:
			# Translators: A message reported when toggling log reader commands.
			msg = _("Log Reader commands enabled.")
		else:
			# Translators: A message reported when toggling log reader commands.
			msg = _("Log Reader commands disabled.")
		ui.message(msg)

	@script(
		# Translators: Input help mode message for Toggle log translation script.
		description=_("Toggles speech translation in the log"),
		category=ADDON_SUMMARY,
	)
	def script_toggleLogTranslation(self, gesture):
		if LogContainer.translateLog:
			LogContainer.translateLog = False
			# Translators: A message reported when disabling log translation.
			ui.message(_("Log translation disabled"))
		else:
			if getattr(globalPlugins, 'instantTranslate', None):
				LogContainer.translateLog = True
				# Translators: A message reported when enabling log translation.
				ui.message(_("Log translation enabled"))
			else:
				# Translators: A message reported when trying to enable log translation.
				ui.message(_("Cannot enable log translation. Please install or enable Instant Translate add-on."))

	@script(
		# Translators: Input help mode message for Open source file script.
		description=_("Opens the source code file whose path is located at the caret's position."),
		category=ADDON_SUMMARY,
	)
	def script_openSourceFile(self, gesture):
		ti = self.makeTextInfo('caret')
		ti.collapse()
		ti.expand(textInfos.UNIT_LINE)
		line = ti.text.strip()
		try:
			if self.openStackTraceLine(line):
				return
			if self.openMessageHeaderLine(line):
				return
			if self.openInputHelpLine(line):
				return
		except FileOpenerError as e:
			log.debugWarning(str(e))
			ui.message(e.getUserFriendlyMessage())
			return
		# Translators: A message reported when trying to open the source code from the current line.
		ui.message(_('No file path or object found on this line.'))

	
	@script(
		description=_(
			# Translators: Input help mode message for go to error script.
			"Move the caret at the error's position in a traceback frame."
			" A second press selects the erroneous code."
			" A third press selects the error with its context."
			),
		category=ADDON_SUMMARY,
	)
	def script_goToError(self, gesture):
		reader = LogReader(self)
		nRepeat = scriptHandler.getLastScriptRepeatCount()
		if nRepeat == 0:
			select = False
			includeContext = False	
		elif nRepeat == 1:
			select = True
			includeContext = False	
		elif nRepeat == 2:
			select = True
			includeContext = True
		else:
			return
		reader.goToError(select, includeContext)

	@script(
		# Translators: Input help mode message for move to next block script.
		description="Move the caret to the next block.",
		category=ADDON_SUMMARY,
	)
	def script_moveToNextBlock(self, gesture):
		reader = LogReader(self)
		curMsg = reader.getCurrentMessage()
		blockType = curMsg.blockType()
		if blockType is None:
			# Translators: A message reported when using block navigation command
			ui.message(_("No block in this message"))
			return
		reader.moveToBlock(direction=1, blockType=blockType)

	@script(
		# Translators: Input help mode message for move to previous block script.
		description="Move the caret to the previous block.",
		category=ADDON_SUMMARY,
	)
	def script_moveToPreviousBlock(self, gesture):
		reader = LogReader(self)
		curMsg = reader.getCurrentMessage()
		blockType = curMsg.blockType()
		if blockType is None:
			# Translators: A message reported when using block navigation command
			ui.message(_("No block in this message"))
			return
		reader.moveToBlock(direction=-1, blockType=blockType)

	@script(
		# Translators: Input help mode message for Log Reader help script.
		description=_("Displays help for the Log reader commands"),
		category=ADDON_SUMMARY,
	)
	def script_displayLogReaderHelp(self, gesture):
		# Translators: Title of the Log Reader commands help window.
		title = _("Log Reader commands ({name})").format(name=ADDON_SUMMARY)
		cmdList = []
		for (gesture, scriptName) in self.scriptTable.items():
			gesture = ':'.join(gesture.split(":")[1:])
			script = getattr(self, scriptName)
			desc = script.__doc__
			cmdParts = []
			cmdParts.append(
				# Translators: Separator between key names in the log reader command help window.
				"+".join(
					localizedKeyLabels.get(k.lower(), k) for k in gesture.split("+")
				)
			)
			cmdParts.append(': ')
			cmdParts.append(desc)
			cmdList.append(''.join(cmdParts))
		cmdList = '\r'.join(cmdList)
		secureBrowseableMessage(cmdList, title)

	@staticmethod
	def openStackTraceLine(line):
		match = matchDict(RE_STACK_TRACE_LINE.match(line))
		if not match:
			return False
		if match["specPath"]:
			path = match["specPath"]
		elif match['drive'] == '':
			nvdaSourcePath = getNvdaCodePath()
			if not nvdaSourcePath:
				 # Return True even if no file open since a stack trace line has been identified.
				return True
			path = os.path.join(nvdaSourcePath, match['path'])
		else:
			path = match['path']
		line = match['line']
		openSourceFile(path, line)
		return True

	@staticmethod
	def openMessageHeaderLine(line):
		match = matchDict(RE_MESSAGE_HEADER.match(line))
		if not match:
			return False
		objPath = match['codePath']
		externalPrefix = 'external:'
		if objPath.startswith(externalPrefix):
			objPath = objPath[len(externalPrefix):]
		openObject(objPath)
		return True

	@staticmethod
	def openInputHelpLine(line):
		match = matchDict(RE_INPUT_HELP.match(line))
		if not match:
			return False
		
		objPath = '{loc}.script_{name}'.format(loc=match['scriptLocation'], name=match['scriptName'])
		openObject(objPath)
		return True


class EditableTextLogContainer(LogContainer):
	def initOverlayClass(self):
		self.initialize()


class LogViewerLogContainer(EditableTextLogContainer):
	isLogViewer = True


class DocumentWithLog(Window):

	def _get_treeInterceptorClass(self):
		cls = super(DocumentWithLog, self).treeInterceptorClass
		bases = (DocumentWithLogTreeInterceptor, cls)
		# Python 2/3: use str() to convert type since it is str in both version of Python
		name = str('Mixed_[{classList}]').format(classList=str("+").join([x.__name__ for x in bases]))
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

	@script(
		# Translators: Input help mode message for Add marker in log script.
		description=_("Adds a marker in the log."),
		category=ADDON_SUMMARY,
	)
	def script_addMarkerInLog(self, gesture):
		markerCount = getattr(logHandler, 'ndttLogMarkerCount', 0)
		log.info(NDTT_MARKER_STRING.format(markerCount))
		# Translators: a message telling the user that a marker has been inserted in the log.
		ui.message(_("Marker {} added in the log").format(markerCount))
		logHandler.ndttLogMarkerCount = markerCount + 1

	@script(
		# Translators: Input help mode message for Toggle log Reader script.
		description=_("Activates or deactivates the log Reader commands."),
		category=ADDON_SUMMARY,
	)
	def script_toggleLogReadingCommands(self, gesture):
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if (
			isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor)
			and not treeInterceptor.passThrough
		):
			obj = treeInterceptor
		if isinstance(obj, LogContainer):
			obj.toggleLogReadingCommands()
		else:
			# Translators: A message when using Toggle log Reader script.
			ui.message(_("Not in a text area."))

	def terminate(self, *args, **kwargs):
		scriptHandler._getObjScript = _getObjScript_original
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	def isNvdaPythonConsoleUIOutputCtrl(self, obj):
		if not isinstance(obj.appModule, NVDAAppModule):
			return False
		try:
			# NVDA 2021.1
			obj.appModule.isNvdaPythonConsoleUIOutputCtrl
		except AttributeError:
			pass
		else:
			return obj.appModule.isNvdaPythonConsoleUIOutputCtrl(obj)
		# NVDA < 2021.1 - fallback to explicit code of the function
		from pythonConsole import consoleUI
		if not consoleUI:
			return False
		return obj.windowHandle == consoleUI.outputCtrl.GetHandle()

	def isNvdaLogViewer(self, obj):
		hParent = winUser.getAncestor(obj.windowHandle, winUser.GA_PARENT)
		try:
			hLogViewer = gui.logViewer.logViewer.GetHandle()
			return hLogViewer == hParent
		# Error when logViewer is None or when its windows has been dismissed or closed.
		except (AttributeError, RuntimeError):
			return False

	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# Note: chooseNVDAObjectOverlayClasses needs to be explicitely called in the mother class; else, NVDA
		# will skip it.
		if obj.role == controlTypes.Role.DOCUMENT:
			clsList.insert(0, DocumentWithLog)
		for cls in clsList:
			if issubclass(cls, editableText.EditableText):
				isEditable = True
				break
		else:
			isEditable = False
		if isEditable:
			shouldEnableLogReader = (
				# Enable log reader in Python console output
				self.isNvdaPythonConsoleUIOutputCtrl(obj)
				# Enable log reader in log viewer
				or self.isNvdaLogViewer(obj)
			)
			if shouldEnableLogReader:
				clsList.insert(0, LogViewerLogContainer)
			else:
				clsList.insert(0, EditableTextLogContainer)
