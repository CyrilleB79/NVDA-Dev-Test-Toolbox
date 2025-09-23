# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import re

import wx

import globalPluginHandler
import addonHandler
import languageHandler
import api
import ui
try:
	# For NVDa 2024.2+
	from speech.extensions import pre_speech
except ImportError:  # Also catches ModuleNotFoundError)
	# For NVDA 2024.1 or below
	pre_speech = None
import speech
import core
import gui
import config
import globalVars
from logHandler import log

try:
	speechModule = speech.speech
except AttributeError:
	# For older version such as NVDA 2019.3.1 (probably < NVDA 2021.1)
	speechModule = speech

from .speechOnDemand import script


addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]


def removeAccel(s):
	"""Remove accelerator from a string.
	"""
	
	# Remove accelerator
	s = re.sub('&', '', s)

	return s


class ReverseCatalogValue:
	def __init__(self, text, ctx=None, n=None, addon=None):
		self.text = text
		self.ctx = ctx
		self.n = n
		self.addon = addon


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self._reverseCatalogs = None
		self._fullReverseCatalog = None
		if pre_speech:
			pre_speech.register(self.memorizeLastSpeechString)
		else:
			self._speak = speechModule.speak
			speechModule.speak = self._localSpeak
		self.lastSpeechString = None

	def _localSpeak(self, sequence, *args, **kwargs):
		self.memorizeLastSpeechString(sequence)
		self._speak(sequence, *args, **kwargs)

	def memorizeLastSpeechString(self, speechSequence):
		seq = (i for i in speechSequence if isinstance(i, str))
		try:
			self.lastSpeechString = next(seq)
		except StopIteration:
			# No update for speech strings with no text
			pass

	def terminate(self, *args, **kwargs):
		if pre_speech:
			pre_speech.unregister(self.memorizeLastSpeechString)
		else:
			speechModule.speak = self._speak
		super(GlobalPlugin, self).terminate(*args, **kwargs)

	@script(
		# Translators: Input help mode message for Reverse UI translation command
		description=_("Performs a reverse UI translation of the last speech, using NVDA translation catalogs."),
		category=ADDON_SUMMARY,
		speakOnDemand=True,
	)
	def script_reverseNVDAUITranslation(self, gesture):
		catalog = self.reverseCatalogs[""]
		self._reverseTranslate(catalog)

	@script(
		# Translators: Input help mode message for Reverse UI translation command
		description=_("Performs a reverse UI translation of the last speech, using NVDA and add-ons translation catalogs."),
		category=ADDON_SUMMARY,
		speakOnDemand=True,
	)
	def script_reverseUITranslation(self, gesture):
		catalog = self.fullReverseCatalog
		self._reverseTranslate(catalog)

	def _reverseTranslate(self, catalog):
		if not catalog:
			# Translators: An error message when calling the reverse UI translation command
			ui.message(_("Reverse translation not available for this version of NVDA."))
			return
		if self.lastSpeechString is None:
			# Translators: An error message when calling the reverse UI translation command
			ui.message(_("No last spoken text"))
		try:
			valList = catalog[self.lastSpeechString]
		except KeyError:
			pass
		else:
			if len(valList) == 1 or len(set(i.text for i in valList)) == 1:
				val = valList[0]
				self.reportAndCopyReverseTranslation(val.text)
				return
			elif len(valList) > 1:
				self.choiceMenu(valList)
				return
			else:
				RuntimeError('valList is empty')
		# Translators: An error message when calling the reverse UI translation command
		ui.message(_("Message not found in translation catalogs"))

	def getReverseCatalog(self, addon=None):
		if addon:
			trans = addon.getTranslationsInstance()
		else:
			try:
				# For NVDA version >= 2022.1
				trans = languageHandler.installedTranslation()
			except AttributeError:
				# For NVDA version < 2022.1
				return None
		try:
			if trans.CONTEXT != '%s\x04%s':
				raise RuntimeError('Unexpected context splitting rule')
		except AttributeError:
			pass  # trans.CONTEXT not available before Python 3.11, i.e. NVDA < 2024.1
		try:
			catalog = trans._catalog
		except AttributeError:
			# For add-ons
			log.debugWarning(
				"No translation of add-on {name} for {lang}".format(
					name=addon.name,
					lang=languageHandler.getLanguage(),
				)
			)
			return None
		reverseCatalog = {}
		for (k, v) in catalog.items():
			if k == "":
				continue
			if isinstance(k, tuple):
				(kString, n) = k
			else:
				kString = k
				n = None
			ctxSplitList = kString.split('\x04')
			if len(ctxSplitList) == 1:
				ctxString = None
				englishString = removeAccel(ctxSplitList[0])
			elif len(ctxSplitList) == 2:
				ctxString = ctxSplitList[0]
				englishString = removeAccel(ctxSplitList[1])
			else:
				RuntimeError('ctxSplitList = {}'.format(ctxSplitList))
			localeString = removeAccel(v)
			try:
				reverseCatalog[localeString]
			except KeyError:
				reverseCatalog[localeString] = []
			name = addon.name if addon else None
			reverseCatalog[localeString].append(ReverseCatalogValue(englishString, ctx=ctxString, n=n, addon=name))
		return reverseCatalog

	def _get_reverseCatalogs(self):
		if not self._reverseCatalogs:
			self._reverseCatalogs = {"": self.getReverseCatalog()}  # For NVDA
			self._reverseCatalogs.update({
				a.name: self.getReverseCatalog(a) for a in addonHandler.getRunningAddons()
			})
		return self._reverseCatalogs

	def _get_fullReverseCatalog(self):
		if not self._fullReverseCatalog:
			self._fullReverseCatalog = {}
			for (catName, catalog) in self.reverseCatalogs.items():
				if not catalog:
					log.debugWarning("No catalog for {catName}".format(catName=catName))
					continue
				self._fullReverseCatalog.update(catalog)	
		return self._fullReverseCatalog
	
	def reportAndCopyReverseTranslation(self, text):
		speech.cancelSpeech()
		ui.message(text)
		if config.conf['ndtt']['copyRevTranslation'] and not globalVars.appArgs.secure:
			api.copyToClip(text)

	def choiceMenu(self, valList):
		self.menu = wx.Menu()
		for val in valList:
			label = val.text
			if val.ctx is not None:
				label += ', context = {}'.format(val.ctx)
			if val.n is not None:
				label += ', n = {}'.format(val.n)
			if val.addon is not None:
				label += ", addon = {}".format(val.addon)
			self.menu.Append(
				wx.ID_ANY,
				label,
				val.text,
			)
			self.menu.Bind(wx.EVT_MENU, lambda evt: self.onChoice(evt, val))

		def openMenu():
			gui.mainFrame.prePopup()
			gui.mainFrame.sysTrayIcon.PopupMenu(self.menu)
			gui.mainFrame.postPopup()
		wx.CallLater(0, openMenu)
	
	def onChoice(self, evt, val):
		core.callLater(100, lambda: self.reportAndCopyReverseTranslation(val.text))
