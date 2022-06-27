# NVDA Dev & Test Toolbox

* Author: Cyrille Bougot
* NVDA compatibility: 2019.2 and beyond
* Download [stable version][1]

This add-on gathers various features for NVDA debugging and testing.

## Features

* An enhanced restart dialog to specify some extra options when restarting NVDA.
* A toggle script and a backport of NVDA's "Play a sound for logged errors" feature.
* An object property explorer.
* An extended script description mode: when enabled input help mode report information on scripts that have no description.
* Commands to help log reading and analyzing.
* In the Python console workspace, a function to open the source code of an object.
* A command to log the stack trace of the speech.speak function.

## Enhanced restart dialog

The NVDA+shift+Q command opens a dialog to specify some extra options before restarting NVDA.
The options that can be specified correspond to the [command line options][2] that can be used with `nvda.exe`, e.g. `-c` for config path, `--disable-addons` to disable add-ons, etc.

## Play a sound for logged errors

The ["Play a sound for logged errors" setting][4] has been introduced in NVDA 2021.3 and allows to specify if NVDA will play an error sound in case an error is logged.

This add-on provides an additional command (NVDA+control+alt+E) to toggle this setting.
You can choose:

* "Only in test versions" (default) to make NVDA play error sounds only if the current NVDA version is a test version (alpha, beta or run from source).
* "Yes" to enable error sounds whatever your current NVDA version is. 

For NVDA prior to 2021.3, this add-on provides the backport of this feature and the possibility to control it with the keyboard command.
The checkbox in the Advanced settings panel is not backported however.

## Object property explorer

This feature allows to report some properties of the current navigator object without opening the log viewer.

To list the properties of an object, move the navigator object to it and use the following commands:

* Selects the previous property and reports it for the navigator object.
* Selects the next property and reports it for the navigator object.
* Reports the currently selected property for the navigator object; two presses displays this information in a browseable message.

These three commands are unassigned by default; you will have to assign them in the Input gesture dialog to use them.

The list of the supported properties is the following:
name, role, state, value, windowClassName, windowControlID, windowHandle, location, Python class, Python class mro.

This feature is an improvement of an example in [NVDA developer guide][5].


## Extended script description mode

When the Extended script description mode is active, the input help mode (NVDA+1) is modified as follows.
If a script has no description, the script's name and class are reported.
If a script has a description, its description is reported as usual.
The gesture to activate or deactivate this feature is NVDA+control+alt+D.

Executing a gesture bound to a script without description in input help mode also create an entry for this script in the gesture management dialog.
This entry is located in a dedicated category called "Scripts without description (modify at your own risk!)".
This allow to easily add, delete or change the native NVDA gestures for these script.
Be aware however that it is often intended that such script do not have any description to prevent the user to modify the associated gesture.
Indeed, the gesture may be defined to match an application shortcut key.
For example the script script_toggleItalic on NVDAObjects.window.winword.WordDocument is bound to control+I and this should not be modified since the gesture is passed to the application to actually execute the shortcut key.

### Usage example

Control+shift+I also toggle italic in Word, even if it is not natively reported by NVDA.
To have the control+shift+I result reported by NVDA as control+I, you should perform the following steps:

* Open a Word document.
* Enable the extended script description mode with NVDA+control+alt+D.
* Enter input help mode with NVDA+1.
* Press control+I to report the italic script and have it added in the gesture dialog.
* Exit input help mode with NVDA+1.
* Open the input gestures dialog.
* In the category "Scripts without description (modify at your own risk!)", select the command "toggleItalic on NVDAObjects.window.winword.WordDocument".
* Add the control+shift+I shortcut and validate.
* If you want, exit the extended script description mode with NVDA+control+alt+D.

Known bug: A script added for a specific class is visible even if gesture manager is opened in another context.

## Log reading and analyzing commands

A log reader mode provides commands to ease log reading and analyzing.
In the log viewer window the log reader is enabled by default, thus log reading commands are available immediately.
In another text reading area such as an editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press NVDA+control+alt+L to enable log reader mode and use its commands.
When you are done with log reading and analyzing tasks, you can disable again NVDA+control+alt+L to disable the log reader mode.

