# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2024-2025 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import sys
import re
import gettext

import wx

import globalPluginHandler
import addonHandler
import languageHandler
import api
import ui
import buildVersion
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

# Return codes to build reverse catalogs.
BRC_SUCCESS = 0
BRC_ERROR_UNSUPPORTED_NVDA_VERSION = 1
BRC_ERROR_NVDA_TRANSLATION_NOT_AVAILABLE = 2
BRC_ERROR_ADDON_TRANSLATION_NOT_AVAILABLE = 4


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

	def __repr__(self):
		return "{name}(text={text}, ctx={ctx}, n={n}, addon={addon})".format(
			name=self.__class__.__name__,
			text=self.text,
			ctx=self.ctx,
			n=self.n,
			addon=self.addon,
		)


class ReverseCatalogs:
	def __init__(self):
		self.catalogs = {}

	def add(self, dicCatalogs):
		self.catalogs.update(dicCatalogs)

	def __getitem__(self, key):
		return self.catalogs[key]

	def items(self):
		return self.catalogs.items()


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self._reverseCatalogs = None
		self._mergedReverseCatalog = None
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
		if sys.version_info.major == 2:
			unicodeStr = unicode
		else:
			unicodeStr = str
		seq = (i for i in speechSequence if isinstance(i, unicodeStr))
		try:
			self.lastSpeechString = next(seq)
		except StopIteration:
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
		try:
			self._reverseTranslate()
		except LookupError:
			# Translators: An error message when calling the NVDA reverse UI translation command
			ui.message(_("Message not found in NVDA's translation catalog"))

	@script(
		# Translators: Input help mode message for Reverse UI translation command
		description=_("Performs a reverse UI translation of the last speech, using NVDA and add-ons translation catalogs."),
		category=ADDON_SUMMARY,
		speakOnDemand=True,
	)
	def script_reverseUITranslation(self, gesture):
		try:
			self._reverseTranslate(withAddons=True)
		except LookupError:
			# Translators: An error message when calling the NVDA+add-ons reverse UI translation command
			ui.message(_("Message not found in NVDA's and addons translation catalogs"))

	def _reverseTranslate(self, withAddons=False):
		if withAddons:
			catalog, errCode = self.mergedReverseCatalog
			if errCode != BRC_SUCCESS:
				# Translators: An error message when calling the reverse UI translation command
				ui.message(_("Reverse translation not available."))
				return
		else:
			catalog, errCode = self.nvdaReverseCatalog
			if errCode == BRC_ERROR_UNSUPPORTED_NVDA_VERSION:
				# Translators: An error message when calling the reverse UI translation command for older NVDA versions
				ui.message(_("Retrieving translated strings of NVDA not supported for this version of NVDA."))
				return
			if errCode == BRC_ERROR_NVDA_TRANSLATION_NOT_AVAILABLE:
				# Translators: An error message when calling the reverse UI translation command while NVDA is in English
				ui.message(_("Reverse translation not available: NVDA is not translated."))
				return
		if self.lastSpeechString is None:
			# Translators: An error message when calling the reverse UI translation command
			ui.message(_("No last spoken text"))
			return
		try:
			valList = catalog[self.lastSpeechString]
		except KeyError:
			if (
				(buildVersion.version_year, buildVersion.version_major) >= (2019, 3)
				or "  " not in self.lastSpeechString
			):
				raise LookupError
			# Pre-speech refactor (NVDA < 2019.3)
			# Content strings are concatenated with role, state, shortcut, etc.
			# So fall back splitting the original string with "  " and taking the first part.
			try:
				valList = catalog[self.lastSpeechString.split("  ")[0]]
			except KeyError:
				raise LookupError
			log.debugWarning("Found fallback reverse translation string splitting the original string with '  '.")
		if len(valList) == 1 or len(set(i.text for i in valList)) == 1:
			val = valList[0]
			self.reportAndCopyReverseTranslation(val.text)
			return
		elif len(valList) > 1:
			self.choiceMenu(valList)
			return
		else:
			raise RuntimeError('valList is empty')

	def buildReverseCatalog(self, addon=None):
		if addon:
			trans = addon.getTranslationsInstance()
		else:
			try:
				# For NVDA version >= 2022.1
				trans = languageHandler.installedTranslation()
			except AttributeError:
				# For NVDA version < 2022.1
				log.debugWarning(
					"NVDA translations not retrieved for NVDA version before 2022.1."
				)
				return None, BRC_ERROR_UNSUPPORTED_NVDA_VERSION
		if not isinstance(trans, gettext.GNUTranslations):
			log.debugWarning(
				"No translation of {name} for {lang}".format(
					name=("addon " + addon.name) if addon else "NVDA",
					lang=languageHandler.getLanguage(),
				)
			)
			return None, (BRC_ERROR_ADDON_TRANSLATION_NOT_AVAILABLE if addon else BRC_ERROR_NVDA_TRANSLATION_NOT_AVAILABLE)
		try:
			if trans.CONTEXT != '%s\x04%s':
				raise RuntimeError('Unexpected context splitting rule')
		except AttributeError:
			pass  # trans.CONTEXT not available before Python 3.11, i.e. NVDA < 2024.1
	
		reverseCatalog = {}
		for (k, v) in trans._catalog.items():
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
				sourceString = removeAccel(ctxSplitList[0])
			elif len(ctxSplitList) == 2:
				ctxString = ctxSplitList[0]
				sourceString = removeAccel(ctxSplitList[1])
			else:
				RuntimeError('ctxSplitList = {}'.format(ctxSplitList))
			localeString = removeAccel(v)
			try:
				reverseCatalog[localeString]
			except KeyError:
				reverseCatalog[localeString] = []
			reverseCatalog[localeString].append(ReverseCatalogValue(
				sourceString,
				ctx=ctxString,
				n=n,
				addon=addon.name if addon else None,
			))
		return reverseCatalog, BRC_SUCCESS

	def _get_reverseCatalogs(self):
		if not self._reverseCatalogs:
			self._reverseCatalogs = ReverseCatalogs()
			log.debug("Building reverse catalog for NVDA.")
			self._reverseCatalogs.add({"": self.buildReverseCatalog()})  # For NVDA
			log.debug("Building reverse catalog for add-ons.")
			self._reverseCatalogs.add({
				a.name: self.buildReverseCatalog(a) for a in addonHandler.getRunningAddons()
			})
		return self._reverseCatalogs

	def _get_nvdaReverseCatalog(self):
		return self.reverseCatalogs[""]

	def _get_mergedReverseCatalog(self):
		if not self._mergedReverseCatalog:
			globalErrCode = BRC_SUCCESS
			anyTranslationPresent = False
			mergedReverseCatalog = {}
			for (catName, (catalog, errCode)) in self.reverseCatalogs.items():
				if catalog is None:
					globalErrCode |= errCode
					log.debugWarning("No catalog for {catName}".format(catName=(catName if catName else "NVDA")))
					continue
				else:
					 anyTranslationPresent = True
				for (translated, catValueList) in catalog.items():
					try:
						mergedReverseCatalog[translated]
					except KeyError:
						mergedReverseCatalog[translated] = []
					mergedReverseCatalog[translated].extend(catValueList)
			self._mergedReverseCatalog = mergedReverseCatalog, (BRC_SUCCESS if anyTranslationPresent else globalErrCode)
		return self._mergedReverseCatalog
	
	def reportAndCopyReverseTranslation(self, text):
		speech.cancelSpeech()
		ui.message(text)
		if config.conf['ndtt']['copyRevTranslation'] and not globalVars.appArgs.secure:
			api.copyToClip(text)

	def choiceMenu(self, valList):
		self.menu = wx.Menu()
		menuItems = []
		for val in valList:
			label = val.text
			if val.ctx is not None:
				label += ', context = {}'.format(val.ctx)
			if val.n is not None:
				label += ', n = {}'.format(val.n)
			if val.addon is not None:
				label += ", addon = {}".format(val.addon)
			menuItems.append(((val.text, val.ctx, val.n, val.addon), label))
		# Convert to dict to remove duplicate
		menuItems = dict(menuItems)
		for label in menuItems.values():
			self.menu.Append(
				wx.ID_ANY,
				label,
			)
			self.menu.Bind(wx.EVT_MENU, lambda evt: self.onChoice(evt, val))

		def openMenu():
			gui.mainFrame.prePopup()
			gui.mainFrame.sysTrayIcon.PopupMenu(self.menu)
			gui.mainFrame.postPopup()
		wx.CallLater(0, openMenu)
	
	def onChoice(self, evt, val):
		core.callLater(100, lambda: self.reportAndCopyReverseTranslation(val.text))
