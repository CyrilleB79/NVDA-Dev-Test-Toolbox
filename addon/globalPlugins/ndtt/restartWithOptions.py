# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import gui
import queueHandler
import globalVars
import globalPluginHandler
import addonHandler
from scriptHandler import script
import languageHandler

import wx
import sys
import os
import weakref
from . import compa

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


def restartWithOptions(options):
	"""Restarts NVDA by starting a new copy, providing some options."""
	if globalVars.appArgs.launcher:
		import gui
		globalVars.exitCode = 3
		try:
			gui.safeAppExit()
		except AttributeError:
			wx.GetApp().ExitMainLoop()
		return
	import subprocess
	import winUser
	import shellapi
	if not hasattr(sys, "frozen"):
		options.insert(0, os.path.basename(sys.argv[0]))
	if sys.version_info.major < 3 and "-r" not in options:
		# NVDA <= 2019.2.1 (Python 2) do not restart automatically if a new instance is started.
		options.append("-r")
	file = sys.executable
	parameters = subprocess.list2cmdline(options)
	directory = compa.appDir
	if sys.version_info.major < 3:
		file = file.decode("mbcs")
		parameters = parameters.decode("mbcs")
	shellapi.ShellExecute(
		hwnd=None,
		operation=None,
		file=file,
		parameters=parameters,
		directory=directory,
		# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL
		showCmd=winUser.SW_SHOWNORMAL
	)


class FileSelectionHelper(object):
	"""
	Abstracts away details for creating a file selection helper. The file selection helper is a textCtrl with a
	button in horizontal layout. The Button launches a file explorer. To get the path selected by the user, use
	the `pathControl` property which exposes a wx.TextCtrl.
	"""
	def __init__(self, parent, buttonText, wildcard, browseForFileTitle):
		""" @param parent: An instance of the parent wx window. EG wx.Dialog
			@param buttonText: The text for the button to launch a file selection dialog (wx.DirDialog). This is
				typically 'Browse'
			@type buttonText: string
			@param wildcard: The text for the title of the file dialog (wx.FileDialog)
			@type wildcard: string
			@param browseForFileTitle: The text for the title of the file dialog (wx.FileDialog)
			@type browseForFileTitle: string
		"""
		object.__init__(self)
		self._textCtrl = wx.TextCtrl(parent)
		self._browseButton = wx.Button(parent, label=buttonText)
		self._wildcard = wildcard
		self._browseForFileTitle = browseForFileTitle
		self._browseButton.Bind(wx.EVT_BUTTON, self.onBrowseForFile)
		self._sizer = gui.guiHelper.associateElements(self._textCtrl, self._browseButton)
		self._parent = parent

	@property
	def pathControl(self):
		return self._textCtrl

	@property
	def sizer(self):
		return self._sizer

	def getDefaultBrowseForFilePath(self):
		return self._textCtrl.Value or "c:\\"

	def onBrowseForFile(self, evt):
		startPath = self.getDefaultBrowseForFilePath()
		filename = wx.FileSelector(
			# Translators: The title of a file selector window
			_("Save As"),
			default_path=startPath,
			default_filename="nvda.log",
			wildcard=self._wildcard,
			flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
			parent=self._parent,
		)
		if filename:
			self._textCtrl.Value = filename


class CommandLineOption(object):
	def __init__(self, description, flagList, allowInSecureMode):
		self.description = description
		self.flagList = flagList
		self.allowInSecureMode = allowInSecureMode

	def shouldBeDisabled(self):
		return globalVars.appArgs.secure and not self.allowInSecureMode

	def shouldBeDisplayed(self):
		return True

	def addWithGuiHelper(self, parent, sHelper):
		raise NotImplementedError

	@property
	def flagListLabel(self):
		label = " ".join(self.flagList)
		return label.replace('{', '').replace('}', '')

	def disable(self):
		for c in self.controls:
			c.Disable()

	@property
	def value(self):
		return self.mainControl.Value

	@property
	def mainControl(self):
		return self.controls[0]


class CommandLineBooleanOption(CommandLineOption):
	"""A simple command line option only controlled by the presence or not of a flags.
	E.g. --disable-addons or -s
	"""

	def addWithGuiHelper(self, parent, sHelper):
		checkBox = wx.CheckBox(
			parent,
			label="{description}:\n{flags}".format(
				description=self.description,
				flags=self.flagListLabel,
			)
		)
		checkBox.SetValue(False)
		sHelper.addItem(checkBox)
		self.controls = (checkBox,)

	def makeFlagValueString(self):
		if self.value:
			return self.flagList[-1]
		else:
			return ""


