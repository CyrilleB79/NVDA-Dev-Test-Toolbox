# Copyright (C) 2023-2025 Cyrille Bougot
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

"""A module to manage speak on-demand feature support for add-ons.
Compatible with NVDA 2019.2.1 and above.
"""

import threading

import speech
import core
from scriptHandler import script as original_script


def isSpeechOnDemandFeatureAvailable():
	"""Indicates if the speech on-demand feature is available in the current version of NVDA.
	"""

	try:
		# NVDA >= 2024.1
		speech.SpeechMode.onDemand
		return True
	except AttributeError:
		# NVDA <= 2023.3
		return False


def getSpeechOnDemandParameter():
	"""Returns a dictionary containing the speakOnDemand parameter and its True value for NVDA versions where
	this feature exists; returns an empty dictionary otherwise.
	Use `**getSpeechOnDemandParameter()` in script decorator's parameters to define `speakOnDemand=True` only
	for NVDA versions where this feature is supported.
	This syntax is only available with Python 3, thus with NVDA >= 2019.3.
	"""

	if isSpeechOnDemandFeatureAvailable():
		# Define on-demand parameter only if the feature is available.
		return {'speakOnDemand': True}
	else:
		return {}


def executeWithSpeakOnDemand(f, *args, **kwargs):
	"""Allows to execute a function forcing the on-demand mode for its execution.
	This may be useful for a functions that is scheduled by an on-demand script
	to be run after the script execution has finished, e.g. using `core.callLater`.
	This function should only be called from the main thread.

	Parameters:
	f: function to execute.
	args: unnamed arguments to pass to the function.
	kwargs: keyword arguments to pass to the function.
	"""

	if threading.get_ident() != core.mainThreadId:
		raise RuntimeError('This function should only be executed from the main thread.')

	if not isSpeechOnDemandFeatureAvailable() or speech.getState().speechMode != speech.SpeechMode.onDemand:
		return f(*args, **kwargs)
	try:
		speech.setSpeechMode(speech.SpeechMode.talk)
		return f(*args, **kwargs)
	finally:
		speech.setSpeechMode(speech.SpeechMode.onDemand)


def script(
	speakOnDemand = False,
	**kwargs  # Python 2: do not put tailing comma after **kwargs
):
	"""Define metadata for a script.
	This function is an extended version of NVDA's original scriptHandler.script decorator.
	It supports speakOnDemand parameter no matter the NVDA version, ignoring this parameter for NVDA versions
	which do not implement this feature.
	:param speakOnDemand: Whether this script should speak when NVDA speech mode is "on-demand"
	:param **kwargs: Other parameters supported by scripthHandler.script decorator.
	"""

	def script_decorator(decoratedScript):
		decoratedScript = original_script(**kwargs)(decoratedScript)
		decoratedScript.speakOnDemand = speakOnDemand
		return decoratedScript

	return script_decorator

	