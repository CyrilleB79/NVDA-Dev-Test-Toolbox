# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler
from .beepError import GlobalPlugin as BeepErrorGP
from .debugHelpMode import GlobalPlugin as DebugHelpModeGP
from .debugTool import GlobalPlugin as DebugToolGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .windowutil import GlobalPlugin as WindowutilGP

class GlobalPlugin(
	BeepErrorGP,
	DebugHelpModeGP,
	DebugToolGP,
	RestartWithOptionsGP,
	WindowutilGP,
):
	pass
	