# Набір інструментів для розробки та тестування NVDA (NVDA Dev & Test Toolbox)

* Автор: Cyrille Bougot
* Сумісність із NVDA: 2019.2 та наступні

NVDA Dev & Test Toolbox надає інструменти для налагодження та тестування NVDA.
Засоби роботи з журналом спрощують навігацію та аналіз записів, перегляд помилок і трасувань (tracebacks), збереження резервних копій журналу та його анонімізацію перед поширенням.
Також у журнал можна записувати виклики конкретних функцій та маркери.
Крім того, передбачено відкриття відповідного вихідного коду безпосередньо із записів журналу, змінних консолі чи навіть за допомогою команди жестом.
Додаток також розширює можливості консолі Python і надає такі утиліти, як зворотний переклад рядків інтерфейсу NVDA та вдосконалений діалог перезапуску.

## Функції

* Вдосконалений діалог виходу з NVDA для вибору додаткових параметрів під час перезапуску NVDA.
* Різноманітні функції, пов'язані із зафіксованими в журналі помилками.
* Оглядач властивостей об'єктів.
* Інструменти для роботи зі скриптами та вихідним кодом: розширений режим опису скриптів і команди відкриття вихідного коду.
* Команди для спрощення читання та аналізу журналу.
* Резервні копії старих журналів
* Команда для анонімізації журналу
* Покращення консолі Python, такі як власний стартовий скрипт і можливість зберігати історію вводу в пам'яті після перезапуску NVDA.
* Функція відкриття вихідного коду об'єкта в робочому просторі консолі Python.
* Команда для запису в журнал викликів певної функції (наприклад, `speech.speech.speak`), включно з її трасуванням стека.
* Команда для зворотного перекладу елементів інтерфейсу.

## Команди

Це доповнення використовує багатошарові команди для всіх нових команд, які воно додає.
Точкою входу для цих команд є `NVDA+Z`; тому всі команди повинні виконуватися за допомогою `NVDA+Z`, а потім ще однієї літери або жесту.
За потреби ви можете змінити його в діалоговому вікні Жести вводу.

У решті цієї документації ми називатимемо цей жест `Жест NDTT`.
Наприклад, `Жест NDTT, S` означає `NVDA+Z, S`, якщо ви не змінили жест за замовчуванням.

Ви можете переглянути список усіх доступних багатошарових команд, натиснувши `Жест NDTT, H`.

Для команд, які ви використовуєте частіше, ви також можете визначити прямий жест у діалоговому вікні жестів вводу.

## Покращений діалог перезапуску

Команда `Жест NDTT, Q` відкриває діалог для налаштування додаткових параметрів перед перезапуском NVDA.
Параметри, які можна вказати, відповідають [параметрам командного рядка][2], що використовуються з `nvda.exe`, наприклад: `-c` для шляху до конфігурації, `--disable-addons` для вимкнення додатків тощо.

## Функції, пов'язані із зафіксованими в журналі помилками

### Повідомити про останню зафіксовану помилку

Натискання `Жест NDTT, E` дозволяє повідомити про останню зафіксовану помилку без потреби відкривати журнал.
Повторне натискання очищає запам'ятовану останню помилку.

### Відтворювати звук під час журналювання помилок

[Параметр «Відтворювати звук під час журналювання помилок»][4] з'явився в NVDA 2021.3 і дозволяє вказати, чи має NVDA відтворювати звук помилки, коли вона фіксується в журналі.

Цей додаток надає додаткову команду (`Жест NDTT, Shift+E`) для перемикання цього параметра.
Ви можете обрати:

* «Тільки в тестових версіях» (за замовчуванням), щоб NVDA відтворювала звуки помилок, лише якщо поточна версія NVDA є тестовою (alpha, beta або запуск із вихідного коду).
* «Так», щоб увімкнути звуки помилок незалежно від поточної версії NVDA.
* «Ні», щоб вимкнути звуки помилок незалежно від поточної версії NVDA (доступно лише у свіжих версіях NVDA).

Для версій NVDA старіших за 2021.3 цей додаток забезпечує зворотне портування (backport) цієї функції та можливість керувати нею за допомогою комбінації клавіш.
Проте комбінований список на панелі «Додаткові налаштування» не портується.
Можливість вимкнути звуки помилок для будь-якої версії NVDA також не портується для версій, раніших за 2026.2.

