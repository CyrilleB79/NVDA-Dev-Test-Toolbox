# NVDA Dev & Test Toolbox

* Author: Cyrille Bougot
* NVDA compatibility: 2018.3 and beyond
* Download [stable version][1]

This add-on gathers various features for NVDA debugging and testing.

## Features

* Manage beep on error / play error sound in stable versions
* Get script info in input help mode.
* Log stack trace for a function.
* Get object's information

## Beep on error

This feature allows NVDA to beep on error even in NVDA non-test versions.
To activate or de-activate beep error feature, press NVDA+control+alt+B.
With NVDA 2021.2 and below, the beep on error is enabled by default and is not saved to NVDA's configuration.
With NVDA 2021.3 and above, NVDA+control+alt+B toggles the 'Play a sound for logged errors' parameter in advanced settings. It can be saved in NVDA's configuration.


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

## Change log

### Version 1.0

* Initial release.

[1]: https://addons.nvda-project.org/files/get.php?file=ndtt

[3]: https://addons.nvda-project.org/addons/speech_history.en.html

[4]: https://github.com/CyrilleB79/startupOptionWorkaround
