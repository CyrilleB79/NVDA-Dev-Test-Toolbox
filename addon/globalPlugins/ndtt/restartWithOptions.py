# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

import gui
import queueHandler
import core
import globalVars
import globalPluginHandler
from scriptHandler import script
import languageHandler

import wx
import sys
import os

from types import MethodType

def restartWithOptions(options):
	"""Restarts NVDA by starting a new copy, providing some options."""
	if globalVars.appArgs.launcher:
		import gui
		globalVars.exitCode=3
		gui.safeAppExit()
		return
	import subprocess
	import winUser
	import shellapi
	if not hasattr(sys, "frozen"):
		options.insert(0, os.path.basename(sys.argv[0]))
	shellapi.ShellExecute(
		hwnd=None,
		operation=None,
		file=sys.executable,
		parameters=subprocess.list2cmdline(options),
		directory=globalVars.appDir,
		# #4475: ensure that the first window of the new process is not hidden by providing SW_SHOWNORMAL
		showCmd=winUser.SW_SHOWNORMAL
	)


class SecuredPathSelectionHelper(gui.guiHelper.PathSelectionHelper):
	"""A PathSelectionHelper usable on secure screen. The browse button is then disabled.
	"""
	
	def __init__(self, parent, buttonText, browseForDirectoryTitle):
		super().__init__(parent, buttonText, browseForDirectoryTitle)
		if globalVars.appArgs.secure:
			self._browseButton.Disable()

class SecuredFileSelectionHelper(object):
	"""
	Abstracts away details for creating a file selection helper. The file selection helper is a textCtrl with a
	button in horizontal layout. The Button launches a file explorer. To get the path selected by the user, use the
	`pathControl` property which exposes a wx.TextCtrl.
	For security concerns, the button is disabled in secure environment.
	"""
	def __init__(self, parent, buttonText, wildcard, browseForFileTitle):
		""" @param parent: An instance of the parent wx window. EG wx.Dialog
			@param buttonText: The text for the button to launch a file selection dialog (wx.DirDialog). This is typically 'Browse'
			@type buttonText: string
			@param wildcard: The text for the title of the file dialog (wx.FileDialog)
			@type browseForDirectoryTitle: string
			@param browseForFileTitle: The text for the title of the file dialog (wx.FileDialog)
			@type browseForDirectoryTitle: string
		"""
		object.__init__(self)
		self._textCtrl = wx.TextCtrl(parent)
		self._browseButton = wx.Button(parent, label=buttonText)
		if globalVars.appArgs.secure:
			self._browseButton.Disable()
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
		# Translators: The title of a file selector window
		filename = wx.FileSelector(_("Save As"), default_path=startPath, default_filename="nvda.log", wildcard=self._wildcard, flags=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT, parent=self._parent)
		if filename:
			self._textCtrl.Value = filename


class FolderStr(str):
	pass
class FileStr(str):
	pass
class LangStr(str):
	pass
class LogLevelStr(str):
	pass

