# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

from functools import wraps

from scriptHandler import script
from tones import beep
from keyLabels import localizedKeyLabels
from baseObject import ScriptableObject

from .securityUtils import secureBrowseableMessage


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


NDTT_LAYERED_COMMANDS_LIST = [
	# A list of 3-tuples. Each 3-tuple contains:
	# - a gesture list
	# - the associated script name
	# - if the command is available in secure mode.
	(["d"], "toggleESDMode", True),
	(["e"], "reportLastError", False),
	(["shift+e"], "togglePlayErrorSound", False),
	(["k"], "addMarkerInLog", False),
	(["o"], "announceObjectInfo", True),
	(["upArrow"], "nextObjectInfo", True),
	(["downArrow"], "priorObjectInfo", True),
	(["shift+o"], "toggleCustomObjectReporting", True),
	(["q"], "restartWithOptions", True),
	(["r"], "reverseUITranslation", True),
	(["s"], "toggleStackTraceLog", False),
	(["p"], "openSettings", False),
	(["h"], "displayHelp", True),
]


def ScriptableObjectWithLayeredGestures(scriptableObjectName, entryPointGestures):
	class MyScriptableObject(ScriptableObject):

		scriptCategory = scriptableObjectName

		def __init__(self, layeredCommandsList, *args, **kw):
			super(MyScriptableObject, self).__init__(*args, **kw)
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
