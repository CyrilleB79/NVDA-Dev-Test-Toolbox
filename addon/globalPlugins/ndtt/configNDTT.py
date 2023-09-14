# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

import config

confspec = {
	"sourceFileOpener": 'string(default="")',
	"nvdaSourcePath": 'string(default="")',
	"logBackup": 'option("off", "maxNumber", default="off")',
	"logBackupMaxNumber": 'integer(min=1, max=100, default=3)',
}
config.conf.spec["ndtt"] = confspec

# Configuration initialization
# Perform a dummy change and restore the original value.
# This is needed to ensure that 'ndtt' key is present in config.conf.profiles[0] (default).
# Since we directly save in the default profile, we cannot take advantage of automatic secion creation.
val = config.conf['ndtt']['logBackupMaxNumber']
if val == 1:
	config.conf['ndtt']['logBackupMaxNumber'] = 2
else:
	config.conf['ndtt']['logBackupMaxNumber'] = 1
config.conf['ndtt']['logBackupMaxNumber'] = val
