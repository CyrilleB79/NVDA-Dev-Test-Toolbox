# -*- coding: UTF-8 -*-
# NVDA add-on: NVDA Dev & Test Toolbox
# Copyright (C) 2023-2026 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import wx

import gui
from gui import guiHelper, nvdaControls
import config
from logHandler import log
import addonHandler
import globalVars
import globalPluginHandler

from .compa import PANEL_DESCRIPTION_WIDTH
from .configNDTT import speakFun
from .utils import getBaseProfileConfigValue

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


PATCHABLE_FUNCTIONS = [
	speakFun,
	"tones.beep",
	"braille.BrailleBuffer.update",
	"nvwave.playWaveFile",
]

class NDTTSettingsPanel(gui.settingsDialogs.SettingsPanel):
	title = ADDON_SUMMARY

	BACKUP_TYPES = [
		# Translators: This is a label of an item for the backup combo box in the NDTT Settings panel.
		('off', _('Off')),
		# Translators: This is a label of an item for the backup combo box in the NDTT Settings panel.
		('maxNumber', _('On')),
	]

	NO_DEFAULT_PROFILE_MESSAGE = _(
		# Translators: A message presented in the settings panel when opened while no-default profile is active.
		"{name} add-on can only be configured from the Normal Configuration profile.\n"
		"Please close this dialog, set your config profile to default and try again."
	).format(name=ADDON_SUMMARY)

	def makeSettings(self, settingsSizer):
		from .functionCallsLogging import logMethodDisplayStrings

		if config.conf.profiles[-1].name is not None or len(config.conf.profiles) != 1:
			self.panelDescription = self.NO_DEFAULT_PROFILE_MESSAGE
			helper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
			textItem = helper.addItem(wx.StaticText(self, label=self.panelDescription.replace('&', '&&')))
			textItem.Wrap(self.scaleSize(PANEL_DESCRIPTION_WIDTH))
			return
		sHelper = guiHelper.BoxSizerHelper(self, sizer=settingsSizer)

		openInEditorCmdLabel = _(
			# Translators: This is a label for an edit field in the NDTT Settings panel.
			'Command to open a file in your favorite editor\n'
			'(use "{path}" and "{line}" placeholders in this command)'
		)
		self.openInEditorCmdEdit = sHelper.addLabeledControl(openInEditorCmdLabel, wx.TextCtrl)
		self.openInEditorCmdEdit.SetValue(config.conf['ndtt']['sourceFileOpener'])

		# Translators: This is a label for an edit field in the NDTT Settings panel.
		nvdaSourceCodePathLabel = _("NVDA source code path")

		groupSizer = wx.StaticBoxSizer(wx.VERTICAL, self, label=nvdaSourceCodePathLabel)
		groupBox = groupSizer.GetStaticBox()
		groupHelper = sHelper.addItem(gui.guiHelper.BoxSizerHelper(self, sizer=groupSizer))
		# Translators: The label of a button to browse for a directory or a file.
		browseText = _("Browse...")
		# Translators: The title of the dialog presented when browsing for the directory.
		dirDialogTitle = _("Select a directory")
		directoryPathHelper = gui.guiHelper.PathSelectionHelper(groupBox, browseText, dirDialogTitle)
		directoryEntryControl = groupHelper.addItem(directoryPathHelper)
		self.nvdaSourceCodePathEdit = directoryEntryControl.pathControl
		self.nvdaSourceCodePathEdit.Value = config.conf['ndtt']['nvdaSourcePath']

		# Translators: This is a label for the combo box in the NDTT Settings panel.
		text = _("Backup of old logs:")
		self.makeBackupsList = sHelper.addLabeledControl(
			text,
			wx.Choice,
			choices=[label for val, label in self.BACKUP_TYPES],
		)
		val = getBaseProfileConfigValue('ndtt', 'logBackup')
		index = [v for v, l in self.BACKUP_TYPES].index(val)
		self.makeBackupsList.Select(index)
		backupType = self.BACKUP_TYPES[index][0]
		self.makeBackupsList.Bind(wx.EVT_CHOICE, self.onMakeBackupsListItemChanged)

		minNbBackups = int(self.getParameterBound("logBackupMaxNumber", "min"))
		maxNbBackups = int(self.getParameterBound("logBackupMaxNumber", "max"))

		# Translators: This is a label for a setting in the settings panel
		text = _("Limit the number of backups to:")
		self.nbBackupsEdit = sHelper.addLabeledControl(
			text,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minNbBackups,
			max=maxNbBackups,
			initial=getBaseProfileConfigValue('ndtt', 'logBackupMaxNumber'),
		)
		self.updateNbBackupsEdit(backupType)

		# Translators: This is a label for a setting in the settings panel
		self.copyReverseTranslation = wx.CheckBox(self, label=_("Copy reverse &translation to clipboard"))
		self.copyReverseTranslation.SetValue(
			config.conf['ndtt']['copyRevTranslation']
			and not globalVars.appArgs.secure
		)
		if globalVars.appArgs.secure:
			self.copyReverseTranslation.Disable()
		sHelper.addItem(self.copyReverseTranslation)

		self.preserveConsoleInputHistory = wx.CheckBox(
			self,
			# Translators: This is a label for a setting in the settings panel
			label=_("Preserve console input history after restart"),
		)
		self.preserveConsoleInputHistory.SetValue(
			config.conf["ndtt"]["preserveConsoleInputHistory"]
		)
		self.preserveConsoleInputHistory.Bind(wx.EVT_CHECKBOX, self.onSaveConsoleInputHistoryModified)
		sHelper.addItem(self.preserveConsoleInputHistory)
		
		minConsoleHistorySize = int(self.getParameterBound("consoleInputHistorySize", "min"))
		maxConsoleHistorySize = int(self.getParameterBound("consoleInputHistorySize", "max"))
		# Translators: This is a label for a setting in the settings panel
		text = _("Number of inputs preserved in Python console history")
		self.nbPreservedInputsEdit = sHelper.addLabeledControl(
			text,
			nvdaControls.SelectOnFocusSpinCtrl,
			min=minConsoleHistorySize,
			max=maxConsoleHistorySize,
			initial=getBaseProfileConfigValue("ndtt", "consoleInputHistorySize"),
		)
		self.nbPreservedInputsEdit.Enable(self.preserveConsoleInputHistory.GetValue())
		
		self.functionsChoices = [name for name in PATCHABLE_FUNCTIONS]
		# Translators: This is a label for a combo box in the NDTT Settings panel.
		self.customFunctionChoice = "<{}>".format(_("Custom function"))
		self.functionsChoices.append(self.customFunctionChoice)
		self.functionCallsLogTarget = sHelper.addLabeledControl(
			# Translators: This is a label for a setting in the settings panel
			_("Target function for function call logging:"),
			wx.Choice,
			choices=self.functionsChoices,
		)
		
		self.customFunctionLabel = _(
			# Translators: This is a label for an edit field in the NDTT Settings panel.
			"Custom function for stack tracing:",
		)
		self.customFunction = sHelper.addLabeledControl(self.customFunctionLabel, wx.TextCtrl)
		
		val = getBaseProfileConfigValue("ndtt", "functionCallsLogTarget")
		if val in self.functionsChoices:
			self.functionCallsLogTarget.StringSelection = val
			self.customFunction.SetValue("")
		else:
			self.functionCallsLogTarget.StringSelection = self.customFunctionChoice
			self.customFunction.SetValue(val)
		
		self.functionCallsLogTarget.Bind(wx.EVT_CHOICE, self.onFunctionCallsLogTargetChanged)		
		self.onFunctionCallsLogTargetChanged()

		# Translators: This is a label for the combo box in the NDTT Settings panel.
		text = _("Function call log method:")
		self.functionCallsLogMethodsList = sHelper.addLabeledControl(
			text,
			wx.Choice,
			choices=[label for val, label in logMethodDisplayStrings],
		)
		val = getBaseProfileConfigValue("ndtt", "functionCallsLogMethod")
		index = [val for val, label in logMethodDisplayStrings].index(val)
		self.functionCallsLogMethodsList.Select(index)

	@staticmethod
	def getParameterBound(name, boundType):
		"""Gets the bound of a parameter in the "ndtt" section of the config.
		@param name: the name of the paremeter
		@type name: str
		@param boundType: "min" or "max"
		@type boundType: str
		"""

		try:
			return config.conf.getConfigValidation(("ndtt", name)).kwargs[boundType]
		except TypeError:
			# For older version of configObj (e.g. used in NVDA 2019.2.1)
			return config.conf.getConfigValidationParameter(["ndtt", name], boundType)

	def onMakeBackupsListItemChanged(self, evt):
		index = evt.GetSelection()
		self.updateNbBackupsEdit(self.BACKUP_TYPES[index][0])

	def onSaveConsoleInputHistoryModified(self, evt):
		self.nbPreservedInputsEdit.Enable(evt.IsChecked())

	def updateNbBackupsEdit(self, backupType):
		self.nbBackupsEdit.Enable(backupType == 'maxNumber')

	def onFunctionCallsLogTargetChanged(self, evt=None):
		val = self.functionCallsLogTarget.StringSelection
		if val == self.customFunctionChoice:
			self.customFunction.Enable()
		else:
			self.customFunction.Disable()
				

	def onSave(self):
		from .functionCallsLogging import logMethodDisplayStrings
		# Make sure we're operating in the "normal" profile
		if not (config.conf.profiles[-1].name is None and len(config.conf.profiles) == 1):
			log.debugWarning("No configuration saved for NDTT since the current profile is not the default one.")
			return
		config.conf['ndtt']['sourceFileOpener'] = self.openInEditorCmdEdit.GetValue()
		config.conf['ndtt']['nvdaSourcePath'] = self.nvdaSourceCodePathEdit.GetValue()
		config.conf['ndtt']['logBackup'] = self.BACKUP_TYPES[self.makeBackupsList.Selection][0]
		config.conf['ndtt']['logBackupMaxNumber'] = int(self.nbBackupsEdit.Value)
		if not globalVars.appArgs.secure:
			config.conf['ndtt']['copyRevTranslation'] = self.copyReverseTranslation.IsChecked()
		config.conf["ndtt"]["preserveConsoleInputHistory"] = self.preserveConsoleInputHistory.GetValue()
		config.conf["ndtt"]["consoleInputHistorySize"] = int(self.nbPreservedInputsEdit.Value)
		if not config.conf["ndtt"]["preserveConsoleInputHistory"]:
			plugin = [p for p in globalPluginHandler.runningPlugins if p.__module__ == "globalPlugins.ndtt"][0]
			plugin.deleteInputHistory()
		val = self.functionCallsLogTarget.StringSelection
		if val == self.customFunctionChoice:
			config.conf["ndtt"]["functionCallsLogTarget"] = self.customFunction.GetValue()
		else:
			config.conf["ndtt"]["functionCallsLogTarget"] = val
		config.conf["ndtt"]["functionCallsLogMethod"] = logMethodDisplayStrings[self.functionCallsLogMethodsList.Selection][0]
