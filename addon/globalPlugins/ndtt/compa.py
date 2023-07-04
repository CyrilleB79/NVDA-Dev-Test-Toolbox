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


def matchDict(m):
	"""A helper function to get the match dictionary (useful in Python 2)
	"""

	if not m:
		return m
	return m.groupdict()


# Copied from gui\dpiScalingHelper.py
def scaleSize(scaleFactor, size):
	"""Helper method to scale a size using the logical DPI
	@param size: The size (x, y) as a tuple or a single numerical type to scale
	@returns: The scaled size, as a float or tuple of floats.
	"""
	if isinstance(size, tuple):
		return (scaleFactor * size[0], scaleFactor * size[1])
	return scaleFactor * size


# Copied from gui\dpiScalingHelper.py
def getScaleFactor(windowHandle):
	"""Helper method to get the window scale factor. The window needs to be constructed first, in
	order to get the window handle, this likely means calling the wx.window __init__ method prior
	to calling self.GetHandle()"""
	import windowUtils
	return windowUtils.getWindowScalingFactor(windowHandle)


# Copied from gui\dpiScalingHelper.py
class DpiScalingHelperMixinWithoutInit(object):
	"""Same concept as DpiScalingHelperMixin, but ensures you do not have to explicitly call the init
		of wx.Window or this mixin
	"""
	_scaleFactor = None

	def scaleSize(self, size):
		if self._scaleFactor is None:
			windowHandle = self.GetHandle()
			self._scaleFactor = getScaleFactor(windowHandle)
		return scaleSize(self._scaleFactor, size)


def getPanelDescriptionWidth():
	try:
		from gui.settingsDialogs import PANEL_DESCRIPTION_WIDTH
		return PANEL_DESCRIPTION_WIDTH
	except ImportError:
		# Not available before NVDA 2021.3:
		return 544


appDir = getApDir()
controlTypesCompatWrapper = ControlTypesCompatWrapper()
PANEL_DESCRIPTION_WIDTH = getPanelDescriptionWidth()
