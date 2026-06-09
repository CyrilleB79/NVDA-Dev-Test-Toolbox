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
except KeyError:
	# For NVDA < 2021.3
	hasPlayErrorSoundFeature = False
else:
	playErrorSoundFeatureOptionsNumber = int(config.conf.getConfigValidation(("featureFlag", "playErrorSound")).args[1]) + 1
	if not playErrorSoundFeatureOptionsNumber in [2, 3]:
		raise ValueError('Unexpected number of options for "Play error sound feature": {}'.format(playErrorSoundFeatureOptionsNumber))
if not hasPlayErrorSoundFeature:
	# Add (NVDA < 2021.3) config spec value with only 2 values (as before NVDA 2026.2)
	# 0: Only in test versions, 1: yes
	config.conf.spec["featureFlag"]["playErrorSound"] = "integer(0, 1, default=0)"
if playErrorSoundFeatureOptionsNumber < 3
	# Add (NVDA < 2026.2) config spec value to track disable all error sounds
	config.conf.spec["ndtt"]["disableErrorSound"] = "boolean(default=False)"
else:
	try:
		config.conf["ndtt"]["disableErrorSound"]
	except KeyError:
		pass
	else:
		log.debug('NVDA version >= 2026.2 - Ignoring config.conf["ndtt"]["disableErrorSound"]')

builtinHandle = logHandler.FileHandler.handle
builtinShouldPlayErrorSound = logHandler.shouldPlayErrorSound


def myShouldPlayErrorSound():
	if not hasPlayErrorSoundFeature:
		raise RuntimeError("This function should not be called in this version of NVDA.")
	if (
		playErrorSoundFeatureOptionsNumber == 3  # NVDA >= 2026.2
		or config.conf["featureFlag"]["playErrorSound"] < 2  # Supported values for NVDA < 2026.2
	):
		# We let the native shouldPlayErrorSound function return the value.
		return builtinShouldPlayErrorSound()
	# If we get here, we have necessarily config.conf["featureFlag"]["playErrorSound"] == 2
	return False

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
		if (
			playErrorSoundFeatureOptionsNumber < 3  # NVDA < 2026.2
			and config.conf["ndtt"]["disableErrorSound"]
		):
			playErrorSound = 3
		else:
			playErrorSound = config.conf["featureFlag"]["playErrorSound"]
		playErrorSound  = (playErrorSound + 1) % 3
		try:
			config.conf["featureFlag"]["playErrorSound"] = playErrorSound
			config.conf["ndtt"]["disableErrorSound"] = False
		except configobj.validate.VdtValueTooBigError:  # NVDA < 2026.2
			config.conf["ndtt"]["disableErrorSound"] = True
		if playErrorSound == 0:
			# Translators: Message reported when calling the command to toggle play a sound for logged errors
			msg = _("Only in NVDA test versions")
		elif playErrorSound == 1:
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
