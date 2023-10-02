# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019-2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import inspect
import os

import globalPluginHandler
import ui
import api
from .compa import controlTypesCompatWrapper as controlTypes
# Import normal controlTypes and not the wrapper only to be used for older versions of NVDA.
import controlTypes as oldControlTypes
from logHandler import log
import addonHandler
import scriptHandler
from scriptHandler import script
import speech

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


def _createDicControlTypesConstantes(prefix):
	dic = {}
	attributes = dir(oldControlTypes)
	for name in attributes:
		if name.startswith(prefix):
			dic[getattr(oldControlTypes, name)] = name[len(prefix):]
	return dic


_DIC_ROLES = _createDicControlTypesConstantes('ROLE_')
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


def makeGetInfo(infoType):
	def getInfo(o):
		return getattr(o, infoType)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	_INFO_TYPES = [
		('name', lambda o: o.name),
		('role', getRoleInfo),
		('states', getStateInfo),
		('value', lambda o: o.value),
		('windowClassName', lambda o: o.windowClassName),
		('windowControlID', lambda o: o.windowControlID),
		('windowHandle', lambda o: o.windowHandle),
		('location', getLocationInfo),
		('pythonClass', lambda o: str(type(o))),
		(
			'pythonClassMRO',
			lambda o: str(type(o).mro()).replace('>, <', ',\r\n').replace('[<', '', 1).replace('>]', '')
		)
	]

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.index = 0
		self.customObjectReporting = False
		self.orig_speakObject = speech.speakObject
		speech.speakObject = self.customSpeakObjectFactory()

	def terminate(self, *args, **kwargs):
		speech.speakObject = self.orig_speakObject
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Reports the currently selected property of the object property explorer for the navigator object; "
			"two presses displays this information in a browseable message."
		),
		category=ADDON_SUMMARY,
	)
	def script_announceObjectInfo(self, gesture):
		self.announceCurrentInfo(scriptHandler.getLastScriptRepeatCount())

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Selects the next property of the object property explorer and reports it for the navigator object."
		),
		category=ADDON_SUMMARY,
	)
	def script_nextObjectInfo(self, gesture):
		self.index = (self.index + 1) % len(self._INFO_TYPES)
		self.announceCurrentInfo()

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Selects the previous property of the object property explorer and reports it for the navigator object."
		),
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
		infoType, fun = self._INFO_TYPES[self.index]
		nav = api.getNavigatorObject()
		try:
			info = fun(nav)
		except Exception:
			info = 'Unavailable information.'
			log.debugWarning('An exception occurred while retrieving the requested information.', exc_info=True)
		self.lastInfo = '{}:\r\n{}'.format(infoType, info)
		ui.message(self.lastInfo)

	@script(
		description=_(
			# Translators: Input help mode message for a command of the object property explorer.
			"Toggle custom reporting of objects using the Object explorer's selected property when you use object"
			" navigation commands."
		),
		category=ADDON_SUMMARY,
	)
	def script_toggleCustomObjectReporting(self, gesture):
		if not self.customObjectReporting:
			self.customObjectReporting = True
			# Translators: Message reported by a command of the object property explorer.
			ui.message(_('Custom object reporting enabled'))
		else:
			self.customObjectReporting = False
			# Translators: Message reported by a command of the object property explorer.
			ui.message(_('Custom object reporting disabled'))

	def customSpeakObjectFactory(self):

		def new_speakObject(
			obj,
			reason=controlTypes.OutputReason.QUERY,
			_prefixSpeechCommand=None,
			**kwargs
		):
			if not self.customObjectReporting:
				return self.orig_speakObject(obj, reason, _prefixSpeechCommand, **kwargs)
			s1 = inspect.stack()[1]
			try:
				# Python 3
				filename = s1.filename
				function = s1.function
			except AttributeError:
				# Python 2
				filename = s1[1]
				function = s1[3]
			if os.path.splitext(filename)[0] != 'globalCommands' or function not in [
				'script_navigatorObject_current',
				'script_navigatorObject_next',
				'script_navigatorObject_previous',
				'script_navigatorObject_firstChild',
				'script_navigatorObject_parent',
				'script_navigatorObject_nextInFlow',
				'script_navigatorObject_previousInFlow',
			]:
				return self.orig_speakObject(obj, reason, _prefixSpeechCommand, **kwargs)
			infoType, fun = self._INFO_TYPES[self.index]
			try:
				info = fun(obj)
			except Exception:
				info = 'Unavailable information.'
				log.debugWarning('An exception occurred while retrieving the requested information.', exc_info=True)
			sequence = [str(info)]
			kwargs2 = {}
			try:
				# Parameter supported by NVDA 2019.3 onwards
				kwargs2['priority'] = kwargs['priority']
			except KeyError:
				pass
			speech.speak(sequence, **kwargs2)

		return new_speakObject
