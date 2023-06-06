# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020-2021 Cyrille Bougot
# This file is covered by the GNU General Public License.

from types import MethodType

import globalPluginHandler
import addonHandler
import scriptHandler
import inputCore
import ui

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Translators: The name of a category in the Input gesture dialog
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
		scriptLocation = scriptHandler.getScriptLocation(script)
		if scriptLocation:
			# Translators: A message reported in input help mode when extended script description is enabled.
			desc = "{scriptName} on {scriptLocation}".format(
				scriptName=scriptName,
				scriptLocation=scriptLocation,
			)
		else:
			desc = scriptName
		script.__func__.__doc__ = desc
		script.__func__.category = SCRIPT_WITHOUT_DESC_CATEGORY
		GlobalPlugin.scriptsWithAddedDoc.add(script)
	res = _originalMethod(gesture, onlyLog)
	return res


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	scriptsWithAddedDoc = set()

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.configureESDMode(False, silent=True)

	def terminate(self):
		self.configureESDMode(False, silent=True)
		super(GlobalPlugin, self).terminate()

	@scriptHandler.script(
		# Translators: Input help mode message for a toggle command.
		description=_("Toggles the extended script description mode."),
		gesture="kb:nvda+control+alt+D",
		category=ADDON_SUMMARY,
	)
	def script_tobbleESDMode(self, gesture):
		self.configureESDMode(not self.esdMode)

	def configureESDMode(self, enable, silent=False):
		self.esdMode = enable
		if enable:
			inputCore.manager._handleInputHelp = MethodType(newHandleInputHelp, _originalMethod.__self__)
			# Translators: A message reported when toggling Extended script description mode.
			msg = _('Extended script description mode enabled')
		else:
			inputCore.manager._handleInputHelp = _originalMethod
			# Translators: A message reported when toggling Extended script description mode.
			msg = _('Extended script description mode disabled')
			for script in self.__class__.scriptsWithAddedDoc:
				del script.__func__.__doc__
				del script.__func__.category
			self.__class__.scriptsWithAddedDoc.clear()
		if not silent:
			ui.message(msg)
