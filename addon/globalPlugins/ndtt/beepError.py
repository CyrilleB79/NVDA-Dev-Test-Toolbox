# -*- coding: UTF-8 -*-
#Beep error scripts for NVDA
#Copyright (C) 2019 Cyrille Bougot
#This file is covered by the GNU General Public License.

#This script allows NVDA to beep on error even in NVDA non-test versions.
#To use it, put it in the globalPlugins folder.

#To activate or de-activate beep error feature, press NVDA+control+alt+B

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
	config.conf['featureFlag']['playErrorSound']
	hasPlayErrorSoundFeature = True
except KeyError:
	hasPlayErrorSoundFeature = False

builtinHandle = logHandler.FileHandler.handle

def myHandle(fh,record, *args, **kwargs):
	# Only play the error sound if this is NOT a test version.
	#If test version, error sound will be played by built-in function
	shouldPlayErrorSound =  not buildVersion.isTestVersion
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
		self.beepOnErrorConfigure(True, silent=True)
		
	@script(
		description = "Toggle beep on error feature; this does not impact beep on NVDA test versions.",
		gesture = "kb:nvda+control+alt+B",
		category = ADDON_SUMMARY,
	)
	def script_toggleBeepOnError(self, gesture):
		self.beepOnErrorConfigure(not self.beepOnErrorEnabled)
		
	def beepOnErrorConfigure(self, bEnable, silent=False):
		self.beepOnErrorEnabled = bEnable
		if bEnable:
			logHandler.FileHandler.handle = myHandle
			msg = 'Beep on error enabled'
		else:
			logHandler.FileHandler.handle = builtinHandle
			msg = 'Beep on error disabled'
		if not silent:
			ui.message(msg)
			
	def terminate(self):
		self.beepOnErrorConfigure(False, silent=True)
		super(GlobalPlugin, self).terminate()


if hasPlayErrorSoundFeature:
	# NVDA 2021.3: remove beep on error feature since play error sound is present
	class GlobalPlugin(globalPluginHandler.GlobalPlugin):
		pass