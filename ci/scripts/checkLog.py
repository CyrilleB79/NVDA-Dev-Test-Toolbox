import sys
import re

def isExpectedErrorMessage(errMsg):
	TRACEBACK_START_MSG = "Traceback (most recent call last):"
	lines = errMsg.split('\n')
	if (
		lines[0].startswith("ERROR - audio.soundSplit.initialize")
		and lines[1] == "Could not initialize audio session manager"
	):
		return True
	if (
		lines[0].startswith("ERROR - audioDucking._setDuckingState")
		and lines[1] == "Unknown error when setting ducking state:  Error number: 0X800706BA"
	):
		return True
	try:
		tbIndex = lines.index(TRACEBACK_START_MSG)
	except ValueError:
		return False
	tbLines = [l.strip() for l in lines[tbIndex:]]
	if (
		lines[0].startswith("ERROR - unhandled exception")
		and tbIndex == 1
		# and 'File "audioDucking.pyc", line 84, in _setDuckingState' in tbLines
		and any(re.search(r'File "audioDucking\.pyc", line \d+, in initialize', l) for l in tbLines)
		and any(re.search(r'File "audioDucking\.pyc", line \d+, in _setDuckingState', l) for l in tbLines)
		and lines[-1] == "OSError: [WinError -2147023174] The RPC server is unavailable"
	):
		return True
	return False

def readLogMessages(filePath):
	logMessages = []
	currentMessage = []
	with open(filePath, encoding="utf-8") as f:
		for line in f:
			if line.lstrip().startswith(("DEBUG -", "INFO -", "WARNING -", "ERROR -", "IO -", "DEBUGWARNING -", "CRITICAL -")):
				if currentMessage:
					logMessages.append("".join(currentMessage).strip())
					currentMessage = []
			currentMessage.append(line)
		if currentMessage:
			logMessages.append("".join(currentMessage).strip())
	return logMessages

if len(sys.argv) < 2:
	print("Usage: checkLog.py <logFilePath>")
	sys.exit(2)

logFilePath = sys.argv[1]

nUnexpectedErr = 0
noExit = True

for message in readLogMessages(logFilePath):
	if message.startswith(("ERROR -", "CRITICAL -")):
		if isExpectedErrorMessage(message):
			continue
		print("===> Unexpected error:\n" + message + "\n")
		nUnexpectedErr += 1
	if message.endswith("NVDA exit"):
		noExit = False

if noExit:
	print("NVDA did not exit successfully")

exit(nUnexpectedErr + int(noExit))
