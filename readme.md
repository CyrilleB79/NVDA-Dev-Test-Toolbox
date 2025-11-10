# NVDA Dev & Test Toolbox

* Author: Cyrille Bougot
* NVDA compatibility: 2019.2 and beyond
* Download [stable version][1]

This add-on gathers various features for NVDA debugging and testing.

## Features

* An enhanced restart dialog to specify some extra options when restarting NVDA.
* Various features related to logged errors.
* An object property explorer.
* Script tools: an extended script description mode and a script opener.
* Commands to help log reading and analyzing.
* Backups of old logs
* A command to anonymize a log
* Python console enhancements such as a custom startup script and the possibility to preserve input history in memory after NVDA restarts.
* In the Python console workspace, a function to open the source code of an object.
* A command to log the stack trace of the speech.speak function.
* A command to reverse translate the items of the interface.

## Commands

This add-on uses layered commands for all of the new commands it adds.
The entry point for these commands is `NVDA+X`; thus all the commands should be executed by `NVDA+X` followed by another single letter or gesture.
You can list all the available layered commands pressing `NVDA+X, H`.

For the commands that you use more frequently, you can also define a direct gesture in the input gesture dialog.

## Enhanced restart dialog

The `NVDA+X, Q` command opens a dialog to specify some extra options before restarting NVDA.
The options that can be specified correspond to the [command line options][2] that can be used with `nvda.exe`, e.g. `-c` for config path, `--disable-addons` to disable add-ons, etc.

## Features related to logged errors

### Report last logged error

Pressing `NVDA+X, E` allows to report the last error logged without needing to open the log. A second press clears the memorized last error.

### Play a sound for logged errors

The ["Play a sound for logged errors" setting][4] has been introduced in NVDA 2021.3 and allows to specify if NVDA will play an error sound in case an error is logged.

This add-on provides an additional command (`NVDA+X, shift+E`) to toggle this setting.
You can choose:

* "Only in test versions" (default) to make NVDA play error sounds only if the current NVDA version is a test version (alpha, beta or run from source).
* "Yes" to enable error sounds no matter your current NVDA version. 

For NVDA prior to 2021.3, this add-on provides the backport of this feature and the possibility to control it with the keyboard command.
The checkbox in the Advanced settings panel is not backported however.

## Object property explorer

This feature allows to report some properties of the current navigator object without opening the log viewer.

To list the properties of an object, move the navigator object to it and use the following commands:

* `NVDA+X, upArrow`: Selects the previous property and reports it for the navigator object.
* `NVDA+X, downArrow`: Selects the next property and reports it for the navigator object.
* `NVDA+X, N`: Reports the currently selected property for the navigator object
* `NVDA+X, shift+N`: Displays the currently selected property for the navigator object in a browseable message

The list of the supported properties is the following:
name, role, state, value, windowClassName, windowControlID, windowHandle, location, Python class, Python class mro.

When using object navigation commands, you can also choose to have the currently selected property reported instead of NVDA usual object reporting.
A toggle command, `NVDA+X, control+N`, allows to switch between this custom reporting of objects and NVDA usual reporting.

For exemple, you may select "windowClassName" property and enable custom object reporting.
Then when moving the navigator object to next or previous object, you will hear the object's windowClassName instead of usual reporting.

## Script tools

<a id="scriptOpener"></a>
### The script opener

The script opener command allows to open the code of a script knowing its gesture.

To use it press `NVDA+x, C` and then the gesture of the script which you want to see the code of.
For example to see the code of the script that reports the title of the foreground window, press `NVDA+X, C` and then `NVDA+T`.

