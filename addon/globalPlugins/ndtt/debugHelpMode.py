# -*- coding: UTF-8 -*-
# debug help mode script for NVDA
# Copyright (C) 2020 Cyrille Bougot
# This file is covered by the GNU General Public License.

# This global plugin allows to also announce unbound script in help mode.
# To use it, put it in the globalPlugins folder.

from types import MethodType

import globalPluginHandler
import scriptHandler

import inputCore
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
		scriptName = scriptHandler.getScriptName(script)
		desc = scriptName
		scriptLocation = scriptHandler.getScriptLocation(script)
		if scriptLocation:
			desc += " on %s" % scriptLocation
		script.__func__.__doc__ = desc
		script.__func__.category = "Scripts without description (modify at your own risk!)"
	res = _originalMethod(gesture, onlyLog)
	#if addDesc:
	#	del script.__func__.__doc__
	return res
		
	
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.debugHelpMode = True
		self.setDebugHelpMode(self.debugHelpMode)
		
	def terminate(self):
		self.debugHelpMode = False
		self.setDebugHelpMode(self.debugHelpMode)
		super(GlobalPlugin, self).terminate()
		
	def setDebugHelpMode(self, enable):
		if enable:
			inputCore.manager._handleInputHelp = MethodType(newHandleInputHelp, _originalMethod.__self__)
			#newHandleInputHelp
		else:
			inputCore.manager._handleInputHelp = _originalMethod
		