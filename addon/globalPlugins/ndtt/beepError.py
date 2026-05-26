# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2026 Cyrille Bougot

import globalPluginHandler
import addonHandler
import scriptHandler
import logHandler
import logging
import buildVersion
import ui
import config
import os

from .compa import appDir
from .speechOnDemand import script

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

# Check if NVDA has "Play error sound" feature and which one
try:
	# Present in NVDA 2020.2+
	config.conf.spec["featureFlag"]
except KeyError:
	# For NVDA < 2020.2
	config.conf.spec["featureFlag"] = {}
try:
	# OK for NVDA 2021.3+
	config.conf.spec["featureFlag"]["playErrorSound"]
	hasPlayErrorSoundFeature = True
	hasThreeValuePlayErrorSoundFeature = zzz check config int max value (cf settings dialog)
except KeyError:
	# For NVDA < 2021.3
	hasPlayErrorSoundFeature = False
	hasThreeValuePlayErrorSoundFeature = False
if not hasThreeValuePlayErrorSoundFeature:
	# Add (NVDA < 2021.3) or modify (NVDA < 2026.2) config spec value
	# 0: Only in test versions, 1: yes, 2: No
	config.conf.spec["featureFlag"]["playErrorSound"] = "integer(0, 2, default=0)"

builtinHandle = logHandler.FileHandler.handle
builtinShouldPlayErrorSound = logHandler.shouldPlayErrorSound


def myHandle(fh, record, *args, **kwargs):
	# Save the last error
	if record.levelno >= logging.ERROR:
		errorInfo = []
		errorInfo.append(record.levelname)
		errorInfo.append(record.getMessage())
		if record.exc_info:
			excType = record.exc_info[1]
			if excType is not None:
				errorInfo.append(repr(excType))
			# else it is probably not worth reporting that no exception is available but has been requested.
		logHandler.ndttLastErrorInfo = " - ".join(errorInfo)
		logHandler.ndttLastRecord = record
	
	if hasPlayErrorSoundFeature:
		# We can use NVDA's built-in handle method since it calls shouldPlayErrorSound, that we have patched for
		# our needs
		return builtinHandle(fh, record, *args, **kwargs)
	
	# If NVDA has not the play error sound feature we copy its handle method (below), replacing
	# shouldPlayErrorSound internal variable computation by a call to shouldPlayErrorSound() function.
	if record.levelno>=logging.CRITICAL:
		try:
			winsound.PlaySound("SystemHand",winsound.SND_ALIAS)
		except Exception:
			pass
	elif record.levelno>=logging.ERROR and shouldPlayErrorSound():
		import nvwave
		try:
			nvwave.playWaveFile(os.path.join(globalVars.appDir, "waves", "error.wav"))
		except Exception:
			pass
	return logging.FileHandler.handle(record)
	
	# zzz To be removed
	# The add-on only controls error sound playing when all of the following conditions are met:
	if (
		# 1. NVDA has not play error sound feature built in (else it is played directly by NVDA if needed).
		(not hasPlayErrorSoundFeature)
		# 2. It is not a test version of NVDA (else it is played directly by NVDA if needed).
		and (not buildVersion.isTestVersion)
		# 3. Play error sound is enabled in config (else, no need to care of playing sound).
		and (config.conf["featureFlag"]["playErrorSound"] == 1)
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
		# Patch 
		if hasPlayErrorSoundFeature:
			logHandler.shouldPlayErrorSound = myShouldPlayErrorSound

	def terminate(self):
		if hasPlayErrorSoundFeature:
			logHandler.shouldPlayErrorSound =  builtinShouldPlayErrorSound
		logHandler.FileHandler.handle = builtinHandle
		self.clearLastError()
		super(GlobalPlugin, self).terminate()

	def clearLastError(self):
		try:
			del logHandler.ndttLastErrorInfo
		except AttributeError:
			pass

	@script(
		# Translators: Input help mode message for a cycle command.
		description=_("Cycles play a sound for logged error."),
		category=ADDON_SUMMARY,
	)
	def script_togglePlayErrorSound(self, gesture):
		config.conf["featureFlag"]["playErrorSound"] = (config.conf["featureFlag"]["playErrorSound"] + 1) % 3
		if config.conf["featureFlag"]["playErrorSound"] == 0:
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("Only in NVDA test versions")
		elif config.conf["featureFlag"]["playErrorSound"] == 1:
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("Yes")
		else:
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("No")
		ui.message(msg)

	@script(
		# Translators: Input help mode message for a command.
		description=_("Report the last error logged. A second press clears the memorized last error."),
		category=ADDON_SUMMARY,
		speakOnDemand=True,
	)
	def script_reportLastError(self, gesture):
		nRepeat = scriptHandler.getLastScriptRepeatCount()
		if nRepeat == 0:
			try:
				ui.message(logHandler.ndttLastErrorInfo)
			except AttributeError:
				# Translators: Message reported when calling the "report last error" command
				ui.message(_("No error"))
		elif nRepeat == 1:
			self.clearLastError()
			# Translators: Message reported when calling the "report last error" command
			ui.message(_("Last error cleared"))
		else:
			pass
