# -*- coding: UTF-8 -*-
# NVDA add-on: NVDA Dev & Test Toolbox
# Copyright (C) 2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals
import inspect
from logHandler import log


def logLocals():
	"""A function to logs the local variables where this function is called.
	Calling it at the beginning of a function allows to log its parameters; which are the only locals that are
	already defined.
	
	Example:
	def foo(a, b):
		logLocals()  # a and b will be logged, not c.
		c = a + b
		logLocals()  # a, b and c will be logged here
		return c
	"""

	info = []
	frame = inspect.currentframe().f_back
	try:
		file = frame.f_code.co_filename
		lineNo = frame.f_lineno
		name = frame.f_code.co_name
		info.append(
			'Location:\n'
			'  File "{file}", line {lineNo}, in {name}'.format(file=file, lineNo=lineNo, name=name)
		)
		localsInfo = []
		for name, value in frame.f_locals.items():
			localsInfo.append('  {name}: {value}'.format(name=name, value=value))
		if localsInfo:
			info.append('Locals:')
			info.extend(localsInfo)
		else:
			info.append('No locals')
		log.info('\n'.join(info))
	except Exception:
		log.error('Unable to log locals', exc_info=True)
	finally:
		del frame