class CommandLineStringOption(CommandLineOption):
	"""A command line option with an associated parameter, i.e. a flag with a value.
	E.g. --lang=en
	"""

	def makeFlagValueString(self):
		val = self.value
		if val:
			# We use the last element of flagList since it is the long form ("--flag=value"), which exists for
			# all the options.
			flagLHS, flagRHS = self.flagList[-1].split('=')
			return flagLHS + '={}'.format(val)
		else:
			return ""


class CommandLineChoiceOption(CommandLineStringOption):

	def __init__(self, choices, *args, **kw):
		super(CommandLineChoiceOption, self).__init__(*args, **kw)
		self.choices = choices

	def addWithGuiHelper(self, parent, sHelper):
		choice = sHelper.addLabeledControl(
			"{description}:\n{flags}".format(description=self.description, flags=self.flagListLabel),
			wx.Choice,
			choices=self.choices,
		)
		choice.SetSelection(0)
		self.controls = (choice,)

	@property
	def value(self):
		# List items are of the form "10 (debug)" or "en - English, en"
		return self.mainControl.StringSelection.split(' ')[0]


class CommandLineLanguageOption(CommandLineChoiceOption):

	def shouldBeDisplayed(self):
		try:
			# Forcing the language from the command line is available in NVDA 2022.1+.
			languageHandler.isLanguageForced
			return True
		except AttributeError:
			return False


class CommandLineFileOption(CommandLineStringOption):

	def addWithGuiHelper(self, parent, sHelper):
		groupSizer = wx.StaticBoxSizer(
			wx.VERTICAL,
			parent,
			label="{description}:   {flags}".format(description=self.description, flags=self.flagListLabel),
		)
		groupBox = groupSizer.GetStaticBox()
		groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(parent, sizer=groupSizer))
		# Translators: The label of a button to browse for a directory or a file.
		browseText = _("Browse...")
		# Translators: the label for the NVDA log extension (log) file type
		wildcard = (_("NVDA log file (*.{ext})") + "|*.{ext}").format(ext="log")
		# Translators: The title of the dialog presented when browsing for the file.
		fileDialogTitle = _("Select a file")
		filePathHelper = FileSelectionHelper(groupBox, browseText, wildcard, fileDialogTitle)
		shouldAddSpacer = groupHelper.hasFirstItemBeenAdded
		if shouldAddSpacer:
			groupHelper.sizer.AddSpacer(gui.guiHelper.SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
		groupHelper.sizer.Add(filePathHelper.sizer, flag=wx.EXPAND)
		groupHelper.hasFirstItemBeenAdded = True
		fileEntryControl = filePathHelper

		fileEdit = fileEntryControl.pathControl
		fileEdit.Value = ""
		self.controls = (fileEdit, fileEntryControl._browseButton)


class CommandLineFolderOption(CommandLineStringOption):

	def addWithGuiHelper(self, parent, sHelper):
		groupSizer = wx.StaticBoxSizer(
			wx.VERTICAL,
			parent,
			label="{description}:   {flags}".format(description=self.description, flags=self.flagListLabel),
		)
		groupBox = groupSizer.GetStaticBox()
		groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(parent, sizer=groupSizer))
		# Translators: The label of a button to browse for a directory or a file.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the directory.
		dirDialogTitle = _("Select a directory")
		directoryPathHelper = gui.guiHelper.PathSelectionHelper(groupBox, browseText, dirDialogTitle)
		directoryEntryControl = groupHelper.addItem(directoryPathHelper)
		directoryEdit = directoryEntryControl.pathControl
		directoryEdit.Value = ""
		self.controls = (directoryEdit, directoryEntryControl._browseButton)


