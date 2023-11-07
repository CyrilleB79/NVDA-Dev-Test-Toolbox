# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2023 Cyrille Bougot
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

from .compa import controlTypesCompatWrapper as controlTypes
from .compa import matchDict
from .fileOpener import (
	openSourceFile,
	openObject,
	getNvdaCodePath,
	FileOpenerError,
)

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
RE_MSG_BRAILLE_REGION = re.compile(r'^Braille regions text: \[(?P<text>.*)\]')
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

# Regexps of log line containing a file path and a line number.
RE_STACK_TRACE_LINE = re.compile(
	r'^File "(?P<drive>(?:[A-Z]:\\)|)(?P<path>[^:"]+\.pyw?)[co]?", line (?P<line>\d+)(?:, in .+)?$'
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


class LogMessage(object):
	def __init__(self, header, msg):
		self.header = header
		self.msg = msg.strip()

	def getSpeakMessage(self, mode):
		if self.header.level == 'IO':
			return self.getSpeakIoMessage(mode)
		elif self.header.level == 'ERROR':
			return self.getSpeakErrorMessage()
		else:
			return self.msg

	def getSpeakIoMessage(self, mode):
		match = matchDict(RE_MSG_SPEAKING.match(self.msg))
		if match:
			try:
				txtSeq = match['seq']
			except Exception:
				log.error("Sequence cannot be spoken: {seq}".format(seq=match['seq']))
				return self.msg
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

		match = matchDict(RE_MSG_BEEP.match(self.msg))
		if match:
			return [BeepCommand(
				float(match['freq']),
				int(match['duration']),
				int(match['leftVol']),
				int(match['rightVol']),
			)]

		# Check for input gesture:
		match = matchDict(RE_MSG_INPUT.match(self.msg))
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

		match = matchDict(RE_MSG_TYPED_WORD.match(self.msg))
		if match:
			return self.msg

		match = matchDict(RE_MSG_BRAILLE_REGION.match(self.msg))
		if match:
			return self.msg
		else:
			import globalVars as gv
			gv.dbg = self.msg

		match = matchDict(RE_MSG_BRAILLE_DOTS.match(self.msg))
		if match:
			return self.msg

		match = matchDict(RE_MSG_TIME_SINCE_INPUT.match(self.msg))
		if match:
			return self.msg

		# Unknown message format; to be implemented.
		log.debugWarning('Message not implemented: {msg}'.format(msg=self.msg))
		return self.msg

	def getSpeakErrorMessage(self):
		msgList = self.msg.split('\r')
		try:
			idxTraceback = msgList.index('Traceback (most recent call last):')
		except ValueError:
			return self.msg
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

	@classmethod
	def makeFromTextInfo(cls, info, atStart=False):
		info = info.copy()
		if not atStart:
			raise NotImplementedError
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
				# Next line equivalent to:
				# infoMsg.end = infoLine.start
				# but usable in older NVDA versions (e.g. 2019.2)
				infoMsg.setEndPoint(infoLine, 'endToStart')
				break
		else:
			# Next line equivalent to:
			# infoMsg.end = infoLine.end
			# but usable in older NVDA versions (e.g. 2019.2)
			infoMsg.setEndPoint(infoLine, 'endToEnd')
		msg = infoMsg.text
		return cls(header, msg)


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
		'Message': RE_MESSAGE_HEADER,
		'Error': RE_ERROR_HEADER,
		'Input': re.compile(RES_MESSAGE_HEADER.format(levelName='IO')),
		'Speech': re.compile(RES_MESSAGE_HEADER.format(levelName='IO')),
		'Marker': re.compile(RES_MESSAGE_HEADER.format(levelName='INFO')),
	})

	def __init__(self, obj):
		self.obj = obj
		self.ti = obj.makeTextInfo(textInfos.POSITION_CARET)
		self.ti.collapse()

	def moveToHeader(
			self,
			direction,
			searchType,
			filterFun,
	):
		while self.ti.move(textInfos.UNIT_LINE, direction):
			tiLine = self.ti.copy()
			tiLine.expand(textInfos.UNIT_LINE)
			regexp = self.__class__.SEARCHERS[searchType]
			if regexp.search(tiLine.text.rstrip()):
				msg = LogMessage.makeFromTextInfo(
					self.ti,
					atStart=True
				)
				if filterFun(msg):
					break
		else:
			# Translators: Reported when pressing a quick navigation command in the log.
			ui.message(_('No more item'))
			return
		self.ti.updateSelection()
		msg.speak(reason=controlTypes.OutputReason.CARET, mode=searchType)


