# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2021-2022 Cyrille Bougot
# This file is covered by the GNU General Public License.

import controlTypes

try:
	from globalVars import appDir
except ImportError:
	import os
	appDir = os.path.abspath(os.curdir)


def convertControlTypes(ct):
	"""This functions takes controlTypes module as parameter.
	It recreates Role and State enumerations if they are missing for this module.
	"""
	import enum
	try:
		ct.Role
	except AttributeError:
		# Re-create Role enum
		Role = enum.IntEnum('Role', {v[len('ROLE_'):]: getattr(ct, v) for v in dir(ct) if v.startswith('ROLE_')})
		ct.Role = Role
	try:
		ct.State
	except AttributeError:
		# Re-create State enum
		State = enum.IntEnum('State', {v[len('STATE_'):]: getattr(ct, v) for v in dir(ct) if v.startswith('STATE_')})
		ct.State = State
	try:
		ct.OutputReason
	except AttributeError:
		# Re-create Reason enum
		OutputReason = enum.Enum('OutputReason', {v[len('REASON_'):]: getattr(ct, v) for v in dir(ct) if v.startswith('REASON_')})
		ct.OutputReason = OutputReason
	return ct
controlTypes = convertControlTypes(controlTypes)
