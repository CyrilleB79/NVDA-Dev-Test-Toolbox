# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020-2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import wx

import globalVars
from scriptHandler import script
import addonHandler
import gui

# Initialize config spec; should be done before GlobalPlugins import
from . import configNDTT  # noqa: F401 - Required to initialize config spec.

from .ndttGui import NDTTSettingsPanel

# Plugins that may be used in any context, including secure context.
from .extScriptDesc import GlobalPlugin as ExtScriptDescGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .objPropExplorer import GlobalPlugin as ObjPropExplorerGP


if not globalVars.appArgs.secure:
	# Plugins that may be used only in normal context, not in secure context.
	from .beepError import GlobalPlugin as BeepErrorGP  # No error tone in secure mode
	from .stackTracing import GlobalPlugin as StackTracingGP  # No log nor log viewer in secure mode
	from . import logManagement  # No log in secure mode.
	from .logReader import GlobalPlugin as LogReaderGP  # No log nor log viewer in secure mode.
	from .pythonConsoleEx import GlobalPlugin as PythonConsoleExGP  # No Python console in secure mode

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

if globalVars.appArgs.secure:

	class MixedGlobalPlugin(
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
	):
		pass

else:
	class MixedGlobalPlugin(
			ExtScriptDescGP,
			RestartWithOptionsGP,
			ObjPropExplorerGP,
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
		super(MixedGlobalPlugin, self).__init__()
		# Gui initialization
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(NDTTSettingsPanel)

	def terminate(self):
		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(NDTTSettingsPanel)
		super(MixedGlobalPlugin, self).terminate()

	@script(
		# Translators: The description of a command of this add-on.
		description=_("Opens NVDA Dev & Test Toolbox add-on settings"),
		category=ADDON_SUMMARY,
	)
	def script_openSettings(self, gesture):
		wx.CallAfter(
			gui.mainFrame._popupSettingsDialog,
			gui.settingsDialogs.NVDASettingsDialog,
			NDTTSettingsPanel,
		)

	if not globalVars.appArgs.secure:
		def chooseNVDAObjectOverlayClasses(self, obj, clsList):
			# We need to call explicitely chooseNVDAObjectOverlayClasses of the child class; else NVDA will skip them.
			LogReaderGP.chooseNVDAObjectOverlayClasses(self, obj, clsList)
