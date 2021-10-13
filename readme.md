# NVDA Dev & Test Toolbox

* Author: Cyrille Bougot
* NVDA compatibility: 2018.3 and beyond
* Download [stable version][1]

This add-on gathers various features for NVDA debugging and testing.

## Features

* Manage play error sound in stable versions
* Get script info in input help mode.
* Commands to help log reading and analyzing.
* Provide a window to specify option when restarting NVDA.
* Log stack trace for a function.
* Python console extension
* Get object's information

## Play a sound for logged errors

This feature provides a toggle command (NVDA+control+alt+E) to specify if NVDA will play an error sound in case an error is logged.
You can choose:
* "Only in test versions" (default) to make NVDA play error sounds only if the current NVDA version is a test version (alpha, beta or run from source).
* "Yes" to enable error sounds whatever your current NVDA version is. 


Please note the following points regarding the version of NVDA you are using:
* For NVDA 2021.3 onwards, this feature has been integrated in NVDA's core and it can be configured in the Advanced settings panel. But this extension add the possibility to control it with the keyboard command.
* For NVDA prior to 2021.3, this extension provides the backport of this feature and the possibility to control it with the keyboard command. The checkbox in the Advanced settings panel is not backported however.

## Script information in input help mode

This feature allow to get information on any script in input help mode (NVDA+1).
If the executed script has no description, the script's name and location/class are announced instead.
The gesture to activate or deactivate this feature is NVDA+control+alt+H.

Executing a gesture bound to a script without description in input help mode also create an entry for this script in the gesture management dialog.
This entry is located in a dedicated category called "Scripts without description (modify at your own risk!)".
This allow to easily add, delete or change the native NVDA gestures for these script.
Be aware however that it is often intended that such script do not have any description to prevent the user to modify the associated gesture.
Indeed, the gesture may be defined to match an application shortcut key.
For example the script script_toggleItalic on NVDAObjects.window.winword.WordDocument is bound to control+I and this should not be modified since the gesture is passed to the application to actually execute the shortcut key. But control+shift+I also toggle italic in Word, even if it is not natively reported by NVDA. To have the control+shift+I result reported by NVDA as control+I, you should perform the following steps:

* Open a Word document.
* Enable the debug help mode with NVDA+control+alt+H.
* Enter help mode with NVDA+1.
* Press control+I to report the italic script and have it added in the gesture dialog.
* Exit help mode with NVDA+1.
* Open the input gestures dialog.
* In the category 'niveau 0  Scripts without description (modify at your own risk!)', select the command 'toggleItalic on NVDAObjects.window.winword.WordDocument'.
* Add the control+shift+I shortcut and validate.
* If you want, exit the debug help mode with NVDA+control+alt+H.

Known bug: A script added for a specific class is visible even if gesture manager is opened in another context.

## Log reader

The log reader provides commands to ease log reading and analyzing. In the log viewer window the log reading commands are available immediately. In another text reading area such as an editor (e.g. Notepat++) or a webpage (e.g. GitHub issue), you need to press NVDA+control+alt+L to enable log reader commands.

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
For this feature to work, you need to have configured your favorite editor's command, as well as the location of NVDA source code in case you are not running NVDA from source.

## Python console extension

In the console, you can call the following command to view the source code that defines the variable `myVar`:  
`openCodeFile(myVar)`

For this feature to work, you need to have configured your favorite editor's command, as well as the location of NVDA source code in case you are not running NVDA from source.

The `openCodeFile` functions can be called on objects defined in NVDA's code or on objects defined by add-ons. It cannot be called on objects whose source code is not avaiable such as python builtins.

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

## Specify some options when restarting NVDA

The NVDA+shift+Q command allows to display a window to specify some options before restarting NVDA.
The options that can be specified correspond to the [command line options](https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions) that can be used with `nvda.exe`, e.g. `-c` for config path, `--disable-addons` to disable add-ons, etc.

## Log stack trace for a function

This feature allows to enable the stack trace logging of the speech function when pressing NVDA+control+alt+S. You may modify the script's file directly to patch another function.
See all instructions in the file for details on usage.

## Object's information

This feature allows to get various information on the current navigator object or associated window.

Usage:

* NVDA+LeftArrow : Announce the navigator object's currently selected property.
* NVDA+Shift+LeftArrow or NVDA+Shift+RightArrow: select previous or next property and announce it for the navigator object.

The list of supported properties is the following:
name, role, state, value, windowClassName, windowControlID, windowHandle, location, pythonClass, pythonClassMRO

This feature is an improvement of [NVDA developer guide][2] example 3

If you have installed [Speech history review and copying][3]  addon from Tyler Spivey and James Scholes, you may use it to copy and paste the announced property to review it;
review via copy/paste is especially useful for pythonClassMRO since it may be long.

## NVDA Debug & Test Tools configuration

The log reader and the python console extension feature may require a specific configuration.
To use functions that allow to view source code in your editor, you should first configure your editor's command.
If NVDA's file need to be viewed and if you are not running from source, you also need to configure NVDA's source code path.

### Editor's command configuration

To use the 'open source code' command or the `openCodeFile` console command, you need first to configure the command that will be called to open the file in your favorite editor.
For this, open the NVDA console (NVDA+control+Z) and type the following line and then Enter:
`config.conf['ndtt']['sourceFileOpener'] = r'"C:\path\to\my\editor\editor.exe" "{path}":{line}'`
You should of course modify this line according to the real name and location of your editor and the syntax used by it to open files.
`{path}` will be replaced by the full path of the file to open and `{line}` by the line number where you want the cursor to be set.
For Notepad++ for example the command to type in the console would be:
`config.conf['ndtt']['sourceFileOpener'] = r'"C:\Program Files\Notepad++\notepad++.exe" {path} -n{line}'`

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

### Version 1.0

* Initial release.

[1]: https://addons.nvda-project.org/files/get.php?file=ndtt

[3]: https://addons.nvda-project.org/addons/speech_history.en.html

[4]: https://github.com/CyrilleB79/startupOptionWorkaround
