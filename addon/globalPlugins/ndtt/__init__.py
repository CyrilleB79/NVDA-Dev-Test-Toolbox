# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2020 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler
import globalVars

from . import configNDTT


from .extScriptDesc import GlobalPlugin as ExtScriptDescGP
from .restartWithOptions import GlobalPlugin as RestartWithOptionsGP
from .objPropExplorer import GlobalPlugin as ObjPropExplorerGP

# Plugins that may be also used in secure context
allContextGPList = [ExtScriptDescGP, RestartWithOptionsGP, ObjPropExplorerGP]

if not globalVars.appArgs.secure:
	from .beepError import GlobalPlugin as BeepErrorGP  # No error tone in secure mode
	from .stackTracing import GlobalPlugin as StackTracingGP  # No log nor log viewer in secure mode
	from .logReader import GlobalPlugin as LogReaderGP  # No log nor log viewer in secure mode.
	from .pythonConsoleEx import GlobalPlugin as PythonConsoleExGP  # No Python console in secure mode
	
	# Plugins that may be used only in normal context, not in secure context.
	normalContextGPList = [BeepErrorGP, StackTracingGP, LogReaderGP, PythonConsoleExGP]


class GlobalPlugin(*allContextGPList):
	pass


if not globalVars.appArgs.secure:
	class GlobalPlugin(*(allContextGPList + normalContextGPList)):
		
		def chooseNVDAObjectOverlayClasses(self, obj, clsList):
			# We need to call explicitely chooseNVDAObjectOverlayClasses of the child class; else NVDA will skip them.
			LogReaderGP.chooseNVDAObjectOverlayClasses(self, obj, clsList)
		