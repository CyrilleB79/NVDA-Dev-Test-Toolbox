# -*- coding: UTF-8 -*-
# debug help mode script for NVDA
# Copyright (C) 2020-2021 Cyrille Bougot
# This file is covered by the GNU General Public License.

# This global plugin allows to also announce unbound script in help mode.
# To use it, put it in the globalPlugins folder.

from types import MethodType

import globalPluginHandler
import addonHandler
import scriptHandler
from scriptHandler import script
import inputCore
import ui

ADDON_SUMMARY = addonHandler.getCodeAddon ().manifest["summary"]

SCRIPT_WITHOUT_DESC_CATEGORY = _("Scripts without description (modify at your own risk!)")

_originalMethod = inputCore.manager._handleInputHelp

def newHandleInputHelp(self, gesture, onlyLog=False):
	script = gesture.script
	scriptName = scriptHandler.getScriptName(script) if script else ''
	addDesc = (
		# The script must exist
		script
		# And the script must not be input help script
		and scriptName != "toggleInputHelp"
		# And the script must not have already a description.
		and not getattr(script, '__doc__', None)
	)
	if addDesc:
		desc = scriptName
		scriptLocation = scriptHandler.getScriptLocation(script)
		if scriptLocation:
			desc += " on %s" % scriptLocation
		script.__func__.__doc__ = desc
		script.__func__.category = SCRIPT_WITHOUT_DESC_CATEGORY
		GlobalPlugin.scriptsWithAddedDoc.add(script)
	res = _originalMethod(gesture, onlyLog)
	#if addDesc:
	#	del script.__func__.__doc__
	#	del script.__func__.category
	return res
		
	
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptsWithAddedDoc = set()
	
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.configureDebugHelpMode(False, silent=True)
		
	def terminate(self):
		self.configureDebugHelpMode(False, silent=True)
		super(GlobalPlugin, self).terminate()
		
	@script(
		description = "Toggle debug help mode.",
		gesture = "kb:nvda+control+alt+H",
		category = ADDON_SUMMARY,
	)
	def script_tobbleDebugHelpMode(self, gesture):
		self.configureDebugHelpMode(not self.debugHelpMode)
	
	def configureDebugHelpMode(self, enable, silent=False):
		self.debugHelpMode = enable
		if enable:
			inputCore.manager._handleInputHelp = MethodType(newHandleInputHelp, _originalMethod.__self__)
			msg = 'Debug help mode enabled'
		else:
			inputCore.manager._handleInputHelp = _originalMethod
			msg = 'Debug help mode disabled'
			for script in self.__class__.scriptsWithAddedDoc:
				del script.__func__.__doc__
				del script.__func__.category
			self.__class__.scriptsWithAddedDoc.clear()
		if not silent:
			ui.message(msg)
		