class RestartWithOptionsDialog(gui.settingsDialogs.SettingsDialog):
	# Translators: This is the title for the Restart with options dialog
	title = _("Specify some options and restart")
	helpId = "CommandLineOptions"
	
	# Check the possibility of forcing the language from the command line (NVDA 2022.1+)
	# to decide if the language option should be added.
	try:
		languageHandler.isLanguageForced
	except AttributeError:
		langOptList = []
	else:
		langOptList = [[
			"Override the configured NVDA language",
			["--lang={LANGUAGE}"],
			LangStr(""),
		]]
	
	OPTION_LIST = [
		[
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"The file where log messages should be written to",
			["-&f {LOGFILENAME}", "--log-file={LOGFILENAME}"],
			FileStr(""),
		], [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"The lowest level of message logged", #(debug 10, input/output 12, debug warning 15, info 20, warning 30, error 40, critical 50, disabled 100), default is warning
			["-&l {LOGLEVEL}", "--log-level={LOGLEVEL}"],
			LogLevelStr(""),
		], [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"The path where all settings for NVDA are stored",
			["-&c {CONFIGPATH}", "--config-path={CONFIGPATH}"],
			FolderStr(""),
		], *langOptList, [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"No sounds, no interface, no start message, etc.",
			["-&m", "--minimal"],
			False,
		], [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"Secure mode",
			["-&s", "--secure"],
			False
		], [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"Add-ons will have no effect",
			["--disable-addons"],
			False,
		# --debug-logging (Enable debug level logging just for this run. This setting will override any other log level ( --loglevel, -l) argument given, including no logging option.)
		# --no-logging (Disable logging altogether while using NVDA. This setting can be overridden if a log level ( --loglevel, -l) is specified from command line or if debug logging is turned on.)
		], [
			# Translators: The description of an NVDA start option, copied from the user guide (paragraph Command Line Options)
			"Don't change the global system screen reader flag",
			["--no-sr-flag"],
			False,
		#check? --create-portable (Creates a portable copy of NVDA (starting the newly created copy). Requires --portable-path to be specified)
		#check? --create-portable-silent (Creates a portable copy of NVDA (does not start the newly installed copy). Requires --portable-path to be specified)
		#check? --portable-path=PORTABLEPATH (The path where a portable copy will be created)
		]
	]
	def makeSettings(self, settingsSizer):
		sHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self.options = []
		for (label, flagList, defaultValue) in self.OPTION_LIST:
			flagList = " ".join(flagList)
			flagList = flagList.replace('{', '').replace('}', '')
			if isinstance(defaultValue, bool):
				checkBox = wx.CheckBox(self, label="{label}:\n{flags}".format(label=label, flags=flagList))
				checkBox.SetValue(defaultValue)
				sHelper.addItem(checkBox)
				self.options.append(checkBox)
			elif isinstance(defaultValue, LogLevelStr):
				logLevelChoices = ['{level} ({name})'.format(name=name, level=level) for level, name in gui.settingsDialogs.GeneralSettingsPanel.LOG_LEVELS]
				logLevelChoices.insert(0, '')
				logLevelList = sHelper.addLabeledControl("{label}:\n{flags}".format(label=label, flags=flagList), wx.Choice, choices=logLevelChoices)
				logLevelList.SetSelection(0)
				self.options.append(logLevelList)
			elif isinstance(defaultValue, LangStr):
				self.languages = languageHandler.getAvailableLanguages(presentational=True)
				langChoices = ['{code} - {lng}'.format(code=c, lng=l) for (c, l) in self.languages]
				langChoices.insert(0, '')
				langList = sHelper.addLabeledControl("{label}:\n{flags}".format(label=label, flags=flagList), wx.Choice, choices=langChoices)
				langList.SetSelection(0)
				self.options.append(langList)
			elif isinstance(defaultValue, str):
				groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label="{label}:   {flags}".format(label=label, flags=flagList))
				groupBox = groupSizer.GetStaticBox()
				groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
				# Translators: The label of a button to browse for a directory or a file.
				browseText = _("Browse...")
				if isinstance(defaultValue, FolderStr):
					# Translators: The title of the dialog presented when browsing for the directory.
					dirDialogTitle = _("Select a directory")
					directoryPathHelper = SecuredPathSelectionHelper(groupBox, browseText, dirDialogTitle)
					directoryEntryControl = groupHelper.addItem(directoryPathHelper)
					directoryEdit = directoryEntryControl.pathControl
					directoryEdit.Value = defaultValue
					self.options.append(directoryEdit)		
				elif isinstance(defaultValue, FileStr):
					# Translators: the label for the NVDA log extension (log) file type
					wildcard = (_("NVDA log file (*.{ext})")+"|*.{ext}").format(ext="log")
					# Translators: The title of the dialog presented when browsing for the file.
					fileDialogTitle = _("Select a file")
					filePathHelper = SecuredFileSelectionHelper(groupBox, browseText, wildcard, fileDialogTitle)
					shouldAddSpacer = groupHelper.hasFirstItemBeenAdded
					if shouldAddSpacer:
						groupHelper.sizer.AddSpacer(SPACE_BETWEEN_VERTICAL_DIALOG_ITEMS)
					groupHelper.sizer.Add(filePathHelper.sizer, flag=wx.EXPAND)
					groupHelper.hasFirstItemBeenAdded = True
					fileEntryControl = filePathHelper
					
					fileEdit = fileEntryControl.pathControl
					fileEdit.Value = defaultValue
					self.options.append(fileEdit)		
				else:
					raise			
			else:
				raise Exception('Unknown option type')

	def postInit(self):
		# Finally, ensure that focus is on the first option.
		self.options[0].SetFocus()

	def onOk(self, evt):
		options = []
		for (ctrl, optionInfo) in zip(self.options, self.OPTION_LIST):
			try:
				value = ctrl.Value
			except AttributeError:
				value = ctrl.StringSelection.split(' ')[0]
			if value:
				splitFlag = optionInfo[1][-1].split('=')
				flag = splitFlag[0]
				if len(splitFlag) == 1:
					pass
				elif len(splitFlag) == 2:
					flag = flag + '={}'.format(value)
				else:
					raise ValueError('Unexpected value {}'.format(optionInfo[1][-1]))
				options.append(flag)
		queueHandler.queueFunction(queueHandler.eventQueue, restartWithOptions, options)
		super(RestartWithOptionsDialog, self).onOk(evt)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		
	def terminate(self, *args, **kwargs):
		super(GlobalPlugin, self).terminate(*args, **kwargs)
	
	@script(
		# Translators: Input help mode message for Restart with options command.
		description=_("Restart NVDA with specific options."),
		gesture="kb:NVDA+shift+q"
	)
	def script_restartWithOptions(self,gesture):
		wx.CallAfter(self.openRestartWithOptionsDialog)
		
	@staticmethod
	def openRestartWithOptionsDialog():
		gui.mainFrame.prePopup()
		d = RestartWithOptionsDialog(gui.mainFrame)
		d.Raise()
		d.Show()
		gui.mainFrame.postPopup()		
		