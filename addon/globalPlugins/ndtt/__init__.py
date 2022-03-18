# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler

from . import configNDTT

from .beepError import GlobalPlugin as BeepErrorGP
from .extScriptDesc import GlobalPlugin as ExtScriptDescGP
from .stackTracing import GlobalPlugin as StackTracingGP
from .logReader import GlobalPlugin as LogReaderGP
from .pythonConsoleEx import GlobalPlugin as PythonConsoleExGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .objPropExplorer import GlobalPlugin as ObjPropExplorerGP

class GlobalPlugin(
	BeepErrorGP,
	ExtScriptDescGP,
	StackTracingGP,
	LogReaderGP,
	PythonConsoleExGP,
	RestartWithOptionsGP,
	ObjPropExplorerGP,
):
	
	def chooseNVDAObjectOverlayClasses(self, obj, clsList):
		# We need to call explicitely chooseNVDAObjectOverlayClasses of the child class; else NVDA will skip them.
		LogReaderGP.chooseNVDAObjectOverlayClasses(self, obj, clsList)
		