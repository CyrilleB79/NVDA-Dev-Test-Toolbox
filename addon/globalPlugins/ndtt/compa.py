# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Lukasz Golonka, Cyrille Bougot
# This file is covered by the GNU General Public License.

import operator
import os
import sys

import controlTypes
import globalVars


# Following code based on Lukasz Golonka's work.

class EnhancedGetter(object):

	def __init__(self, modWithAttrs, attrType, alternativeNameFactories):
		super(EnhancedGetter, self).__init__()
		self.mod = modWithAttrs
		self.attrType = attrType
		self.alternativeNameFactories = alternativeNameFactories

	def __getattr__(self, attrName):
		for aliasNameMaker in self.alternativeNameFactories:
			try:
				return operator.attrgetter(aliasNameMaker(self.attrType, attrName))(self.mod)
			except AttributeError:
				continue
		raise AttributeError("Attribute {} not found!".format(attrName))


class ControlTypesCompatWrapper(object):

	_ALIAS_FACTORIES = (
		lambda attrType, attrName: "_".join(({
			'OutputReason': 'REASON',
			'Role': 'ROLE',
			'State': 'STATE',
		}[attrType], attrName)),
		lambda attrType, attrName: ".".join((attrType, attrName)),
	)

	def __init__(self):
		super(ControlTypesCompatWrapper, self).__init__()
		self.OutputReason = EnhancedGetter(
			controlTypes,
			"OutputReason",
			self._ALIAS_FACTORIES
		)
		self.Role = EnhancedGetter(
			controlTypes,
			"Role",
			self._ALIAS_FACTORIES
		)
		self.State = EnhancedGetter(
			controlTypes,
			"State",
			self._ALIAS_FACTORIES
		)
	
	def __getattr__(self, attr):
		return getattr(controlTypes, attr)


def getApDir():
	try:
		# NVDA 2020.4+
		return globalVars.appDir
	except AttributeError:
		# NVDA <= 2020.3
		if getattr(sys, "frozen", None):
			# We are running as an executable.
			return sys.prefix  # No normalization necessary
		# we are running from source
		# Since we cannot rely on CWD being correct create a path from one of NVDA's core modules.
		return os.path.abspath(os.path.normpath(os.path.dirname(globalVars.__file__)))


appDir = getApDir()
controlTypesCompatWrapper = ControlTypesCompatWrapper()
