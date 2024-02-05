# -*- coding: UTF-8 -*-
# NVDA add-on: Character Information
# Copyright (C) 2024 Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING.txt for more details.

import ui
import buildVersion

nvdaTranslations = _

currentVersion = (buildVersion.version_year, buildVersion.version_major, buildVersion.version_minor)


def secureBrowseableMessage(message, title=None, isHtml=False):
	"""Call securely `ui.browseableMessage`.

	`ui.browseableMessage` is impacted by GHSA-xg6w-23rw-39r8
	(see https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994)
	This function should be used instead if you do not fully control what is passed as title of
	`ui.browseableMessage`.
	"""

	if not hasFix_GHSA_xg6w_23rw_39r8():
		# NVDA <= 2023.3.3
		if title is None:
			# The translation of NVDA's ui.browseableMessage title
			titleToCheck = nvdaTranslations("NVDA Message")
		else:
			titleToCheck = title
		if currentVersion < (2023, 1, 0):
			# Before #14668 (NVDA < 2023.1)
			sep = ";"
		else:
			sep = "__NVDA:split-here__"
		if sep in titleToCheck:
			raise RuntimeError('"{sep}" not allowed in the title of browseable messages'.format(sep=sep))
	return ui.browseableMessage(message, title, isHtml)


def hasFix_GHSA_xg6w_23rw_39r8():
	fixedVersion = (2023, 3, 3)
	return currentVersion >= fixedVersion
