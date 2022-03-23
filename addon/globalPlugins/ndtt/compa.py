# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

import controlTypes


try:
# NVDA 2020.4+
	from globalVars import appDir
except ImportError:
# NVDA <= 2020.3
	import os
	appDir = os.path.abspath(os.curdir)


def convertControlTypes(ct):
	"""This functions takes controlTypes module as parameter.
	It recreates Role and State enumerations if they are missing for this module.
	"""
	try:
		ct.Role
	except AttributeError:
		ct.Role = recreateEnum(ct, 'Role', 'ROLE_')
	try:
		ct.State
	except AttributeError:
		# Re-create State enum
		ct.State = recreateEnum(ct, 'State', 'STATE_')
	try:
		ct.OutputReason
	except AttributeError:
		# Re-create Reason enum
		ct.OutputReason = recreateEnum(ct, 'OutputReason', 'REASON_')
	return ct

def recreateEnum(ct, name, prefix):
	try:
	# NVDA >= 2019.3 (Python 3)
		import enum
		if name == 'OutputReason':
			enumType=enum.Enum
		else: # Role, State
			enumType = enum.IntEnum
		# Re-create enum
		return enumType(name, {v[len(prefix):]: getattr(ct, v) for v in dir(ct) if v.startswith(prefix)})
	except ImportError:
		pass
	
	# NVDA 2019.2.1 (python 2)
	# Create a fake enum just as a class with fields.
	dct = {}
	for v in dir(ct):
		if v.startswith(prefix):
			dct[v[len(prefix):]] = getattr(ct, v)
	return type(name, (object,), dct)
		
controlTypes = convertControlTypes(controlTypes)
