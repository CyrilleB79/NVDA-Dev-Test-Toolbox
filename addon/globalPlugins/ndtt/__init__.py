# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020-2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from functools import wraps
import wx

import globalVars
import globalPluginHandler
from scriptHandler import script
import addonHandler
import gui
from tones import beep
from keyLabels import localizedKeyLabels

# Initialize config spec; should be done before GlobalPlugins import
from . import configNDTT  # noqa: F401 - Required to initialize config spec.

from .ndttGui import NDTTSettingsPanel
from .securityUtils import secureBrowseableMessage

# Plugins that may be used in any context, including secure context.
from .extScriptDesc import GlobalPlugin as ExtScriptDescGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .objPropExplorer import GlobalPlugin as ObjPropExplorerGP
from .reverseUITranslation import GlobalPlugin as ReverseUITranslationGP


if not globalVars.appArgs.secure:
	# Plugins that may be used only in normal context, not in secure context.
	from .beepError import GlobalPlugin as BeepErrorGP  # No error tone in secure mode
	from .stackTracing import GlobalPlugin as StackTracingGP  # No log nor log viewer in secure mode
	from . import logManagement  # No log in secure mode.
	from .logReader import GlobalPlugin as LogReaderGP  # No log nor log viewer in secure mode.
	from .pythonConsoleEx import GlobalPlugin as PythonConsoleExGP  # No Python console in secure mode

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


# Below toggle code came from Tyler Spivey's code, with enhancements by Joseph Lee.
def finally_(func, final):
	"""Calls final after func, even if it fails."""
	def wrap(f):
		@wraps(f)
		def new(*args, **kwargs):
			try:
				func(*args, **kwargs)
			finally:
				final()
		return new
	return wrap(final)


class NDTTLayeredScriptsGlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptCategory = ADDON_SUMMARY

	def __init__(self):
		super(NDTTLayeredScriptsGlobalPlugin, self).__init__()
		_layerCommandList = [
			(["d"], "toggleESDMode"),
			(["e"], "reportLastError"),
			(["shift+e"], "togglePlayErrorSound"),
			(["k"], "addMarkerInLog"),
			(["o"], "announceObjectInfo"),
			(["upArrow"], "nextObjectInfo"),
			(["downArrow"], "priorObjectInfo"),
			(["shift+o"], "toggleCustomObjectReporting"),
			(["q"], "restartWithOptions"),
			(["r"], "reverseUITranslation"),
			(["so"], "toggleStackTraceLog"),
			(["p"], "openSettings"),
			(["h"], "displayHelp"),
		]
		self.layerCommandList = []
		for gesturesList, scriptName in _layerCommandList:
			try:
				script = getattr(self, "script_{}".format(scriptName))
			except AttributeError:  # In case the script is not defined due to secure mode.
				continue
			self.layerCommandList.append(
				(gesturesList, scriptName, script.__doc__),
			)
		self.toggling = False

	def getScript(self, gesture):
		if not self.toggling:
			return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		script = globalPluginHandler.GlobalPlugin.getScript(self, gesture)
		if not script:
			script = finally_(self.script_error, self.finish)
		if getattr(script, 'allowMultipleLayeredCommands', None):
			return script
		else:
			return finally_(script, self.finish)

	def finish(self):
		self.toggling = False
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)

	def script_error(self, gesture):
		beep(120, 100)

	@script(
		# Translators: Part of the description for the layered command script.
		description=_("NVDA Dev & Test Toolbox layer commands entry point."),
		gesture="kb:NVDA+X",
	)
	def script_ndttLayer(self, gesture):
		# A run-time binding will occur from which we can perform various layered commands.
		# First, check if a second press of the script was done.
		if self.toggling:
			self.script_error(gesture)
			return
		layerGestures = {}
		for (gestures, command, desc) in self.layerCommandList:
			for g in gestures:
				layerGestures["kb:" + g] = command
		self.bindGestures(layerGestures)
		self.toggling = True
		beep(100, 10)

	@script(
		# Translators: The description of a command of this add-on.
		description=_("Displays help on NVDA Dev & Test Toolbox layer commands"),
	)
	def script_displayHelp(self, gesture):
		# Translators: Title of the layered command help window.
		title = _("NVDA Dev & Test Toolbox layered commands")
		cmdList = []
		for (gestures, command, desc) in self.layerCommandList:
			cmdParts = []
			cmdParts.append(
				# Translators: Separator between key names in the layered command help window.
				_(', ').join(
					'+'.join(
						localizedKeyLabels.get(k.lower(), k) for k in gesture.split('+')
					) for gesture in gestures
				)
			)
			cmdParts.append(': ')
			cmdParts.append(desc)
			cmdList.append(''.join(cmdParts))
		cmdList = '\r'.join(cmdList)
		# Translators: Part of the help message displayed for the layered command help.
		msg = _("NVDA Dev & Test Toolbox layer commands:\n{cmdList}").format(cmdList=cmdList)
		secureBrowseableMessage(msg, title)



if globalVars.appArgs.secure:

	class MixedGlobalPlugin(
			NDTTLayeredScriptsGlobalPlugin,
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
			ReverseUITranslationGP,
	):
		pass

else:
	class MixedGlobalPlugin(
			NDTTLayeredScriptsGlobalPlugin,
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
			ReverseUITranslationGP,
			BeepErrorGP,
			StackTracingGP,
			logManagement.GlobalPlugin,
			LogReaderGP,
			PythonConsoleExGP
	):
		pass


def useAlternativeClassInSecureMode(safeClass):
	def decorator(decoratedClass):
		if globalVars.appArgs.secure:
			return safeClass
		else:
			return decoratedClass
	return decorator


@useAlternativeClassInSecureMode(MixedGlobalPlugin)
class GlobalPlugin(MixedGlobalPlugin):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Gui initialization
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(NDTTSettingsPanel)

	def terminate(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(NDTTSettingsPanel)
		super(GlobalPlugin, self).terminate()

	@script(
		# Translators: The description of a command of this add-on.
		description=_("Opens NVDA Dev & Test Toolbox add-on settings"),
		category=ADDON_SUMMARY,
	)
	def script_openSettings(self, gesture):
		try:
			# For NVDA >= 2023.2
			popupSettingsDialog = gui.mainFrame.popupSettingsDialog
		except AttributeError:
			# For NVDA <= 2023.1
			popupSettingsDialog = gui.mainFrame._popupSettingsDialog
		wx.CallAfter(
			popupSettingsDialog,
			gui.settingsDialogs.NVDASettingsDialog,
			NDTTSettingsPanel,
		)

	if not globalVars.appArgs.secure:
		def chooseNVDAObjectOverlayClasses(self, obj, clsList):
			# We need to call explicitely chooseNVDAObjectOverlayClasses of the child class; else NVDA will skip them.
			LogReaderGP.chooseNVDAObjectOverlayClasses(self, obj, clsList)
