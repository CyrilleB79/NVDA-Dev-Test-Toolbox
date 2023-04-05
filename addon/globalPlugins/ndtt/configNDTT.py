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

