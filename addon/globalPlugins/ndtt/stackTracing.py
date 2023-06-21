# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019 Cyrille Bougot
# This file is covered by the GNU General Public License.

# INSTRUCTIONS to modify the function whose stack trrace is logged:
# To change the trigger function search this file for "ToBeCustomized" strings.
# E.g. to trigger stack trace log on braille.BrailleHandler.update
# - import braille instead of speech
# - replace speech.speak function by braille.BrailleHandler.update function
# Good candidate functions may be the ones found in NVDA's journal on lines beginning with 'IO - ',
# e.g. braille.update, braille.BrailleBuffer.update, tones.beep, etc.


import globalPluginHandler
import addonHandler
import ui
import traceback
from logHandler import log
from scriptHandler import script

# ToBeCustomized: import here the module containing the function you want the stacktrace to be logged
try:
	# For NVDA 2021.1 and above
	from speech import speech
except ImportError:
	# For NVDA 2020.4 and below
	import speech
_originalFunction = speech.speak
# import braille
# _originalFunction = braille.BrailleHandler.update

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


def functionWithStackTraceLog(*args, **kwargs):
	res = _originalFunction(*args, **kwargs)
	GlobalPlugin.logStackTrace()
	return res


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.logEnabled = False

	@script(
		# Translators: Input help mode message for a toggle command.
		description=_("Toggles the stack trace log when the speech function is called."),
		gesture="kb:nvda+control+alt+S",
		category=ADDON_SUMMARY,
	)
	def script_toggleStackTraceLog(self, gesture):
		self.logEnabled = not self.logEnabled
		self.enableStackTraceLog(self.logEnabled)
		if self.logEnabled:
			# Translators: Reported when toggling the stack trace log feature.
			msg = _('Stacktrace log enabled')
		else:
			# Translators: Reported when toggling the stack trace log feature.
			msg = _('Stacktrace log disabled')
		ui.message(msg)

	def enableStackTraceLog(self, enable=True):
		if enable:
			newFun = functionWithStackTraceLog
		else:
			newFun = _originalFunction
		# ToBeCustomized: the function from which you want the stack trace
		speech.speak = newFun
		# or: braille.BrailleHandler.update = newFun

	@staticmethod
	def logStackTrace():
		stack = [line.strip() for line in traceback.format_stack()]
		msgStackTrace = (
			'=== Stack trace log ===\n'
			+ '\n'.join(stack[:-1]) + '\n'
			+ '=== End stack trace log ==='
		)
		log.debug(msgStackTrace)

	def terminate(self):
		self.enableStackTraceLog(False)
		super(GlobalPlugin, self).terminate()
