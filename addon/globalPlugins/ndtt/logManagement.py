# -*- coding: UTF-8 -*-
# NVDA Dev & Test Toolbox add-on for NVDA
# Copyright (C) 2022-2023 Cyrille Bougot
# This file is covered by the GNU General Public License.

from __future__ import unicode_literals

import os
import sys
from glob import glob
import shutil
from datetime import datetime, timedelta
try:
	from datetime import timezone
	tzUTC = timezone.utc
except ImportError:
	from datetime import tzinfo

	class UTC(tzinfo):
		"""UTC"""

		def utcoffset(self, dt):
			return timedelta(0)

		def tzname(self, dt):
			return "UTC"

		def dst(self, dt):
			return timedelta(0)
	tzUTC = UTC()
# For Python 2.7, open the open of Python 3, allowing to specify encoding.
from io import open
import weakref
import re

import wx

import globalVars
import globalPluginHandler
import addonHandler
import queueHandler
import logHandler
from logHandler import log
import gui
from gui import guiHelper, nvdaControls
from gui import messageBox
try:
	from gui.dpiScalingHelper import DpiScalingHelperMixinWithoutInit
except ImportError:
	from .compa import DpiScalingHelperMixinWithoutInit
from .compa import matchDict
from .fileOpener import openSourceFile, FileOpenerError
from .ndttGui import NDTTSettingsPanel
from .utils import getBaseProfileConfigValue

addonHandler.initTranslation()

ADDON_SUMMARY = addonHandler.getCodeAddon().manifest["summary"]

TOKEN_INITIALIZATION = 'NDTT - Log management initialization: '
DT_FORMAT_STRING = '%Y-%m-%d_%H-%M-%S'

RES_LOG_BACKUP_FILENAME = (
	r'nvda_'
	r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})_(?P<hour>\d{2})-(?P<minute>\d{2})-(?P<second>\d{2})'
	r'\.log'
)
RE_LOG_BACKUP_FILENAME = re.compile(RES_LOG_BACKUP_FILENAME)
RE_BACKUP_LOG_PATH = re.compile(r'^.+\\{filename}$'.format(filename=RES_LOG_BACKUP_FILENAME))
RE_FIRST_LINE = re.compile(
	r'^INFO - __main__ \((?P<hour>\d{2}):(?P<minute>\d{2}):(?P<second>\d{2}).(?P<millisecond>\d{3})\)'
	r'(?: - MainThread \(\d+\))?:$'
)


def getStartTimeLoggedByNDTT(path):
	with open(path, 'r', encoding='utf8') as f:
		for line in f:
			if line.startswith(TOKEN_INITIALIZATION):
				dtString = line[len(TOKEN_INITIALIZATION):].strip()
				return dtString
	return None


def getFirstTimeLoggedByNVDA(path):
	with open(path, 'r', encoding='utf8') as f:
		line = f.readline()
		m = matchDict(RE_FIRST_LINE.match(line.strip()))
		localTimezone = datetime.now(tz=tzUTC).astimezone().tzinfo
		dt = datetime.now()
		dt = dt.replace(
			hour=int(m['hour']),
			minute=int(m['minute']),
			second=int(m['second']),
			microsecond=int(m['millisecond']) * 1000,
			tzinfo=localTimezone,
		)
		utcTime = datetime.utcfromtimestamp(dt.timestamp()).time()
		return utcTime


