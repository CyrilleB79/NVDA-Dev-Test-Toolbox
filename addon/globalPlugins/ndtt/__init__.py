# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020-2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import wx

import globalVars
import globalPluginHandler
from scriptHandler import script
import addonHandler
import gui
from tones import beep

from .layeredGestures import ScriptableObjectWithLayeredGestures

# Initialize config spec; should be done before GlobalPlugins import
from . import configNDTT  # noqa: F401 - Required to initialize config spec.

from .ndttGui import NDTTSettingsPanel

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
	from .scriptOpener import GlobalPlugin as ScriptOpenerGP  # Do not open any editor in secure mode.

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


NDTT_LAYERED_COMMANDS_LIST = [
	# A list of 3-tuples. Each 3-tuple contains:
	# - a gesture list
	# - the associated script name
	# - if the command is available in secure mode.
	(["c"], "openScriptForNextGesture", False),
	(["d"], "toggleESDMode", True),
	(["e"], "reportLastError", False),
	(["shift+e"], "togglePlayErrorSound", False),
	(["k"], "addMarkerInLog", False),
	(["l"], "toggleLogReadingCommands", False),
	(["n"], "announceObjectInfo", True),
	(["shift+n"], "displayObjectInfo", False),
	(["upArrow"], "nextObjectInfo", True),
	(["downArrow"], "priorObjectInfo", True),
	(["control+n"], "toggleCustomObjectReporting", True),
	(["q"], "restartWithOptions", True),
	(["r"], "reverseUITranslation", True),
	(["s"], "toggleStackTraceLog", False),
	(["o"], "openSettings", False),
	(["h"], "displayHelp", True),
]


if globalVars.appArgs.secure:

	class MixedGlobalPlugin(
			ScriptableObjectWithLayeredGestures(
				scriptableObjectName=ADDON_SUMMARY,
				entryPointGestures=["kb:NVDA+x"],
			),
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
			ReverseUITranslationGP,
	):
		pass

else:
	class MixedGlobalPlugin(
			ScriptableObjectWithLayeredGestures(
				scriptableObjectName=ADDON_SUMMARY,
				entryPointGestures=["kb:NVDA+x"],
			),
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
			ReverseUITranslationGP,
			BeepErrorGP,
			StackTracingGP,
			logManagement.GlobalPlugin,
			LogReaderGP,
			PythonConsoleExGP,
			ScriptOpenerGP,
	):
		pass


class MixedGlobalPluginWithInit(MixedGlobalPlugin):
	def __init__(self):
		super(MixedGlobalPluginWithInit, self).__init__(
			layeredCommandsList=[(gestures, script) for (gestures, script, sec) in NDTT_LAYERED_COMMANDS_LIST if (not globalVars.appArgs.secure) or sec],
		)	


def useAlternativeClassInSecureMode(safeClass):
	def decorator(decoratedClass):
		if globalVars.appArgs.secure:
			return safeClass
		else:
			return decoratedClass
	return decorator


@useAlternativeClassInSecureMode(MixedGlobalPluginWithInit)
class GlobalPlugin(MixedGlobalPluginWithInit):
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		# Gui initialization
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(NDTTSettingsPanel)

	def terminate(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(NDTTSettingsPanel)
		super(GlobalPlugin, self).terminate()

	@script(
		# Translators: The description of a command of this add-on.
		description=_("Opens {name} settings").format(name=ADDON_SUMMARY),
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
