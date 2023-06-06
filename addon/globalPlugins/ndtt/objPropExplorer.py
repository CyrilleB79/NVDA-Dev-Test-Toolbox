# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import globalPluginHandler
import ui
import api
import controlTypes  # Import normal controlTypes and not the wrapper since it is only used for older versions of NVDA.
from logHandler import log
import addonHandler
import scriptHandler
from scriptHandler import script

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon ().manifest["summary"]

def _createDicControlTypesConstantes(prefix):
	dic = {}
	attributes = dir(controlTypes)
	for name in attributes:
		if name.startswith(prefix):
			dic[getattr(controlTypes, name)] = name[len(prefix):]
	return dic
_DIC_ROLES	 = _createDicControlTypesConstantes('ROLE_')
_DIC_STATES = _createDicControlTypesConstantes('STATE_')

def getRoleInfo(o):
	try:
		# NVDA 2021.2+ where controlTypes.Role and controlTypes.State are enums.
		return '{} ({})'.format(o.role.name, o.role.value)
	except AttributeError:
		# Pre-NVDA 2021.2 where controlTypes.ROLE_ and controlTypes.STATE_ are constants
		return '{} ({})'.format(_DIC_ROLES[o.role], o.role)

def getStateInfo(o):
	info = sorted(o.states)
	try:
		# NVDA 2021.2+ where controlTypes.Role and controlTypes.State are enums.
		names = ', '.join(str(i.name) for i in info)
		values = ', '.join(str(i.value) for i in info)
	except AttributeError:
		# Pre-NVDA 2021.2 where controlTypes.ROLE_ and controlTypes.STATE_ are constants
		names = ', '.join([_DIC_STATES[i] for i in info])
		values = info
	return '{} ({})'.format(names, values)
	
def getLocationInfo(o):
	info = ',\r\n'.join('{}: {}'.format(i, getattr(o.location, i)) for i in ['left', 'top', 'width', 'height'])
	return info
			
	

	
class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	_INFO_TYPES = ['name',
		('role', getRoleInfo),
		('states', getStateInfo),
		'value',
		'windowClassName',
		'windowControlID',
		'windowHandle',
		('location', getLocationInfo),
		('pythonClass', lambda o: str(type(o))),
		('pythonClassMRO', lambda o: str(type(o).mro()).replace('>, <', ',\r\n').replace('[<', '', 1).replace('>]',''))]

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.index = 0

	@script(
		# Translators: Input help mode message for a command of the object property explorer.
		description=_("Reports the currently selected property of the object property explorer for the navigator object; two presses displays this information in a browseable message."),
		category=ADDON_SUMMARY,
	)
	def script_announceObjectInfo(self, gesture):
		self.announceCurrentInfo(scriptHandler.getLastScriptRepeatCount())

	@script(
		# Translators: Input help mode message for a command of the object property explorer.
		description=_("Selects the next property of the object property explorer and reports it for the navigator object."),
		category=ADDON_SUMMARY,
	)
	def script_nextObjectInfo(self, gesture):
		self.index = (self.index + 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()

	@script(
		# Translators: Input help mode message for a command of the object property explorer.
		description=_("Selects the previous property of the object property explorer and reports it for the navigator object."),
		category=ADDON_SUMMARY,
	)
	def script_priorObjectInfo(self, gesture):
		self.index = (self.index - 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()
	
	def announceCurrentInfo(self, nPress=0):
		if nPress > 1:
			return
		elif nPress == 1:
			ui.browseableMessage(self.lastInfo)
			return
		infoType = self._INFO_TYPES[self.index]
		nav = api.getNavigatorObject()
		if isinstance(infoType, tuple):
			infoType, fun = infoType
		else:
			fun = lambda o: getattr(o, infoType)
		try:
			info = fun(nav)
		except Exception as e:
			info = 'Unavailable information.'
			log.debugWarning('An exception occurred while retrieving the requested information.', exc_info=True)
		self.lastInfo = '{}:\r\n{}'.format(infoType, info)
		ui.message(self.lastInfo)