def saveOldLog():
	if getBaseProfileConfigValue('ndtt', 'logBackup') == 'off':
		return True
	try:
		logDirPath = os.path.dirname(globalVars.appArgs.logFileName)
		oldLogFilePath = os.path.join(logDirPath, "nvda-old.log")
		# Python 3's open raises FileNotFoundError and Python 2 IOError, so define the error on which to filter
		if sys.version_info.major >= 3:
			CommonFileNotFoundError = IOError
		else:
			CommonFileNotFoundError = IOError
		try:
			dtStartStr = getStartTimeLoggedByNDTT(oldLogFilePath)
		except CommonFileNotFoundError:
			log.debugWarning('No nvda-old.log file to backup in {}'.format(logDirPath))
			return True
		if not dtStartStr:
			log.debugWarning(
				'No NDTT time found in the log ({path}); fallback to NVDA time and file date.'.format(
					path=oldLogFilePath
				)
			)
			stat = os.stat(oldLogFilePath)
			dtEnd = datetime.utcfromtimestamp(stat.st_mtime)
			timeStart = getFirstTimeLoggedByNVDA(oldLogFilePath)

			# Create dtSTart with same D/M/Y values than dtEnd, assuming that the start time was logged the same day.
			# Then if dtStart after dtEnd remove one day.
			# This is not bullet proof but that's the best we can do without a logged time by NDTT.
			dtStart = dtEnd.replace(
				hour=timeStart.hour,
				minute=timeStart.minute,
				second=timeStart.second,
				microsecond=timeStart.microsecond,
			)
			if dtStart > dtEnd:
				dtStart = dtStart - timedelta(days=1)
			dtStartStr = dtStart.strftime(DT_FORMAT_STRING)
		savedLogFileName = "nvda_{}.log".format(dtStartStr)
		savedLogFilePath = os.path.join(logDirPath, savedLogFileName)
		shutil.copy(oldLogFilePath, savedLogFilePath)
		log.debug('Old log backup: {}'.format(savedLogFilePath))
		return True
	except Exception:
		msg = 'Unable to back up old log'
		log.error(msg, exc_info=True)
		return False


def logsCleanup():
	if getBaseProfileConfigValue('ndtt', 'logBackup') == 'off':
		return
	logDirPath = os.path.dirname(globalVars.appArgs.logFileName)
	logList = listLogFiles(logDirPath)
	if getBaseProfileConfigValue('ndtt', 'logBackup') == 'maxNumber':
		nMax = getBaseProfileConfigValue('ndtt', 'logBackupMaxNumber')
		for file in logList[:-nMax]:
			log.debug('Removing {file}'.format(file=file))
			try:
				os.remove(file)
			except Exception:
				log.warning('Unable to remove {file}', exc_info=True)

		return
	raise NotImplementedError


def listLogFiles(folderPath):
	pattern = os.path.join(folderPath, "nvda_*-*-*_*-*-*.log")
	return sorted([p for p in glob(pattern) if RE_BACKUP_LOG_PATH.match(p)])


def getAvailableLogs(folderPath):
	return [Log(os.path.split(name)[1], folderPath) for name in listLogFiles(folderPath)]


def moduleInitialize():
	"""Called at module initialization.
	This functions handles the tasks that need to be performed as early as possible, i.e. when the module is
	imported:
	- Saves the old log
	- Log start date and time
	These tasks are performed only at the first import and not when the module is reloaded with NVDA+control+F3
	(reload plugins command).
	"""

	try:
		logHandler.ndttLogManagementModuleInitialized
		return
	except AttributeError:
		pass
	# Log the start date/time
	log.info('{token}{dt}'.format(token=TOKEN_INITIALIZATION, dt=datetime.utcnow().strftime(DT_FORMAT_STRING)))
	# Call logCleanup only when NVDA has finished startup actions, no need to do it as soon as the current
	# module is imported.
	queueHandler.queueFunction(queueHandler.eventQueue, logsCleanup)
	if not saveOldLog():
		return  # Initialization failed; we may retry it when reloading plugins.
	logHandler.ndttLogManagementModuleInitialized = True