class RestartWithOptionsDialog(gui.settingsDialogs.SettingsDialog):
	# Translators: This is the title for the Restart with options dialog
	title = _("Specify some options and restart")
	helpId = "CommandLineOptions"

	_instance = None

	def __new__(cls, parent):
		# Make this a singleton.
		inst = cls._instance() if cls._instance else None
		if not inst:
			return super(cls, cls).__new__(cls, parent)
		return inst

	def __init__(self, parent):
		inst = RestartWithOptionsDialog._instance() if RestartWithOptionsDialog._instance else None
		if inst:
			return
		# Use a weakref so the instance can die.
		RestartWithOptionsDialog._instance = weakref.ref(self)
		super(RestartWithOptionsDialog, self).__init__(parent)

	OPTION_LIST = [
		CommandLineFileOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("The file where log messages should be written to"),
			flagList=["-&f {LOGFILENAME}", "--log-file={LOGFILENAME}"],
			allowInSecureMode=False,  # Logging in secure mode should be disabled
		),
		CommandLineChoiceOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("The lowest level of message logged"),
			flagList=["-&l {LOGLEVEL}", "--log-level={LOGLEVEL}"],
			allowInSecureMode=False,  # Logging in secure mode should be disabled
			choices=[''] + [
				'{level} ({name})'.format(
					name=name,
					level=level
				) for level, name in gui.settingsDialogs.GeneralSettingsPanel.LOG_LEVELS
			],
		),
		CommandLineFolderOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("The path where all settings for NVDA are stored"),
			flagList=["-&c {CONFIGPATH}", "--config-path={CONFIGPATH}"],
			allowInSecureMode=False,  # Targetting an unauthorized config folder should not be accepted.
		),
		CommandLineLanguageOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("Override the configured NVDA language"),
			flagList=["--lang={LANGUAGE}"],
			allowInSecureMode=True,
			choices=[''] + [
				'{code} - {lng}'.format(
					code=c,
					lng=l
				) for (c, l) in languageHandler.getAvailableLanguages(presentational=True)
			],
		),
		CommandLineBooleanOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("No sounds, no interface, no start message, etc."),
			flagList=["-&m", "--minimal"],
			allowInSecureMode=True,  # Always active on secure screens even if the -m parameter is missing.
		),
		CommandLineBooleanOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("Secure mode"),
			flagList=["-&s", "--secure"],
			allowInSecureMode=True,  # Always active on secure screens even if the -s parameter is missing.
		),
		CommandLineBooleanOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("Add-ons will have no effect"),
			flagList=["--disable-addons"],
			allowInSecureMode=True,  # Restart with add-ons disabled allowed on secure screens by NVDA
		),
		# --debug-logging (Enable debug level logging just for this run. This setting will override any other
		# log level ( --loglevel, -l) argument given, including no logging option.)
		# --no-logging (Disable logging altogether while using NVDA. This setting can be overridden if a log level
		# ( --loglevel, -l) is specified from command line or if debug logging is turned on.)
		CommandLineBooleanOption(
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph
			# "Command Line Options")
			description=_("Don't change the global system screen reader flag"),
			flagList=["--no-sr-flag"],
			allowInSecureMode=True,
		),
		# check? --create-portable (Creates a portable copy of NVDA (starting the newly created copy).
		# Requires --portable-path to be specified)
		# check? --create-portable-silent (Creates a portable copy of NVDA (does not start the newly
		# installed copy). Requires --portable-path to be specified)
		# check? --portable-path=PORTABLEPATH (The path where a portable copy will be created)
	]

	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.options = []
		for option in self.OPTION_LIST:
			if option.shouldBeDisplayed():
				option.addWithGuiHelper(self, sHelper)
				if option.shouldBeDisabled():
					option.disable()
				self.options.append(option)

	def postInit(self):
		# Finally, ensure that focus is on the first option.
		for o in self.options:
			if o.mainControl.IsEnabled():
				o.mainControl.SetFocus()
				break

	def onOk(self, evt):
		options = []
		for option in self.options:
			flagString = option.makeFlagValueString()
			if flagString:
				options.append(flagString)
		queueHandler.queueFunction(queueHandler.eventQueue, restartWithOptions, options)
		super(RestartWithOptionsDialog, self).onOk(evt)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)

	def terminate(self, *args, **kwargs):
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	@script(
		# Translators: Input help mode message for Restart with options command.
		description=_("Restarts NVDA with specific options."),
		gesture="kb:NVDA+shift+q",
		category=ADDON_SUMMARY,
	)
	def script_restartWithOptions(self, gesture):
		wx.CallAfter(self.openRestartWithOptionsDialog)

	@staticmethod
	def openRestartWithOptionsDialog():
		gui.mainFrame.prePopup()
		d = RestartWithOptionsDialog(gui.mainFrame)
		d.Raise()
		d.Show()
		gui.mainFrame.postPopup()
