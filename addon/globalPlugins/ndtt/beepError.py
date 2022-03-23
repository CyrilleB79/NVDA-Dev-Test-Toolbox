# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2019-2021 Cyrille Bougot

import globalPluginHandler
import addonHandler
from scriptHandler import script
import logHandler
import logging
import buildVersion
import ui
import config

ADDON_SUMMARY = addonHandler.getCodeAddon ().manifest["summary"]

# Check if NVDA has "Play error sound" feature.
try:
	config.conf.spec['featureFlag']
except KeyError:
	config.conf.spec['featureFlag'] = {}
try:
	config.conf.spec['featureFlag']['playErrorSound']
	hasPlayErrorSoundFeature = True
except KeyError:
	config.conf.spec['featureFlag']['playErrorSound'] = 'integer(0, 1, default=0)'
	hasPlayErrorSoundFeature = False

builtinHandle = logHandler.FileHandler.handle

def myHandle(fh,record, *args, **kwargs):
	# Only controls the play of the error sound if this is NOT a test version.
	#If test version, error sound will be played by built-in function
	shouldPlayErrorSound =  not buildVersion.isTestVersion and config.conf['featureFlag']['playErrorSound'] == 1
	import api
	if record.levelno>=logging.ERROR and shouldPlayErrorSound:
		import nvwave
		try:
			nvwave.playWaveFile("waves\\error.wav")
		except:
			pass
	return builtinHandle(fh, record, *args, **kwargs)
	
	
class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		if not hasPlayErrorSoundFeature:
			logHandler.FileHandler.handle = myHandle
		
	def terminate(self):
		if not hasPlayErrorSoundFeature:
			logHandler.FileHandler.handle = builtinHandle
		super(GlobalPlugin, self).terminate()
	
	@script(
# Translators: Input help mode message for a toggle command.
		description = _("Toggle play a sound for logged error."),
		gesture = "kb:nvda+control+alt+E",
		category = ADDON_SUMMARY,
	)
	def script_togglePlayErrorSound(self, gesture):
		if config.conf['featureFlag']['playErrorSound'] == 0:
			config.conf['featureFlag']['playErrorSound'] = 1
			msg = pgettext("advanced.playErrorSound", "Yes")
		else:
			config.conf['featureFlag']['playErrorSound'] = 0
			msg = pgettext("advanced.playErrorSound", "Only in NVDA test versions")
		ui.message(msg)		