class Log(object):
	def __init__(self, filename, folder):
		self.filename = filename
		self.folder = folder
		self.type = 'backup'
		self._date = None

	def __lt__(self, other):
		if self.date is None:
			return False
		if other.date is None:
			return True
		return self.date < other.date

	@property
	def fullPath(self):
		return os.path.join(self.folder, self.filename)

	@property
	def date(self):
		"""Date (UTC)
		"""

		if not self._date:
			m = matchDict(RE_LOG_BACKUP_FILENAME.match(self.filename))
			if m:
				self._date = datetime(
					int(m['year']),
					int(m['month']),
					int(m['day']),
					int(m['hour']),
					int(m['minute']),
					int(m['second']),
				)
			else:
				log.error(self.filename, stack_info=True)
		return self._date

	@property
	def displayedDate(self):
		if self.date is None:
			# Translators: Text appearing in the date column of the log manager when the date cnanot be determined.
			return _("Unknown")
		if sys.version_info.major >= 3:
			# Date is displayed in local time.
			localTimezone = datetime.now(tz=tzUTC).astimezone().tzinfo
			dt = self.date.replace(tzinfo=tzUTC).astimezone(tz=localTimezone)
			return dt.strftime('%X %x')
		else:
			dt = self.date
			return dt.strftime('%X %x (UTC)')