## Дослідник властивостей об’єктів

Ця функція дозволяє повідомляти про деякі властивості поточного об’єкта навігатора, не відкриваючи переглядач журналу.

Щоб отримати список властивостей об’єкта, перемістіть до нього об’єктний навігатор і скористайтеся такими командами:

* `Жест NDTT, Стрілка вгору`: вибирає попередню властивість і повідомляє її значення для об'єкта навігатора.
* `Жест NDTT, Стрілка вниз`: вибирає наступну властивість і повідомляє її значення для об'єкта навігатора.
* `Жест NDTT, N`: повідомляє значення поточної вибраної властивості для об'єкта навігатора
* `Жест NDTT, Shift+N`: відображає поточну вибрану властивість для об'єкта навігатора у вікні перегляду

Список підтримуваних властивостей:
name, role, state, value, windowClassName, windowControlID, windowHandle, location, Python class, Python class mro.

Під час використання команд навігації об'єктами ви також можете налаштувати озвучення поточної вибраної властивості замість звичайного повідомлення інформації про об'єкт у NVDA.
Команда-перемикач `Жест NDTT, Control+N` дозволяє перемикатися між цим користувацьким повідомленням об'єктів і звичайним звітуванням NVDA.

Наприклад, ви можете вибрати властивість «windowClassName» та ввімкнути користувацьке повідомлення об'єктів.
Тоді під час переміщення об'єкта навігатора до наступного чи попереднього об'єкта ви чутимете windowClassName цього об'єкта замість звичайної інформації.

## Інструменти для роботи зі скриптами та вихідним кодом

<a id="sourceCodeOpeningCommands"></a>
### Команди відкриття вихідного коду

Додаток надає три команди, що дозволяють відкривати вихідний код.

Перша команда дозволяє відкрити вихідний код скрипта за його жестом.
Щоб скористатися нею, натисніть `Жест NDTT, C`, а потім — жест скрипта, код якого ви хочете переглянути.
Наприклад, щоб переглянути код скрипта, котрий повідомляє заголовок вікна переднього плану, натисніть `Жест NDTT, C`, а потім `NVDA+T`.

Дві інші команди дозволяють відкрити вихідний код за його шляхом:

* `Жест NDTT, Shift+C` відкриває вихідний код, шлях до якого розташований під системним курсором.
* Жест NDTT, Control+C відкриває вихідний код, шлях до якого розташований під курсором перегляду.

E.g. if the caret or the review cursor is located on the following line, the command will open the corresponding file in your editor:
`C:\Users\username\AppData\Roaming\nvda\addons\addonName\globalPlugins\addonName\__init__.py:48`

