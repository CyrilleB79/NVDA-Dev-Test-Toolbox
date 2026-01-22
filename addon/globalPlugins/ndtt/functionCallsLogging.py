# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2019-2026 Cyrille Bougot
# This file is covered by the GNU General Public License.


import sys
import traceback
import inspect
import threading

import globalPluginHandler
import addonHandler
import ui
import config
from logHandler import log
from scriptHandler import script


addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


LOG_METHOD_MONKEY_PATCHING = "monkeyPatching"
LOG_METHOD_SETTRACE = "settrace"

logMethodDisplayStrings = [
	# Translators: A possible choice for function calls log method setting
	(LOG_METHOD_MONKEY_PATCHING, _("Monkey patching")),
	# Translators: A possible choice for function calls log method setting
	(LOG_METHOD_SETTRACE, _("settrace")),
]

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self):
		super(GlobalPlugin, self).__init__()
		self.logEnabled = False
		self.threadState = threading.local()
		self.logMethod = None

	@script(
		# Translators: Input help mode message for a toggle command.
		description=_("Toggles the function calls log."),
		category=ADDON_SUMMARY,
	)
	def script_toggleFunctionCallsLog(self, gesture):
		if self.enableFunctionCallsLog(not self.logEnabled):
			if self.logEnabled:
				# Translators: Reported when toggling the function call log feature.
				msg = _("Function calls log enabled for {function}").format(function=config.conf["ndtt"]["functionCallsLogTarget"])
			else:
				# Translators: Reported when toggling the function call log feature.
				msg = _('Function calls log disabled')
			ui.message(msg)

	@script(
		# Translators: Input help mode message for a toggle command.
		description=_("Toggles the function calls log method."),
		category=ADDON_SUMMARY,
	)
	def script_toggleFunctionCallsLogMethod(self, gesture):
		oldVal = config.conf["ndtt"]["functionCallsLogMethod"]
		if oldVal == LOG_METHOD_SETTRACE:
			newVal = LOG_METHOD_MONKEY_PATCHING
		elif oldVal ==  LOG_METHOD_MONKEY_PATCHING:
			newVal = LOG_METHOD_SETTRACE
		else:
			raise RuntimeError("Unexpected function calls log method: {}".format(val))
		config.conf["ndtt"]["functionCallsLogMethod"] = newVal
		# Translators: Reported when toggling the function calls log method.
		ui.message(_("Function calls log uses {method}").format(
			method=next(label for val, label in logMethodDisplayStrings if val == newVal),
		))
	
	def enableFunctionCallsLog(self, enable=True):
		if enable:
			if config.conf["ndtt"]["functionCallsLogMethod"] == LOG_METHOD_SETTRACE:
				from .fileOpener import getObject, FileOpenerError
				try:
					func = getObject(config.conf["ndtt"]["functionCallsLogTarget"])
				except FileOpenerError:
					# Translators: Reported when toggling the function calls log feature.
					ui.message("{func} is not a valid function name.".format(func=config.conf["ndtt"]["functionCallsLogTarget"]))
					return False
				self._targetCode = self._getCodeObject(func)
				sys.settrace(self._traceFunc)
				try:
					# For NVDA >= 2026.1 (Python 3.13+)
					threading.settrace_all_threads(self._traceFunc)
				except AttributeError:
					# For NVDA < 2026.1 (Python 3.11 or lower)
					threading.settrace(self._traceFunc)
			elif config.conf["ndtt"]["functionCallsLogMethod"] ==  LOG_METHOD_MONKEY_PATCHING:
				if not self.enableMonkeyPatching():
					return False
			else:
				raise RuntimeError("Unexpected function calls log method: {}".format(config.conf["ndtt"]["functionCallsLogMethod"]))
			self.logEnabled = True
			self.logMethod = config.conf["ndtt"]["functionCallsLogMethod"]
		else:
			if self.logMethod == LOG_METHOD_SETTRACE:
				self._targetCode = None
				sys.settrace(None)
				threading.settrace(None)
			elif self.logMethod == LOG_METHOD_MONKEY_PATCHING:
				try:
					setattr(self.patchedObject, self.patchedFunctionName, self.monkeyPatchedFunction.originalFunction)
				except:
					import globalVars as gv
					gv.dbg = (self.patchedObject, self.patchedFunctionName, monkeyPatchedFunction)
					raise
				self.monkeyPatchedFunction = None
			elif self.logMethod  is None:
				# Disable may be called at add-on termination, even if there is currently no logging
				# In this case, do nothing
				pass
			else:
				raise RuntimeError("Unexpected function calls log method: {}".format(self.logMethod))
			self.logEnabled = False
			self.logMethod = None
		return True

	@staticmethod
	def _getCodeObject(func):
		"""Returns the object code of a function or method."""
		try:
			# Bound method (instance.method)
			# Get associated function
			func = func.__func__
		except AttributeError:
			pass
		try:
			# Python 3 (NVDA 2019.3 or higher)
			return func.__code__
		except AttributeError:
			# Python 2 (NVDA 2019.2.1 or lower)
			return func.func_code

	def _traceFunc(self, frame, event, arg):
		if getattr(self.threadState, "inTraceFunc", False):
			return self._traceFunc
		self.threadState.inTraceFunc = True
		try:
			if event == "return" and frame.f_code is self._targetCode:
				self.logTraceFunc(frame)
		finally:
			self.threadState.inTraceFunc = False
		return self._traceFunc

	def logTraceFunc(self, frame):
		stack = traceback.format_stack(frame)
		log.debug(
			"Function call trace for %s (thread=%s):\n%s",
			config.conf["ndtt"]["functionCallsLogTarget"],
			threading.current_thread().name,
			"".join(stack),
		)

	def enableMonkeyPatching(self):
		from .fileOpener import getObject, FileOpenerError
		location, funcName = config.conf["ndtt"]["functionCallsLogTarget"].rsplit(".", 1)
		try:
			patchedObject = getObject(location)
		except FileOpenerError:
			# Translators: Reported when toggling the function calls log feature.
			ui.message("{location} is not a valid name.".format(location=location))
			return False
		try:
			originalFunction = getattr(patchedObject, funcName)
		except AttributeError:
			# Translators: Reported when toggling the function calls log feature.
			ui.message(_("{name} is not a valid function name.").format(name=funcName))
			return False

		def monkeyPatchedFunction(*args, **kw):
			res = monkeyPatchedFunction.originalFunction(*args, **kw)
			frame = inspect.currentframe()
			self.logTraceFunc(frame)
			return res

		monkeyPatchedFunction.originalFunction = originalFunction
		self.patchedObject = patchedObject
		self.patchedFunctionName = funcName
		self.monkeyPatchedFunction = monkeyPatchedFunction
		setattr(self.patchedObject, self.patchedFunctionName, monkeyPatchedFunction)
		return True

	def terminate(self):
		if not self.enableFunctionCallsLog(False):
			log.error("Error disabling stk trace log")
		super(GlobalPlugin, self).terminate()