class LogContainer(ScriptableObject):
	isLogViewer = False

	enableTable = {}
	translateLog = False

	def moveToHeaderFactory(
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
		def script_moveToHeader(self, gesture):
			reader = LogReader(self)
			reader.moveToHeader(direction=dir, searchType=searchType, filterFun=filterFun)
		return script_moveToHeader

	QUICK_NAV_SCRIPT_INFO = {
		'd': ('Debug', noFilter),
		'e': ('Error', noFilter),
		'f': ('Info', noFilter),
		'g': ('DebugWarning', noFilter),
		'i': ('Io', noFilter),
		'k': ('Marker', lambda msg: RE_MSG_MARKER.match(msg.msg)),
		'm': ('Message', noFilter),
		'n': ('Input', lambda msg: RE_MSG_INPUT.match(msg.msg)),
		's': ('Speech', lambda msg: RE_MSG_SPEAKING.match(msg.msg)),
		'w': ('Warning', noFilter),
	}

	for qn, (searchType, filterFun) in QUICK_NAV_SCRIPT_INFO.items():
		locals()['script_moveToNext{st}'.format(st=searchType)] = moveToHeaderFactory(1, searchType, filterFun)
		locals()['script_moveToPrevious{st}'.format(st=searchType)] = moveToHeaderFactory(-1, searchType, filterFun)

	def initialize(self):
		if not hasattr(self, 'scriptTable'):
			self.scriptTable = {}
			for qn, (searchType, filterFun) in self.QUICK_NAV_SCRIPT_INFO.items():
				gestureId = normalizeGestureIdentifier('kb:' + qn)
				self.scriptTable[gestureId] = 'script_moveToNext{st}'.format(st=searchType)
				gestureId = normalizeGestureIdentifier('kb:shift+' + qn)
				self.scriptTable[gestureId] = 'script_moveToPrevious{st}'.format(st=searchType)
			self.scriptTable['kb:t'] = 'script_toggleLogTranslation'
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
		For treeInterceptors, the handle of the root document is returned.
		"""

		try:
			return self.windowHandle
		except AttributeError:
			return self.rootNVDAObject.windowHandle

	@script(
		# Translators: Input help mode message for Toggle log Reader script.
		description=_("Activates or deactivates the log Reader commands."),
		category=ADDON_SUMMARY,
		gesture="kb:nvda+control+alt+L",
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
		# Translators: Input help mode message for Toggle log translation script.
		description=_("Toggle speech translation in the log"),
		category=ADDON_SUMMARY,
	)
	def script_toggleLogTranslation(self, gesture):
		if LogContainer.translateLog:
			LogContainer.translateLog = False
			# Translators: A message reported when disabling log translation.
			ui.message('Log translation disabled')
		else:
			if getattr(globalPlugins, 'instantTranslate', None):
				LogContainer.translateLog = True
				# Translators: A message reported when enabling log translation.
				ui.message('Log translation enabled')
			else:
				# Translators: A message reported when trying to enable log translation.
				ui.message('Cannot enable log translation. Please install or enable Instant Translate add-on.')

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

	@staticmethod
	def openStackTraceLine(line):
		match = matchDict(RE_STACK_TRACE_LINE.match(line))
		if not match:
			return False
		if match['drive'] == '':
			nvdaSourcePath = getNvdaCodePath()
			if not nvdaSourcePath:
				# Return True even if no file open since a stack trace line has been identified.
				return True
			path = os.path.join(nvdaSourcePath, match['path'])
		else:
			path = match['drive'] + match['path']
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
		gesture="kb:nvda+control+alt+K",
	)
	def script_addMarkerInLog(self, gesture):
		markerCount = getattr(logHandler, 'ndttLogMarkerCount', 0)
		log.info(NDTT_MARKER_STRING.format(markerCount))
		# Translators: a message telling the user that a marker has been inserted in the log.
		ui.message(_("Marker {} added in the log").format(markerCount))
		logHandler.ndttLogMarkerCount = markerCount + 1

	def terminate(self, *args, **kwargs):
		scriptHandler._getObjScript = _getObjScript_original
		super(GlobalPlugin, self).terminate(*args, **kwargs)

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
			isLogViewer = False
			hParent = winUser.getAncestor(obj.windowHandle, winUser.GA_PARENT)
			try:
				hLogViewer = gui.logViewer.logViewer.GetHandle()
				isLogViewer = hLogViewer == hParent
			# Error when logViewer is None or when its windows has been dismissed or closed.
			except (AttributeError, RuntimeError):
				isLogViewer = False
			if isLogViewer:
				clsList.insert(0, LogViewerLogContainer)
			else:
				clsList.insert(0, EditableTextLogContainer)