The commands available in log reader mode are described hereafter.

### Quick navigation commands

Single letter command similar to browse mode quick navigation keys allow to move to various type of log messages:
* m: any message
* e: ERROR
* i: IO
* d: DEBUG
* f: INFO
* g: DEBUGWARNING
* w: WARNING

Pressing the single letter moves to the next occurrence of this message. Combining the letter with the shift key moves to the previous occurrence of this message.

### Opening a file in your editor

When looking at a traceback, you may want to open one of the source files to understand the cause and the context of the issue.
Press C to open the source code file corresponding to the current line of the traceback.

For this feature to work, you need to have configured your favorite editor's command.
If you are not running NVDA from source, the location of NVDA source code also should have been configured.
For more details regarding the configuration, please see the paragraph NVDA Debug & Test Tools configuration.

## Python console extension

In the console, you can call the following function to view the source code that defines the variable `myVar`:  
`openCodeFile(myVar)`

For this feature to work, you need to have configured your favorite editor's command.
If you are not running NVDA from source, the location of NVDA source code also should have been configured.
For more details regarding the configuration, please see the paragraph NVDA Debug & Test Tools configuration.

The `openCodeFile` functions can be called on objects defined in NVDA's code or on objects defined by add-ons.
It cannot be called on objects whose source code is not available such as python builtins.

Below are examples of call in NVDA's code:

* View the definition of the function `speech.speech.speak`:  
  `openCodeFile(speech.speech.speak)`
* View the definition of the class `TextInfo`:  
  `openCodeFile(textInfos.TextInfo)`
* View the definition of the method `copyToClipboard` of the class `TextInfo`:  
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`
* View the class definition of the focused object:  
  `openCodeFile(focus)`
* Open the file `api.py` defining the module `api`:  
  `openCodeFile(api)`

## Log the stack trace of the speech function

Sometimes, you may want to see which part of the code is responsible for speaking something.
For this, you can enable the stack trace logging of the speech function pressing NVDA+control+alt+S.
Each time NVDA speaks, a corresponding stack trace will be logged in the log.

Note: You may modify the script's file directly to patch another function.
See all instructions in the file for details on usage.

## NVDA Debug & Test Tools configuration

The log reader commands and the python console extension feature may require a specific configuration.
To use functions that allow to view source code in your editor, you should first configure your editor's command line.
If NVDA's file need to be viewed and if you are not running from source, you also need to configure NVDA's source code path.

### Editor's command line configuration

To use the 'open source code' command or the `openCodeFile` console command, you need first to configure the command that will be called to open the file in your favorite editor.
For this, open the NVDA console (NVDA+control+Z) and type the following line and then Enter:
`config.conf['ndtt']['sourceFileOpener'] = r'"C:\path\to\my\editor\editor.exe" "{path}":{line}'`
You should of course modify this line according to the real name and location of your editor and the syntax used by it to open files.
`{path}` will be replaced by the full path of the file to open and `{line}` by the line number where you want the cursor to be set.
For Notepad++ for example the command to type in the console would be:
`config.conf['ndtt']['sourceFileOpener'] = r'"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}'`

### NVDA source code path configuration

When a file belonging to NVDA's core is listed in the traceback, the line is of the following form:
`File "config\profileUpgrader.pyc", line 30, in upgrade`

If you are not running NVDA from source, you may specify an alternate location where the source file will be found, e.g. the place where you have cloned NVDA source files.
In this case, you have to configure the path where you have NVDA source files located.

For this, open the NVDA console (NVDA+control+Z) and type the following line and then Enter:
`config.conf['ndtt']['nvdaSourcePath'] = r'C:\pathExample\GIT\nvda\source'`
Of course, replace the path of NVDA source with the correct one.

Be sure however that the version of your source file (e.g. GIT commit) is the same as the one of the running instance of NVDA.


## Change log

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

[1]: https://addons.nvda-project.org/files/get.php?file=ndtt

[2]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[4]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]: https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#toc22
