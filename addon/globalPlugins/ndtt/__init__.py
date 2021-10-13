# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler

from . import configNDTT

from .beepError import GlobalPlugin as BeepErrorGP
from .debugHelpMode import GlobalPlugin as DebugHelpModeGP
from .debugTool import GlobalPlugin as DebugToolGP
from .logReader import GlobalPlugin as LogReaderGP
from .pythonConsoleEx import GlobalPlugin as PythonConsoleExGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .windowutil import GlobalPlugin as WindowutilGP

class GlobalPlugin(
	BeepErrorGP,
	DebugHelpModeGP,
	DebugToolGP,
	LogReaderGP,
	PythonConsoleExGP,
	RestartWithOptionsGP,
	WindowutilGP,
):
	
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# We need to call explicitely chooseNVDAObjectOverlayClasses of the child class; else NVDA will skip them.
		LogReaderGP.chooseNVDAObjectOverlayClasses(self, obj, clsList)
		