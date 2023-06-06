# -*- coding: UTF-8 -*-
# NVDA add-on: NVDA Dev & Test Toolbox
# Copyright (C) 2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import config


def getBaseProfileConfigValue(*args):
	cfg = config.conf.profiles[0]
	for key in args:
		try:
			cfg = cfg[key]
		except KeyError:
			break
	else:
		validationFuncName = config.conf.getConfigValidation(tuple(args)).validationFuncName
		typeMaker = {
			'integer': int,
			'string': str,
			'option': str,
			'float': float,
		}.get(validationFuncName)
		if not typeMaker:
			raise NotImplementedError(validationFuncName)
		return typeMaker(cfg)
	return config.conf.getConfigValidation(tuple(args)).default
