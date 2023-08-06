# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2023 Cyrille Bougot

import globalPluginHandler
import addonHandler
from scriptHandler import script
import scriptHandler
import logHandler
import logging
import buildVersion
import ui
import config
import os

from .compa import appDir

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Check if NVDA has "Play error sound" feature.
try:
	# Present in NVDA 2020.2+
	config.conf.spec['featureFlag']
except KeyError:
	# For NVDA < 2020.2
	config.conf.spec['featureFlag'] = {}
try:
	# OK for NVDA 2021.3+
	config.conf.spec['featureFlag']['playErrorSound']
	hasPlayErrorSoundFeature = True
except KeyError:
	# For NVDA < 2021.3
	# 0:Only in test versions, 1:yes
	config.conf.spec['featureFlag']['playErrorSound'] = 'integer(0, 1, default=0)'
	hasPlayErrorSoundFeature = False

builtinHandle = logHandler.FileHandler.handle


def myHandle(fh, record, *args, **kwargs):
	# Save the last error
	if record.levelno >= logging.ERROR:
		errorInfo = []
		errorInfo.append(record.levelname)
		if record.msg is not None:
			errorInfo.append(str(record.msg))
		if record.exc_info:
			excType = record.exc_info[1]
			if excType is not None:
				errorInfo.append(repr(excType))
			# else it is probably not worth reporting that no exception is available but has been requested.
		logHandler.ndttLastErrorInfo = ' - '.join(errorInfo)
		logHandler.ndttLastRecord = record
	# The add-on only controls error sound playing when all of the following conditions are met:
	if (
		# 1. NVDA has not play error sound feature built in (else it is played directly by NVDA if needed).
		(not hasPlayErrorSoundFeature)
		# 2. It is not a test version of NVDA (else it is played directly by NVDA if needed).
		and (not buildVersion.isTestVersion)
		# 3. Play error sound is enabled in config (else, no need to care of playing sound).
		and (config.conf['featureFlag']['playErrorSound'] == 1)
		# 4. Log level is ERROR or higher
		and record.levelno >= logging.ERROR
	):
		import nvwave
		try:
			nvwave.playWaveFile(os.path.join(appDir, "waves", "error.wav"))
		except Exception:
			pass
	return builtinHandle(fh, record, *args, **kwargs)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		logHandler.FileHandler.handle = myHandle

	def terminate(self):
		logHandler.FileHandler.handle = builtinHandle
		self.clearLastError()
		super(GlobalPlugin, self).terminate()

	def clearLastError(self):
		try:
			del logHandler.ndttLastErrorInfo
		except AttributeError:
			pass

	@script(
		# Translators: Input help mode message for a toggle command.
		description=_("Toggles play a sound for logged error."),
		gesture="kb:nvda+control+alt+E",
		category=ADDON_SUMMARY,
	)
	def script_togglePlayErrorSound(self, gesture):
		if config.conf['featureFlag']['playErrorSound'] == 0:
			config.conf['featureFlag']['playErrorSound'] = 1
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("Yes")
		else:
			config.conf['featureFlag']['playErrorSound'] = 0
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("Only in NVDA test versions")
		ui.message(msg)

	@script(
		# Translators: Input help mode message for a command.
		description=_("Report the last error logged. A second press clears the memorized last error."),
		gesture="kb:nvda+shift+alt+E",
		category=ADDON_SUMMARY,
	)
	def script_reportLastError(self, gesture):
		nRepeat = scriptHandler.getLastScriptRepeatCount()
		if nRepeat == 0:
			try:
				ui.message(logHandler.ndttLastErrorInfo)
			except AttributeError:
				# Translators: Message reported when calling the "report last error" command
				ui.message(_('No error'))
		elif nRepeat == 1:
			self.clearLastError()
			# Translators: Message reported when calling the "report last error" command
			ui.message(_('Last error cleared'))
		else:
			pass
