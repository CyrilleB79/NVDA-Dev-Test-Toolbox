# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2026 Cyrille Bougot
# This file is covered by the GNU General Public License.

import config

try:
	# For NVDA 2021.1 and above
	from speech import speech
	speakFun = "speech.speech.speak"
except ImportError:
	# For NVDA 2020.4 and below
	speakFun = "speech.speak"

confspec = {
	"sourceFileOpener": 'string(default="")',
	"nvdaSourcePath": 'string(default="")',
	"logBackup": 'option("off", "maxNumber", default="off")',
	"logBackupMaxNumber": 'integer(min=1, max=100, default=3)',
	"copyRevTranslation": 'boolean(default=True)',
	"preserveConsoleInputHistory": "boolean(default=False)",
	"consoleInputHistorySize": "integer(min=1, max=10000, default=100)",
	"functionCallsLogTarget": "string(default={speakFun})".format(speakFun=speakFun),
	"functionCallsLogMethod": "string(default=settrace)",
}
config.conf.spec["ndtt"] = confspec

# Configuration initialization
# Perform a dummy change and restore the original value.
# This is needed to ensure that 'ndtt' key is present in config.conf.profiles[0] (default).
# Since we directly save in the default profile, we cannot take advantage of automatic section creation.
val = config.conf['ndtt']['logBackupMaxNumber']
if val == 1:
	config.conf['ndtt']['logBackupMaxNumber'] = 2
else:
	config.conf['ndtt']['logBackupMaxNumber'] = 1
config.conf['ndtt']['logBackupMaxNumber'] = val
