# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from functools import wraps

from baseObject import ScriptableObject
from scriptHandler import script
from tones import beep
import addonHandler

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



def ScriptableObjectWithLayer(layerCommandList, **kwargs):
	class _ScriptableObjectWithLayer(ScriptableObject):
		def __init__(self):
			super(_ScriptableObjectWithLayer, self).__init__()
			self.toggling = False

		def getScript(self, gesture):
			if not self.toggling:
				#zzz return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
				#zzz return ScriptableObject.getScript(self, gesture)
				return super(_ScriptableObjectWithLayer, self).getScript(gesture)
			#zzz script = ScriptableObject.getScript(self, gesture)
			#zzz script = super(_ScriptableObjectWithLayer, self).getScript(gesture)
			script = super(_ScriptableObjectWithLayer, self).getScript(gesture)
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
				**kwargs
			)
			def script_enterLayer(self, gesture):
				# A run-time binding will occur from which we can perform various layered commands.
				# First, check if a second press of the script was done.
				if self.toggling:
					self.script_error(gesture)
					return
				layerGestures = {}
				for (gestures, command, desc) in layerCommandList:
					for g in gestures:
						layerGestures["kb:" + g] = command
				self.bindGestures(layerGestures)
				self.toggling = True
				beep(100, 10)
	return _ScriptableObjectWithLayer
