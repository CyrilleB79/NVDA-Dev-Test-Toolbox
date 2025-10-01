# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024-2025 Cyrille Bougot
# This file is covered by the GNU General Public License.

import globalPluginHandler
import addonHandler
import ui
from logHandler import log
from scriptHandler import script
import inputCore
import core

from .fileOpener import (
	openCodeFile,
	FileOpenerError,
)

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()

	@script(
		# Translators: Input help mode message for a command.
		description=_("NVDA will open the code of the script of the next gesture instead of executing the corresponding command."),
		category=ADDON_SUMMARY,
	)
	def script_openScriptForNextGesture(self, gesture):
		inputCore.manager._captureFunc = self._openScriptForNextGestureCaptor
		# Translators: Reported when executing the command to open the script corresponding to the next gesture.
		ui.message(_("Execute a gesture to open the code of the corresponding script."))

	def  _openScriptForNextGestureCaptor(self, gesture):
		if gesture.isModifier:
			return False
		inputCore.manager._captureFunc = None
		script = gesture.script
		if script:
			try:
				openCodeFile(script)
			except FileOpenerError as e:
				log.debugWarning(str(e))
				# Call ui.message in the main thread (needed for braille)
				msg = e.getUserFriendlyMessage()
				core.callLater(0, lambda: ui.message(msg))
		else:
			core.callLater(
				0,
				ui.message,
				# Translators: Reported when executing the command to open the script corresponding to the next gesture.
				_("Script not found for {gestureName}".format(gestureName=gesture.displayName)),
			)
		return False

	def terminate(self):
		if inputCore.manager._captureFunc == self._openScriptForNextGestureCaptor:
			inputCore.manager._captureFunc = None
		super(GlobalPlugin, self).terminate()