class LogsManagerDialog(
	DpiScalingHelperMixinWithoutInit,
	wx.Dialog  # wxPython does not seem to call base class initializer, put last in MRO
):
	@classmethod
	def _instance(cls):
		""" type: () -> LogsManagerDialog
		return None until this is replaced with a weakref.ref object. Then the instance is retrieved
		with by treating that object as a callable.
		"""
		return None

	def __new__(cls, *args, **kwargs):
		instance = LogsManagerDialog._instance()
		if instance is None:
			return super(LogsManagerDialog, cls).__new__(cls, *args, **kwargs)
		return instance

	def __init__(self, parent):
		if LogsManagerDialog._instance() is not None:
			return
		LogsManagerDialog._instance = weakref.ref(self)

		self.folder = os.path.dirname(globalVars.appArgs.logFileName)

		# Translators: The title of the Logs Manager Dialog
		title = _("Logs Manager")
		super(LogsManagerDialog, self).__init__(
			parent=parent,
			title=title,
			style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER | wx.MAXIMIZE_BOX,
		)
		mainSizer = wx.BoxSizer(wx.VERTICAL)
		firstTextSizer = wx.BoxSizer(wx.VERTICAL)
		listAndButtonsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=wx.BoxSizer(wx.HORIZONTAL))
		# Translators: the label for the text on top of the logs manager window.
		entriesLabel = _("Logs in {folder}").format(folder=self.folder)
		firstTextSizer.Add(wx.StaticText(self, label=entriesLabel))
		mainSizer.Add(
			firstTextSizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.TOP | wx.LEFT | wx.RIGHT,
		)
		self.logsList = listAndButtonsSizerHelper.addItem(
			nvdaControls.AutoWidthColumnListCtrl(
				parent=self,
				style=wx.LC_REPORT,
			),
			flag=wx.EXPAND,
			proportion=1,
		)
		# Translators: The label for a column in logs list
		self.logsList.InsertColumn(0, _("Date"), width=self.scaleSize(100))
		# Translators: The label for a column in logs list
		self.logsList.InsertColumn(1, _("Type"), width=self.scaleSize(100))
		# Translators: The label for a column in logs list
		self.logsList.InsertColumn(2, _("File name"), width=self.scaleSize(300))
		# self.logsList.Bind(wx.EVT_LIST_ITEM_FOCUSED, self.onListItemSelected)
		self.logsList.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.onListItemDeselected)
		self.logsList.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onListItemSelected)

		# this is the group of buttons that affects the currently selected log(s)
		entryButtonsHelper = guiHelper.ButtonHelper(wx.VERTICAL)
		# Translators: The label for a button in Logs Manager dialog to open the selected logs.
		self.openButton = entryButtonsHelper.addButton(self, label=_("&Open"))
		self.openButton.Disable()
		self.openButton.Bind(wx.EVT_BUTTON, self.onOpenClick)
		# Translators: The label for a button to delete the selected log(s) in Log Manager dialog.
		self.deleteButton = entryButtonsHelper.addButton(self, label=_("&Delete"))
		self.deleteButton.Disable()
		self.deleteButton.Bind(wx.EVT_BUTTON, self.onDeleteClick)
		listAndButtonsSizerHelper.addItem(entryButtonsHelper.sizer)

		mainSizer.Add(
			listAndButtonsSizerHelper.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND,
			proportion=1,
		)

		# the following buttons are more general and apply regardless of the current selection.
		generalActions = guiHelper.ButtonHelper(wx.HORIZONTAL)
		# Translators: The label of a button in Logs Manager to open the settings panel.
		self.openSettingsButton = generalActions.addButton(self, label=_("Settings..."))
		self.openSettingsButton.Bind(wx.EVT_BUTTON, self.onOpenSettingsClick)

		mainSizer.Add(
			generalActions.sizer,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.LEFT | wx.RIGHT
		)

		mainSizer.Add(
			wx.StaticLine(self),
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.ALL | wx.EXPAND
		)

		# Translators: The label of a button to close the logs manager dialog.
		closeButton = wx.Button(self, label=_("&Close"), id=wx.ID_CLOSE)
		closeButton.Bind(wx.EVT_BUTTON, lambda evt: self.Close())
		mainSizer.Add(
			closeButton,
			border=guiHelper.BORDER_FOR_DIALOGS,
			flag=wx.LEFT | wx.RIGHT | wx.BOTTOM | wx.CENTER | wx.ALIGN_RIGHT
		)
		self.Bind(wx.EVT_CLOSE, self.onClose)
		self.EscapeId = wx.ID_CLOSE

		mainSizer.Fit(self)
		self.SetSizer(mainSizer)
		self.refreshLogsList()
		self.SetMinSize(mainSizer.GetMinSize())
		# Historical initial size, result of L{self.addonsList} being (550, 350) as of commit 1364839447.
		# Setting an initial size on L{self.addonsList} by passing a L{size} argument when
		# creating the control would also set its minimum size and thus block the dialog from being shrunk.
		self.SetSize(self.scaleSize((763, 509)))
		self.CentreOnScreen()
		self.logsList.SetFocus()

	def refreshLogsList(self, activeIndex=0):
		self.logsList.DeleteAllItems()
		self.curLogs = []
		for oLog in sorted(getAvailableLogs(self.folder)):
			self.logsList.Append((
				oLog.displayedDate,
				oLog.type,
				oLog.filename,
			))
			self.curLogs.append(oLog)
		# select the given active log or the first log if not given
		curLogsLen = len(self.curLogs)
		if curLogsLen > 0:
			if activeIndex == -1:
				activeIndex = curLogsLen - 1
			elif activeIndex < 0 or activeIndex >= curLogsLen:
				activeIndex = 0
			self.logsList.Select(activeIndex, on=1)
			self.logsList.SetItemState(activeIndex, wx.LIST_STATE_FOCUSED, wx.LIST_STATE_FOCUSED)
		else:
			self.openButton.Disable()
			self.deleteButton.Disable()

	def getSelectedLogs(self):
		selected = []
		index = self.logsList.GetFirstSelected()
		while index != -1:
			name = self.logsList.GetItem(index, 2).Text
			oLog = Log(name, self.folder)
			selected.append((oLog, index))
			index = self.logsList.GetNextSelected(index)
		return selected

	def onListItemDeselected(self, evt):
		self.listItemSelectionModified(evt.GetIndex(), False)

	def onListItemSelected(self, evt):
		self.listItemSelectionModified(evt.GetIndex(), True)

	def listItemSelectionModified(self, index, selected):
		nSelected = self.logsList.SelectedItemCount
		self.openButton.Enable(nSelected > 0)
		self.deleteButton.Enable(nSelected > 0)

	def onClose(self, evt):
		self.DestroyChildren()
		self.Destroy()

	def onOpenClick(self, evt):
		self.logsList.SetFocus()
		missing = []
		selectedLogs = self.getSelectedLogs()
		for oLog, index in selectedLogs:
			try:
				openSourceFile(oLog.fullPath)
			except FileOpenerError as e:
				log.debugWarning(str(e))
				if e.errorType == FileOpenerError.ET_FILE_NOT_FOUND:
					missing.append(index)
				else:
					# Translators: A message displayed to the user when pressing the Open button in the logs manager dialog
					messageBox(message=e.getUserFriendlyMessage(), style=wx.ICON_ERROR, parent=self)
					return
		for index in sorted(missing, reverse=True):
			self.logsList.DeleteItem(index)
		if len(missing) == len(selectedLogs):
			# We open the message box only if no log can be opened
			# Translators: A message displayed to the user when pressing the Open button in the logs manager dialog
			msg = _('The selected log(s) is (are) not available anymore')
			messageBox(message=msg, style=wx.ICON_ERROR, parent=self)

	def onDeleteClick(self, evt):
		selectedLogs = self.getSelectedLogs()
		# Translators: A message displayed to the user when pressing the Delete button in the logs manager dialog
		msg = _("The following files will be removed:\n{logsList}\n\nWould you like to continue?").format(
			logsList='\n'.join(lg.filename for lg, idx in selectedLogs)
		)
		# Translators: The title of a dialog displayed to the user when pressing the Delete button in the
		# logs manager dialog
		caption = _('Confirm deletion')
		if messageBox(
			message=msg,
			caption=caption,
			style=wx.YES_NO | wx.NO_DEFAULT,
			parent=self,
		) == wx.NO:
			return
		deleted = []
		notDeleted = []
		for oLog, index in selectedLogs:
			try:
				os.remove(oLog.fullPath)
				deleted.append(index)
			except Exception:
				log.warning('Unable to remove {file}'.format(file=oLog.fullPath), exc_info=True)
				notDeleted.append(oLog.filename)
		for index in sorted(deleted, reverse=True):
			self.logsList.DeleteItem(index)
		if notDeleted:
			nNotDeleted = len(notDeleted)
			if nNotDeleted >= 5:
				# Translators: Message issued when 5 or more logs could not be deleted.
				msgNotDeleted = _("{nLogs} log files could not be deleted. See NVDA's log for details.").format(
					nLogs=nNotDeleted
				)
			else:
				# Translators: Message issued when 1 to 4 logs could not be deleted.
				msgNotDeleted = _("The following logs files could not be deleted.\n\n{file}").format(file=oLog.filename)
			# Translators: The title of a dialog displayed to the user when pressing the Delete button in
			# the logs manager dialog
			caption = _('Error')
			messageBox(
				message=msgNotDeleted,
				caption=caption,
				style=wx.ICON_ERROR,
				parent=self,
			)

	def onOpenSettingsClick(self, evt):
		wx.CallAfter(
			gui.mainFrame._popupSettingsDialog,
			gui.settingsDialogs.NVDASettingsDialog,
			NDTTSettingsPanel,
		)


class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.logsManager = self.toolsMenu.Append(
			wx.ID_ANY,
			# Translators: menu item label to open the logs manager dialog.
			_("&Logs manager..."),
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onLogsManager, self.logsManager)

	def onLogsManager(self, evt):
		gui.mainFrame.prePopup()
		d = LogsManagerDialog(gui.mainFrame)
		d.Show()
		gui.mainFrame.postPopup()

	def terminate(self, *args, **kwargs):
		try:
			self.toolsMenu.Remove(self.logsManager)
		except Exception:
			pass
		super(GlobalPlugin, self).terminate(*args, **kwargs)


moduleInitialize()
