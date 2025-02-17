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
	def __init__(self, text, ctx=None, n=None):
		self.text = text
		self.ctx = ctx
		self.n = n


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self._reverseCatalog = None
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
		description=_("Perform a reverse UI translation of the last speech"),
		category=ADDON_SUMMARY,
		speakOnDemand=True,
	)
	def script_reverseUITranslation(self, gesture):
		if not self.reverseCatalog:
			# Translators: An error message when calling the reverse UI translation command
			ui.message(_("Reverse translation not available for this version of NVDA."))
			return
		if self.lastSpeechString is None:
			# Translators: An error message when calling the reverse UI translation command
			ui.message(_("No last spoken text"))
		try:
			valList = self.reverseCatalog[self.lastSpeechString]
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
		ui.message(_("Message not found in translation catalog"))

	def _get_reverseCatalog(self):
		if not self._reverseCatalog:
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
			catalog = trans._catalog
			reverseCatalog = {}
			for (k, v) in catalog.items():
				if k == '':
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
				reverseCatalog[localeString].append(ReverseCatalogValue(englishString, ctxString, n))
			self._reverseCatalog = reverseCatalog
		return self._reverseCatalog

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