Щоб користуватися цими командами, потрібно попередньо налаштувати [команду вашого улюбленого редактора](#settingsOpenCommand) у параметрах додатка.
Якщо ви запускаєте NVDA не з вихідного коду, також має бути налаштований [шлях до вихідного коду NVDA](#settingsNvdaSourcePath).

### Режим розширеного опису скриптів

Режим розширеного опису скриптів дозволяє отримувати інформацію про скрипти без опису в режимі довідки введення.

Коли режим розширеного опису скриптів активний, режим довідки введення (NVDA+1) змінюється так.
Якщо скрипт не має опису, повідомляються його назва та клас.
Якщо скрипт має опис, він озвучується як зазвичай.
Жест для ввімкнення або вимкнення цієї функції — `Жест NDTT, D`.

Виконання в режимі довідки введення жесту, прив'язаного до скрипта без опису, також створює запис для цього скрипта в діалозі керування жестами.
- Цей запис розташовується у спеціальній категорії під назвою «Скрипти без опису (змінюйте на свій страх і ризик!)».
Це дозволяє легко додавати, видаляти або змінювати стандартні жести NVDA для таких скриптів.
Проте майте на увазі, що відсутність опису часто передбачена навмисно, щоб користувач не міг змінити пов'язаний жест.
Справді, цей жест може бути визначений відповідно до гарячої клавіші програми.
Наприклад, скрипт script_toggleItalic на NVDAObjects.window.winword.WordDocument прив'язаний до Control+I, і його не слід змінювати, оскільки жест передається до самої програми для фактичного виконання комбінації клавіш.

#### Приклад використання

Натискання `Control+Shift+I` також вмикає або вимикає курсив у Word, навіть якщо NVDA типово про це не повідомляє.
Щоб результат натискання `Control+Shift+I` озвучувався в NVDA так само, як і `Control+I`, виконайте такі кроки:

* Відкрийте документ Word.
* Увімкніть режим розширеного опису скриптів за допомогою `Жест NDTT, D`.
* Увійдіть у режим довідки введення за допомогою `NVDA+1`.
* Натисніть `Control+I`, щоб озвучити скрипт курсиву й додати його до діалогу жестів.
* Вийдіть із режиму довідки введення за допомогою `NVDA+1`.
* Відкрийте діалог жестів вводу.
* У категорії «Скрипти без опису (змінюйте на свій страх і ризик!)» виберіть команду «toggleItalic on NVDAObjects.window.winword.WordDocument».
* Додайте комбінацію клавіш `Control+Shift+I` та підтвердьте зміни.
* За бажанням вимкніть режим розширеного опису скриптів за допомогою `Жест NDTT, D`.

Відома помилка: скрипт, доданий для певного класу, залишається видимим навіть тоді, коли менеджер жестів відкрито в іншому контексті.

## Log reading and analyzing features

<a id="logPlaceMarkers"></a>
### Place markers in the log

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press `NDTTGesture, K`.
A message as follows will be logged at INFO level:
`-- NDTT marker 0 --`

You can add as many markers as you want in the log.
The marker's number will be incremented each time you place a marker in the log; it will only be reset when NVDA is restarted.

### Log reader mode

A log reader mode provides commands to ease log reading and analyzing.
In the log viewer window and in the Pyton console output area, the log reader is enabled by default, thus log reading commands are available immediately.
In another text reading area such as an editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press `NDTTGesture, L` to enable log reader mode and use its commands.
When you are done with log reading and analyzing tasks, you can disable again `NDTTGesture, L` to disable the log reader mode.

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

Pressing the single letter moves to the next occurrence of this message.
Combining the letter with the shift key moves to the previous occurrence of this message.

In addition, inside certain types of messages, you can jump block by block pressing `O` or `shift+O`.
The following message types and associated blocks are supported:

* In messages containing tracebacks, e.g. error messages, block navigation allows you to jump between tracebacks
  <target/>
* In the message listing the stacks for Python threads logged when a freeze occurs, block navigation allows you to jump between thread stacks.
* In the message providing developer info for the navigator object logged when you press `NVDA+F1`, block navigation allows you to jump between groups of properties.
  <target/>

At last, inside a block, you may want to jump quickly to first or last line of interest of the block.
Use `shift+L` to jump to the first line of interest of the current block's content, e.g. the first frame of a traceback.
And `L` to jump to the last line of interest of the block's content, e.g. last frame of a thread stack or error below a traceback.

#### Translation of speech message

Sometimes, you may have to look at a log taken on a system in a foreignh language that you do not understand.
E.g. the log was taken on a Chinese system / NVDA, whereas you only understand French.
If you have [Instant Translate][3] add-on installed, you may use it in conjonction with [quick log navigation commands](#logReaderQuickNavigationCommands) to have speech messages translated.

* First configure Instant Translate's languages.
  <target/>
  <target/>
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

To use this feature, you need to have configured your [favorite editor's command](#settingsOpenCommand) in the add-on's settings.
If you are not running NVDA from source, the [location of NVDA source code](#settingsNvdaSourcePath) should also have been configured.

#### Analysing a traceback

Sometimes you may have error tracebacks in the log, as in the following example:

    <target/>
error executing script: <bound method LogContainer.script_openSourceFile of <NVDAObjects.Dynamic_LogViewerLogContainerIAccessibleRichEdit50WindowNVDAObject object at 0x34C1E510>> with gesture 'c'
    <target/>
      <target/>
      <target/>
        <target/>
           <target/>
      <target/>
        <target/>
        <target/>
    <target/>

For frames where the source code is available, you may have noticed markers with `^` (caret) and `~` (tilde) characters.
That's the way Python visually indicates the error's location as well as its context in a traceback frame.
Pressing `control+E` moves the cursor at the beginning of the error in the source code line, i.e. the text marked by `^` (caret) character.
A double press select this text.
A triple press selects the error with its context, i.e. the text of the source code line marked by `^` (caret) and `~` (tilde) characters.

Please note that for logs taken with an NVDA version before 2024.1, thus with Python 3.7 or older, Python only indicates the error with one `^` (caret) character.
Thus the double or triple press actions of this command becomes rather useless.

#### Getting a summary of the available commands

To display a list of all the available commands in log reading mode, press `control+H`.

## Anonymize a log

When reporting issues, you may have to provide a log.
However, logs may contain sensitive information (user names, e-mails, etc.).
This add-on provides a command to anonymize a log's content.

Select a part of the log or its whole content and press `NDTTGesture, A`.
The anonymized log content will be put in the clipboard.
You can paste it on the current selection to replace it or anywhere else you wish.

To use this feature, you need to customize the anonymization rules used by this command.
The file to configure these rules is located at: `pathToNVDAConfig\ndtt\anonymizationRules.dic` (e.g. `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\anonymizationRules.dic`).
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

    <target/>
    <target/>
    <target/>
    <target/>
    <target/>
    <target/>

The Python console script should be placed in the following location: `pathToNVDAConfig\ndtt\consoleStartup.py`
For example: `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

Note: In Python 2, i.e. with NVDA 2019.2.1 or earlier, only pure ASCII scripts are supported; any other encoding such as Unicode is not supported.

### Preserving Python console input history

In Python console history, you can use up and down arrows to review and modify previous inputs.
Though, the list of previous inputs is cleared when exiting NVDA.
This add-on provide [an option](#settingsPreserveHistory), enabled by default, allowing to preserve Python console input history even when NVDA is restarted.

<a id="loggingFunctionCall"></a>
## Logging function calls

Sometimes, you may want to see which part of the code is responsible for speaking something.
For this, you can enable the function calls logging for the `speech.speech.speak` function pressing `NDTTGesture, S`.
Each time NVDA speaks, a corresponding message will be logged, including the stack trace, allowing you to identify the code that has caused this speech output.
Once you are done, disable function calls logging with the same gesture.

The same way, you can choose to log the calls of output functions `tones.beep`, `braille.BrailleBuffer.update` or `nvwave.playWaveFile` to track the origin of a beep, braille output or a sound (e.g. spelling error sound).
The [target function](#targetFunctionForCallLogSetting) can be chosen in the add-on's parameters.
You can even log the calls stack of a custom function.

By default, the log of the function calls is performed using the "settrace" method: it uses `sys.settrace`, `threading.settrace` and/or `threading.settrace_all_threads` to install a tracing callback that is invoked on target function return event.
Alternatively, if you do not get satisfying results, you may opt for the "monkey patching" method where the target function (e.g. `speech.speech.speak`) is patched.
Both methods have limitations that may prevent function calls to be logged in specific combined conditions.
For example, the "settrace" method may not work with NVDA version lower than 2026.1, when the target function is run from a non-main thread and the function calls logging is enabled after the target function's thread has been started.
On the other hand, the "monkey patching" method may not work when the target function is imported through a "from import" statement (e.g. `from tones import beep`).

You can toggle the method used to log function calls in [the dedicated setting](#functionCallLogMethodSetting) or pressing `NDTTGesture, shift+S`.

<a id="reverseTranslationCommand"></a>
## Reverse translation command

Many testers use NVDA in another language than English.
But when reporting test results on GitHub, the description of the modified options or the messages reported by NVDA should be written in English.
It's quite frustrating and time consuming to have to restart NVDA in English to check the exact wording of the options or messages.

To avoid this, the add-on provides two reverse translation commands allowing to reverse translate NVDA's interface such as messages, control labels in the GUI, etc.

* `NDTTGesture, R` uses NVDA's gettext translation to try to reverse translate the last speech.
* `NDTTGesture, shift+R` uses gettext translations from NVDA and its add-ons to try to reverse translate the last speech.

More specifically, the first string of the last speech sequence is reverse translated.

For example, in French NVDA, if I arrow down to the Tools menu named "Outils", NVDA will say "Outils  sous-Menu  o" which stands for "Tools  subMenu  o".
If I press the reverse translation command just after that, NVDA will reverse translate "Outils" to "Tools".

Looking at the log afterwards, we can find the following lines:

    <target/>
    <target/>

This confirms that "Outils was the first string in the speech sequence.

In case the reverse translation leads to two or more possible results, a context menu is opened listing all the possibilities.

The result of the reverse translation is also copied to the clipboard if the corresponding [option](#settingsCopyReverseTranslation) is enabled, which is the default value.

Reverse translation of NVDA strings is only available for NVDA version 2022.1 or above.
For earlier versions of NVDA, only the add-ons strings are available for reverse translation.

Besides, in NVDA version 2019.2.1 or earlier, in case no reverse translation is found, a second attempt is made in the first part of the string.
Indeed, in these NVDA version, the speech sequence looks like this:

    <target/>
    <target/>

We can see that an object label may be concatenated with role, state, shortcut, etc.
So if the reverse translation gives no result with the whole string, a second attempt is made on the part of the string before the double space ("  ").
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
This includes the commands to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#sourceCodeOpeningCommands), as well as the [log manager](#oldLogsBackup)'s Open button.

To use them, you first need to configure the command that will be called to open the file in your favorite editor.
The command should be of the form:
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`
You should of course modify this line according to the real name and location of your editor and the syntax used by it to open files.
`{path}` will be replaced by the full path of the file to open and `{line}` by the line number where you want the cursor to be set.
For Notepad++ for example the command to type in the console would be:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA source code path

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture or a path](#sourceCodeOpeningCommands), the file may belong to NVDA itself.
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

<a id="targetFunctionForCallLogSetting"></a>
### Target function for function call logging

This combobox defines the function whose calls will be logged when enabling [function call logging](#loggingFunctionCall).
You can select the function among various output functions or opt for the custom function choice.

If you select the custom function choice, you will need to enter the complete name of the function you want log calls for.
This complete name should include its location (package, module, class, etc.).
Be careful to define the function with its original location, i.e. where it was actually defined, else, call logging is less likely to work.
For example, use `speech.speech.getCurrentLanguage` which targets the function defined in `speech\speech.py`, not `speech.getCurrentLanguage` witch target the symbol imported in `speech\__init__.py`.

<a id="functionCallLogMethodSetting"></a>
### Function call log method

This combobox defines the method used to identify function calls when [function call logging](#loggingFunctionCall) is enabled.
This parameter can also be toggled pressing `NDTTGesture, shift+S`.
When this method is modified, it will first apply the next time the function call log is activated; that is, it does not apply to current function call logging if currently enabled.

## Change log

### Version 10.1

* The commands entry point gesture has been changed to `NVDA+Z` to avoid conflict with new repeat last speech command.
* The command to cycle "Play a sound for logged errors" has been updated to support the "No" value introduced in NVDA 2026.2.

### Version 10.0

* Log reader: when logging function calls, arguments and return values are now logged too. (with the contribution of hwf1324)
* Log reader: when using navigation commands, some messages are no longer reported as truncated or empty.
* When reporting last error, some messages are no longer reported uninterpolated (e.g. containing "%s").
* Fixed some errors with NVDA 2019.2: first usage of Python console history, reporting of non-ASCII object names with Object property explorer.
* Compatibility with NVDA 2026.1.

### Version 9.0

* A new command to open a code file when the caret is on a file path/line has been added.
* Function calls logging (previously known as stack logging) has been improved offering the possibility to log the call of any function and providing a more reliable method to identify function calls.
* Fixed a security issue with the log reader ([GHSA-39pg-6xpm-mjgf](https://github.com/CyrilleB79/NVDA-Dev-Test-Toolbox/security/advisories/GHSA-39pg-6xpm-mjgf)).
* IO beep messages are now correctly reported with NVDA 2019.2.1.
* Log reading commands no longer fail to read some speech commands (e.g. when using Console Toolkit add-on)
* Addressed an issues where, in case of multiple possible reverse translations, the last menu item was copied to clipboard, no matter the item actually clicked.
* Prepared compatibility for NVDA 2026.1

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
* Addresses potential security issues related to [GHSA-xg6w-23rw-39r8][5] when using the add-on with older versions of NVDA.
However, it is recommended to use NVDA 2023.3.3 or higher.

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

[2]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]: https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
