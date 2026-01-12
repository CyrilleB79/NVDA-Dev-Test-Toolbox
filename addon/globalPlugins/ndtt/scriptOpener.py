# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024-2026 Cyrille Bougot
# This file is covered by the GNU General Public License.

import re

import globalPluginHandler
import addonHandler
import ui
import api
import treeInterceptorHandler
import textInfos
from logHandler import log
from scriptHandler import script
import inputCore
import core

from .fileOpener import (
	openCodeFile,
	openSourceFile,
	FileOpenerError,
)

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


RE_PATH = re.compile(
	r"""
	(?P<path>
	"[A-Za-z]:\\[^":]+"
	|[A-Za-z]:(?:\\[^\\\s":]+)+
	)
	(?::(?P<line>\d+)(?::(?P<column>\d+))?)?
	(?=\s|$)
	""",
	re.VERBOSE,
)


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

	@script(
		# Translators: Input help mode message for a command.
		description=_("Opens the code of the path at the position of the cursor"),
		category=ADDON_SUMMARY,
	)
	def script_openSourcePathAtCaret(self, gesture):
		obj = api.getFocusObject()
		treeInterceptor = obj.treeInterceptor
		if (
			isinstance(treeInterceptor, treeInterceptorHandler.DocumentTreeInterceptor)
			and not treeInterceptor.passThrough
		):
			obj = treeInterceptor
		try:
			info = obj.makeTextInfo(textInfos.POSITION_CARET)
		except (NotImplementedError, RuntimeError):
			info = obj.makeTextInfo(textInfos.POSITION_FIRST)
		info.expand(textInfos.UNIT_LINE)
		for match in RE_PATH.finditer(info.text):
			path = match.group("path")
			if path.startswith('"') and path.endswith('"'):
				path = path[1:-1]
			line = match.group("line")
			column = match.group("column")
			break
		else:
			# Translators: Reported when executing the command to open the source code at the path/line at the caret position.
			ui.message(_("No path on this line"))
			return
		try:
			openSourceFile(path, line)
		except FileOpenerError as e:
			log.debugWarning(str(e))
			# Call ui.message in the main thread (needed for braille)
			msg = e.getUserFriendlyMessage()
			core.callLater(0, lambda: ui.message(msg))

	def terminate(self):
		if inputCore.manager._captureFunc == self._openScriptForNextGestureCaptor:
			inputCore.manager._captureFunc = None
		super(GlobalPlugin, self).terminate()
