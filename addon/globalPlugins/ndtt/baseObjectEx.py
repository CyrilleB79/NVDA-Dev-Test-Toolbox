# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from baseObject import ScriptableObject
from scriptHandler import script
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


class ScriptableObjectWithLayer(ScriptableObject):
	def __init__(self):
		super(ScriptableObjectWithLayer, self).__init__()
		self.toggling = False

	def getScript(self, gesture):
		if not self.toggling:
			#zzz return globalPluginHandler.GlobalPlugin.getScript(self, gesture)
			#zzz return ScriptableObject.getScript(self, gesture)
			return super(ScriptableObjectWithLayer, self).getScript(gesture)
		#zzz script = ScriptableObject.getScript(self, gesture)
		#zzz script = super(ScriptableObjectWithLayer, self).getScript(gesture)
		script = super(ScriptableObjectWithLayer, self).getScript(gesture)
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

	def createLayeredCommandEntryPoint(
		self,
		layerCommandList,
		**kwargs,
	):
		@script(
			**kwargs,
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
		setattr(self, 'script_enterLayer', script_enterLayer)
		try:
			gesture = kwargs['gesture']
			self.bindGesture(gesture, 'enterLayer')
		except KeyError:
			pass

	def terminate(self):
		super(ScriptableObjectWithLayer, self).terminate()	