For this feature to work, you need to have configured your [favorite editor's command](#settingsOpenCommand) in the add-on's settings.
If you are not running NVDA from source, the [location of NVDA source code](#settingsNvdaSourcePath) should also have been configured.

### Extended script description mode

The extended script description mode allows to have reported information on scripts without description in input help mode.

When the Extended script description mode is active, the input help mode (NVDA+1) is modified as follows.
If a script has no description, the script's name and class are reported.
If a script has a description, its description is reported as usual.
The gesture to activate or deactivate this feature is `NVDA+X, D`.

Executing a gesture bound to a script without description in input help mode also create an entry for this script in the gesture management dialog.
This entry is located in a dedicated category called "Scripts without description (modify at your own risk!)".
This allow to easily add, delete or change the native NVDA gestures for these script.
Be aware however that it is often intended that such script do not have any description to prevent the user to modify the associated gesture.
Indeed, the gesture may be defined to match an application shortcut key.
For example the script script_toggleItalic on NVDAObjects.window.winword.WordDocument is bound to control+I and this should not be modified since the gesture is passed to the application to actually execute the shortcut key.

#### Usage example

Control+shift+I also toggle italic in Word, even if it is not natively reported by NVDA.
To have the control+shift+I result reported by NVDA as control+I, you should perform the following steps:

* Open a Word document.
* Enable the extended script description mode with `NVDA+X, D`.
* Enter input help mode with NVDA+1.
* Press control+I to report the italic script and have it added in the gesture dialog.
* Exit input help mode with NVDA+1.
* Open the input gestures dialog.
* In the category "Scripts without description (modify at your own risk!)", select the command "toggleItalic on NVDAObjects.window.winword.WordDocument".
* Add the control+shift+I shortcut and validate.
* If you want, exit the extended script description mode with `NVDA+X, D`.

Known bug: A script added for a specific class is visible even if gesture manager is opened in another context.

## Log reading and analyzing features

<a id="logPlaceMarkers"></a>
### Place markers in the log

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press `NVDA+X, K`.
A message as follows will be logged at INFO level:  
`-- NDTT marker 0 --`  
You can add as many markers as you want in the log.
The marker's number will be incremented each time you place a marker in the log; it will only be reset when NVDA is restarted.

### Log reader mode

A log reader mode provides commands to ease log reading and analyzing.
In the log viewer window and in the Pyton console output area, the log reader is enabled by default, thus log reading commands are available immediately.
In another text reading area such as an editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press `NVDA+X, L` to enable log reader mode and use its commands.
When you are done with log reading and analyzing tasks, you can disable again `NVDA+X, L` to disable the log reader mode.

The commands available in log reader mode are described hereafter.
In this mode, you can also press `control+H` to display all the commands available.

<a id="logReaderQuickNavigationCommands"></a>
#### Quick navigation commands

Single letter command similar to browse mode quick navigation keys allow to move to various type of log messages:

* m: any message
* e: error messages (`ERROR` and `CRITICAL`)
* w: warning messages (`WARNING`)
* f: info messages (`INFO`)
* k: markers previously [placed in the log](#logPlaceMarkers)
* g: debug warning messages (`DEBUGWARNING`)
* i: input/output messages (`IO`)
* n: input messages
* s: speech messages
* b: braille messages
* d: debug messages (`DEBUG`)

Pressing the single letter moves to the next occurrence of this message. Combining the letter with the shift key moves to the previous occurrence of this message.

In addition, inside certain types of messages, you can jump block by block pressing `O`  or `shift+O`.
The following message types and associated blocks are supported:

* In messages containing tracebacks, e.g. error messages, block navigation allows you to jump between tracebacks
  This is specifically useful when more than one traceback is present, e.g. when an error is raised in the "except" part of a try/except clause.
* In the message listing the stacks for Python threads logged when a freeze occurs, block navigation allows you to jump between thread stacks.
* In the message providing developer info for the navigator object logged when you press `NVDA+F1`, block navigation allows you to jump between groups of properties.
  There are four groups of properties: general properties, appModule properties, window properties and interface-specific (IAccessible, UIA) properties.

At last, inside a block, you may want to jump quickly to first or last line of interest of the block.
Use `shift+L` to jump to the first line of interest of the current block's content, e.g. the first frame of a traceback.
And `L` to jump to the last line of interest of the block's content, e.g. last frame of a thread stack or error below a traceback.

#### Translation of speech message

Sometimes, you may have to look at a log taken on a system in a foreignh language that you do not understand. E.g. the log was taken on a Chinese system / NVDA, whereas you only understand French.
If you have [Instant Translate][3] add-on installed, you may use it in conjonction with [quick log navigation commands](#logReaderQuickNavigationCommands) to have speech messages translated.

* First configure Instant Translate's languages. The source language should be the language of the system where the log has been taken (e.g. Chinese). The target language should be your language (e.g. French).
* Open the log
* Press `control+T` to enable automatic speech translation in the log
* Use Quick navigation commands in the log, e.g. S, I, etc. Whenever a speech message is encountered, it will be spoken in your language (French in our previous example)

If you want to disable speech translation, press `control+T` again.

<a id="logReaderOpenSourceFile"></a>
#### Open the file of the source code in your editor

In the log some line may refer to the source code:

* A line belonging to a traceback contains the path and the line in a file, e.g.:  
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* The header line of a logged message contains the function which has logged this message, e.g.:  
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* The content of a message logged in input help mode (logged at info level):  
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

You may want to open the file containing this code to understand the context of the traceback or the logged message.
Just press C to open this file.

For this feature to work, you need to have configured your [favorite editor's command](#settingsOpenCommand) in the add-on's settings.
If you are not running NVDA from source, the [location of NVDA source code](#settingsNvdaSourcePath) should also have been configured.

#### Analysing a traceback

Sometimes you may have error tracebacks in the log, as in the following example:
```
ERROR - scriptHandler.executeScript (14:47:43.426) - MainThread (15492):
error executing script: <bound method LogContainer.script_openSourceFile of <NVDAObjects.Dynamic_LogViewerLogContainerIAccessibleRichEdit50WindowNVDAObject object at 0x34C1E510>> with gesture 'c'
Traceback (most recent call last):
  File "scriptHandler.pyc", line 300, in executeScript
  File "C:\Users\myUserName\AppData\Roaming\nvda\addons\nvdaDevTestToolbox\globalPlugins\ndtt\logReader.py", line 603, in script_openSourceFile
    if self.openStackTraceLine(line):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\myUserName\AppData\Roaming\nvda\addons\nvdaDevTestToolbox\globalPlugins\ndtt\logReader.py", line 667, in openStackTraceLine
    0 / 0  # An erroneaous code line
    ~~^~~
ZeroDivisionError: division by zero
```

For frames where the source code is available, you may have noticed markers with `^` (caret) and `~` (tilde) characters.
That's the way Python visually indicates the error's location as well as its context in a traceback frame.
Pressing `control+E` moves the cursor at the beginning of the error in the source code line, i.e. the text marked by `^` (caret) character.
A double press, select this text.
A triple press selects the error with its context, i.e. the text of the source code line marked by `^` (caret) and `~` (tilde) characters.

Please note that for logs taken with an NVDA version before 2024.1, thus with Python 3.7 or older, Python only indicates the error with one `^` (caret) character.
Thus the double or triple press action of this command becomes rather useless.

#### Getting a summary of the available commands

To display a list of all the available commands in log reading mode, press `NVDA+X, H`.

## Anonymize a log

When reporting issues, you may have to provide a log.
However, logs may contain sensitive information (user names, e-mails, etc.).
This add-on provides a command to anonymize a log's content.

Select a part of the log or its whole content and press `NVDA+X, A`.
The anonymized log content will be put in the clipboard.
You can paste it on the current selection to replace it or anywhere else you wish.

For this feature to work, you need to customize the anonymization rules used by this command.
The file to configure these rules is located at: `pathToNVDAConfig\ndtt\anonymizationRules.dic` (e.g. `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`).
You will find all the instructions to write this file in its header.
In case you have corrupted your anonymization rules file or if you have deleted the header's instructions, just delete or rename this file and a new version of this file will be generated at next startup.

<a id="oldLogsBackup"></a>
## Backup of old logs

NVDA already provides a backup of the log of the previous session of NVDA; the file is called `nvda-old.log`.
Sometimes however you may want to access older logs, e.g. because you have had to restart NVDA again before looking at `nvda-old.log`.
This add-on allows you to configure if you want to backup old logs and how many of them; this is done in the [add-on's settings](#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs and perform various actions on the selected log:

* open it (press `Enter`)
* delete it (press `Delete`)
* copy the log file (press `control+C`)

You can also select multiple logs to perform an actions on all of them.

To be able to open a log, you should first have configured the [Command to open a file in your favorite editor](#settingsOpenCommand).

## Python console extension

<a id="pythonConsoleOpenCodeFile"></a>
### `openCodeFile` function

In the console, you can call the following function to view the source code that defines the variable `myVar`:  
`openCodeFile(myVar)`  

For this feature to work, you need to have configured your [favorite editor's command](#settingsOpenCommand) in the add-on's settings.
If you are not running NVDA from source, the [location of NVDA source code](#settingsNvdaSourcePath) should also have been configured.

The `openCodeFile` functions can be called on objects defined in NVDA's code or on objects defined by add-ons.
It cannot be called on objects whose source code is not available such as python builtins.

If you have not yet imported the object in the console, you can also pass its name as parameter to the `openCodeFile` function.

Below are examples of call in NVDA's code:

* View the definition of the function `speech.speech.speak`:  
  `openCodeFile(speech.speech.speak)`  
  or with the name passed as parameter:  
  `openCodeFile("speech.speech.speak")`  
* View the definition of the class `TextInfo`:  
  `openCodeFile(textInfos.TextInfo)`  
* View the definition of the method `copyToClipboard` of the class `TextInfo`:  
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* View the definition of the class of the focused object:  
  `openCodeFile(focus)`  
* Open the file `api.py` defining the module `api`:  
  `openCodeFile(api)`  

### Python console startup script

You can define a custom script which will be executed in the Python console's namespace when it is first opened.

For example, the script allows you to execute new imports and define aliases that you will be able to use directly in the console, as shown below:  

    # Various import that I want in the console.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

The Python console script should be placed in the following location: `pathToNVDAConfig\ndtt\consoleStartup.py`  
For example: `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

Note: In Python 2, i.e. with NVDA 2019.2.1 or earlier, only pure ASCII scripts are supported; any other encoding such as Unicode is not supported.

### Preserving Python console input history

In Python console history, you can use up and down arrows to review and modify previous inputs.
Though, the list of previous inputs is cleared when exiting NVDA.
This add-on provide [an option](#settingsPreserveHistory), enabled by default, allowing to preserve Python console input history even when NVDA is restarted.

## Log the stack trace of the speech function

Sometimes, you may want to see which part of the code is responsible for speaking something.
For this, you can enable the stack trace logging of the speech function pressing `NVDA+X, S`.
Each time NVDA speaks, a corresponding stack trace will be logged in the log.

Note: You may modify the script's file directly to patch another function.
See all instructions in the file for details on usage.

<a id="reverseTranslationCommand"></a>
## Reverse translation command

Many testers use NVDA in another language than English.
But when reporting test results on GitHub, the description of the modified options or the messages reported by NVDA should be written in English.
It's quite frustrating and time consuming to have to restart NVDA in English to check the exact wording of the options or messages.

To avoid this, the add-on provides two reverse translation commands allowing to reverse translate NVDA's interface such as messages, control labels in the GUI, etc.

* `NVDA+X, R` uses NVDA's gettext translation to try to reverse translate the last speech.
* `NVDA+shift+X, R` uses gettext translations from NVDA and its add-ons to try to reverse translate the last speech.

More specifically, the first string of the last speech sequence is reverse translated.

For example, in French NVDA, if I arrow down to the Tools menu named "Outils", NVDA will say "Outils  sous-Menu  o" which stands for "Tools  subMenu  o".
If I press the reverse translation command just after that, NVDA will reverse translate "Outils" to "Tools".

Looking at the log afterwards, we can find the following lines:
```
IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]
```
This confirms that "Outils was the first string in the speech sequence.

In case the reverse translation leads to two or more possible results, a context menu is opened listing all the possibilities.

The result of the reverse translation is also copied to the clipboard if the corresponding [option](#settingsCopyReverseTranslation) is enabled, which is the default value.

Reverse translation of NVDA strings is only available for NVDA version 2022.1 or above.
For earlier versions of NVDA, only the add-ons strings are available for reverse translation.

Besides, in NVDA version 2019.2.1 or earlier, in case no reverse translation is found, a second attempt is made in the first part of the string.
 Indeed, in these NVDA version, the speech sequence looks like this:
```
IO - speech.speak (12:39:12.684):
Speaking [u'Outils  sous-Menu  o']
```
We can see that an object label may be concatenated with role, state, shortcut, etc.
So if the reverse translation gives no  result with the whole string, a second attempt is made on the part of the string before the double space ("  ").
Though, this is not bullet-proof since we cannot exclude that a string actually natively contains a double space.

<a id="settings"></a>
## Settings

Some features of the add-on may require a specific configuration.
A settings panel allows to enable them or to control how they work.
To view and modify these settings, go to NVDA menu -> Preferences and select the category NVDA Dev & Test Toolbox.
This settings dialog can also be accessed directly from the Logs Manager dialog.

These settings are global and can only be configured when the default profile is active.

<a id="settingsOpenCommand"></a>
### Command to open a file in your favorite editor

Some features allow to see content in your favorite editor.
This includes the commands to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), as well as the [log manager](#oldLogsBackup)'s Open button.

To use them, you first need to configure the command that will be called to open the file in your favorite editor.
The command should be of the form:  
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
You should of course modify this line according to the real name and location of your editor and the syntax used by it to open files.
`{path}` will be replaced by the full path of the file to open and `{line}` by the line number where you want the cursor to be set.
For Notepad++ for example the command to type in the console would be:  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA source code path

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\pathExample\GIT\nvda\source`  
Of course, replace the path of NVDA source with the correct one.

Be sure however that the version of your source file (e.g. GIT commit) is the same as the one of the running instance of NVDA.

<a id="settingsLogsBackup"></a>
### Backup of old logs

The combobox Backup of old logs allows to enable or disable the [feature](#oldLogsBackup).
If it is enabled, you can also specify below in "Limit the number of backups" the maximum number of backups you want to keep.
These settings only take effect at next NVDA startup when the backup takes place.

<a id="settingsCopyReverseTranslation"></a>
### Copy reverse translation to clipboard

This option allows to choose if the [reverse translation command](#reverseTranslationCommand) also copies its result to the clipboard.

<a id="settingsPreserveHistory"></a>
### Preserve console input history after restart

If this checkbox is checked, Python console input history will be preserved when NVDA is restarted.
If it is checked, you can also specify below the maximum number of inputs that will be saved.
If it is unchecked, NVDA will behave as usual, i.e. the console history will be empty after restart.

## Change log

### Version 8.0

* Python console history can now be preserved accross restarts.
* Reverse translation: Added a second command to reverse translate a string using both NVDA and its add-ons translations.
* New log reader commans to jump to previous or next braille output message
* New log reader commans to jump to previous or next block in a message, e.g. previous or next thread stack in a watchdog freeze report, previous or next block of properties in the developer info for navigator object, etc.
* New log reader commands to jump to the first or last interesting line of a block, e.g. first or last frame of a traceback
* A new log reader "Go to error" command to jump to the error in a traceback frame.
* A new log reader command to display an help message listing all the available commands while reading a log.
* The log reading mode is now enabled by default in the Python console output pane.
* A new command to anonymize a log
* The console startup script now supports unicode strings (for Python 3 only); full unicode file may not be supported though.
* The Python console startup script will now only be executed once and only once when the console opens.
A bug where this script could be executed many times when reloading the add-ons has been fixed.
* Improved error handling in the console startup script.
* Bugfix: An empty log files created when log is disabled do not fail anymore to be saved as old log.
* Speech on demand is now supported in layered commands
* Improved error handling of the script opener command (in case of wrong or missing configuration, or when a braille display is in use).

### Version 7.3

* Bugfix: The command to activate layered commands of the add-on can now be assigned another gesture.

### Version 7.1

* Compatibility with NVDA 2025.1.

### Version 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.  
  The existing commands have been modified accordingly.  
* A new command (`NVDA+X, R`) to reverse translate the last spoken message.
* A new command (`NVDA+X, C`) to open the source code of the script associated to the next pressed gesture.
* Added speech on demand support.
* The log manager now allows more actions, either with the dedicated buttons in the dialogs or using keyboard shortcuts in the list: `enter` to open the log, `control+C` to copy the log file and `delete` to delete a log file.
* The sorting order in the log manager has been reversed (most recent log on top).
* Fixed an issue when trying to open a Python module with openCodeFile function.

### Version 6.3

* Compatibility with NVDA 2024.1.

### Version 6.2

* Restores console opening for NVDA < 2021.1.
* Addresses potential security issues related to [GHSA-xg6w-23rw-39r8][5] when using the add-on with older versions of NVDA. However, it is recommended to use NVDA 2023.3.3 or higher.

### Version 6.1

* Opening the source file of an object located in the submodule of a package is now working.
* Bugfix: The enhanced exit dialog can now be reopened and used as expected after having been closed. (contribution from Łukasz Golonka)

### Version 6.0

* While using object navigation commands, a specific object property can be reported instead of NVDA usual object reporting.
* In log reading mode, the "C" key to open a code file from the log now also works on an input help message.
* Bugfix: The add-on can now start successfully when the number of logs to save is set to its maximum value.
* Bugfix: Python console startup script's output does not prevent anymore to jump to the first result in the console when using result navigation commands.
* Note: From now on, localization updates will not appear anymore in the change log.

### Version 5.0

* If Instant Translate add-on is installed, it is now possible to have speech messages translated on the fly when using log reading commands.
* While in log reading mode, pressing E or shift+E now jumps to CRITICAL erorr messages as well as normal ERROR messages.
* New log quick navigation commands have been added to jump to input and to speech messages.
* A new command allow to place a marker in the log; and specific quick navigation commands in log reading mode allow to jump to them.  
  Credit: the initial idea for this feature comes from Debug Helper add-on by Luke Davis.  
* Bubfix: The memorization of the last error do not fail anymore in some cases.
* Bugfix: The add-on can initialize again with NVDA 2019.2.1.
* Bugfix: Log saving feature will not fail anymore with non-ASCII logs.

### Version 4.2

* Fixed an error with NVDA version below 2021.3.
* Fixed the stack trace log formatting.
* First localizations.

### Version 4.1

* Fixed a bug occurring in some situations while logging an error.
* The add-on's settings can now be modified only when the default profile is active to avoid config issues.

### Version 4.0

* Possibility to back up old logs and introduction of a logs manager.
* Added a script to report the last logged error.
* Fixed a bug preventing last log message to be read in older NVDA versions.

### Version 3.2

* Compatibility with NVDA 2023.1.

### Version 3.1

* Fixed an error occurring when requesting unavailable information on an object.

### Version 3.0

* In a log, you can now press C on a message's header line to open the function/module which has emitted it.
* In the console, `openCodeFile` function can now receive as parameter the object or a string containing its name.
* New feature: NVDA console startup file: If it exists, the file YourNVDAConfigFolder\ndtt\consoleStartup.py will be executed when NVDA console is first opened or when add-ons are reloaded.
* Various minor fixes for `openCodeFile` Python console's function and the command to open the source file corresponding to a line in the log.
* Fixed an issue when trying to report roles/states for object explorer in older version of NVDA.
* The add-on does not cause a problem anymore with the tree interceptor when using UIA in Edge.

### Version 2.1

* Various bugfixes and code refactoring/cleaning to address all use cases: all supported versions, installed vs. run from source, etc. (contribution from Łukasz Golonka)
* Rewriting of the compa module (contribution from Łukasz Golonka)
* The restart dialog can now be opened only once.
* The object explorer shortcuts are now unassigned by default and need to be mapped by the user.
* With the object explorer, a double-press to call the script to report the current object's property now displays the reported information in a browseable message.

### Version 2.0

* New feature: Enhanced restart dialog to specify some extra options when restarting NVDA.
* New feature: extended description mode.
* Play error sound feature harmonized between pre and post 2021.3 versions of NVDA.
* New feature: Log reader commands are now available in the log viewer and also optionally in edit fields or webpages.
* New feature: In the Python console, an `openCodeFile` function is available to view the source code of an object.
* Some features are now disabled in secure mode for security reasons.
* The add-on's compatibility range has been extended (from 2019.2 to 2021.1).
* Releases are now performed with GitHub action instead of appVeyor.

### Version 1.0

* Initial release.

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]: https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
