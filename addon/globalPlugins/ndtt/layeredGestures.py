# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024-2025 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from functools import wraps

from scriptHandler import script
from tones import beep
from logHandler import log
from keyLabels import localizedKeyLabels
from baseObject import ScriptableObject
import addonHandler

from .securityUtils import secureBrowseableMessage

try:
	addonHandler.initTranslation()
except addonHandler.AddonError:
	pass


# Below toggle code came from Tyler Spivey's code, with enhancements by Joseph Lee.
def finally_(func, final):
	"""Calls final after func, even if it fails."""
	@wraps(func)
	def new(*args, **kwargs):
		try:
			func(*args, **kwargs)
		finally:
			final()
	return new


def ScriptableObjectWithLayeredGestures(scriptableObjectName, entryPointGestures):
	class MyScriptableObject(ScriptableObject):

		scriptCategory = scriptableObjectName

		def __init__(self, layerName, layeredCommandsList, *args, **kw):
			super(MyScriptableObject, self).__init__(*args, **kw)

			# #24 / NVDA 18890: if the scriptable objects is not statically created at module level, NVDA cannot
			# correctly remap its gestures.
			# So work it around by creating a variable holding the class at module level and renaming the class's
			# __name__ attribute accordingly as if the class were statically created at module level.
			moduleLevelClassName = "ScriptableObjectWithLayeredGestures_{}".format(layerName)
			if moduleLevelClassName in globals():
				log.error("Layer {} has already been used. Please use another name.".format(layerName))
			globals()[moduleLevelClassName] = MyScriptableObject
			# For Python 2: explicitely convert to str to avoid unicode instead; no effect in Python 3
			MyScriptableObject.__name__ = str(moduleLevelClassName)

			self.layerCommandsList = []
			for gesturesList, scriptName in layeredCommandsList:
				script = getattr(self, "script_{}".format(scriptName))
				self.layerCommandsList.append(
					(gesturesList, scriptName, script.__doc__),
				)

			self.toggling = False

		def getScript(self, gesture):
			if not self.toggling:
				return super(MyScriptableObject, self).getScript(gesture)
			script = super(MyScriptableObject, self).getScript(gesture)
			if not script:
				script = self.script_error
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
			description=_("Entry point for {name} layered commands").format(name=scriptableObjectName),
			gestures=entryPointGestures,
		)
		def script_layeredCommandsEntryPoint(self, gesture):
			# A run-time binding will occur from which we can perform various layered commands.
			# First, check if a second press of the script was done.
			if self.toggling:
				self.script_error(gesture)
				return
			layerGestures = {}
			for (gestures, command, desc) in self.layerCommandsList:
				for g in gestures:
					layerGestures["kb:" + g] = command
			self.bindGestures(layerGestures)
			self.toggling = True
			beep(100, 10)

		@script(
			# Translators: The description of a command of this add-on.
			description=_("Displays help on {name} layered commands").format(name=scriptableObjectName),
		)
		def script_displayHelp(self, gesture):
			# Translators: Title of the layered command help window.
			title = _("{name} layered commands").format(name=scriptableObjectName)
			cmdList = []
			for (gestures, command, desc) in self.layerCommandsList:
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
			secureBrowseableMessage(cmdList, title)

	return MyScriptableObject
