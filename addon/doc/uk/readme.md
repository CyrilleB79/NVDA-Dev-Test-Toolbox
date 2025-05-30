# NVDA Dev & Test Toolbox #

* Автор: Cyrille Bougot
* Сумісність з NVDA: 2019.2 і пізніші
* Завантажити [стабільну версію][1]

Цей додаток включає різні функції для налагодження та тестування NVDA.

## Функції

* Покращений діалог  перезапуску для вказівки додаткових параметрів під час
  перезапуску NVDA.
* Різні функції, пов’язані з зареєстрованими помилками.
* Дослідник властивостей об’єктів.
* Script tools: an extended script description mode and a script opener.
* Команди, які допомагають читати та аналізувати журнали.
* Резервні копії старих журналів
* У робочій області консолі Python — функція для відкриття вихідного коду
  об’єкта.
* Спеціальний сценарій запуску для консолі Python
* Команда для журналу відстеження функції speech.speak.
* A command to reverse translate the items of the interface.

## Commands

This add-on uses layered commands for all of the new commands it adds.  The
entry point for these commands is `NVDA+X`; thus all the commands should be
executed by `NVDA+X` followed by another single letter or gesture.  You can
list all the available layered commands pressing `NVDA+X, H`.

For the commands that you use more frequently, you can also define a direct
gesture in the input gesture dialog.

## Розширений діалог перезапуску

The `NVDA+X, Q` command opens a dialog to specify some extra options before
restarting NVDA.  The options that can be specified correspond to the
[command line options][2] that can be used with `nvda.exe`, e.g. `-c` for
config path, `--disable-addons` to disable add-ons, etc.

## Функції, пов’язані з зареєстрованими помилками

### Додано сценарій для повідомлення про останню зареєстровану помилку

Pressing `NVDA+X, E` allows to report the last error logged without needing
to open the log. A second press clears the memorized last error.

### Відтворення звуку під час журналювання помилок

Налаштування [«Відтворення звуку під час журналювання помилок»][4] було
представлено в NVDA 2021.3 і дозволяє вказати, чи NVDA відтворюватиме звук
помилки, якщо помилка зареєстрована.

This add-on provides an additional command (`NVDA+X, shift+E`) to toggle
this setting.  You can choose:

* «Лише в тестових версіях» (початково), щоб сигнал помилки NVDA звучав,
  лише якщо поточна версія NVDA є тестовою (альфа-, бета-версія або запущена
  з джерела).
* «Yes», щоб увімкнути звук помилки незалежно від вашої поточної версії
  NVDA.

Для NVDA до 2021.3 цей додаток забезпечує бекпорт цієї функції та можливість
керувати нею за допомогою команд з клавіатури. Однак прапорець на панелі
додаткових налаштувань не з'явився.

## Дослідник властивостей об’єктів

Ця функція дозволяє повідомляти про деякі властивості поточного об’єкта
навігатора, не відкриваючи переглядач журналу.

Щоб отримати список властивостей об’єкта, перемістіть до нього об’єктний
навігатор і скористайтеся такими командами:

* `NVDA+X, upArrow`: Selects the previous property and reports it for the
  navigator object.
* `NVDA+X, downArrow`: Selects the next property and reports it for the
  navigator object.
* `NVDA+X, N`: Reports the currently selected property for the navigator
  object
* `NVDA+X, shift+N`: Displays the currently selected property for the
  navigator object in a browseable message

Список підтримуваних властивостей такий: ім’я, роль, стан, значення,
windowClassName, windowControlID, windowHandle, місцезнаходження, клас
Python, клас Python mro.

When using object navigation commands, you can also choose to have the
currently selected property reported instead of NVDA usual object
reporting.  A toggle command, `NVDA+X, control+N`, allows to switch between
this custom reporting of objects and NVDA usual reporting.

For exemple, you may select "windowClassName" property and enable custom
object reporting.  Then when moving the navigator object to next or previous
object, you will hear the object's windowClassName instead of usual
reporting.

## Script tools

<a id="scriptOpener"></a>
### The script opener

The script opener command allows to open the code of a script knowing its
gesture.

To use it press `NVDA+x, C` and then the gesture of the script which you
want to see the code of.  For example to see the code of the script that
reports the title of the foreground window, press `NVDA+X, C` and then
`NVDA+T`.

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source, the [location of NVDA source
code](#settingsNvdaSourcePath) should also have been configured.

### Режим розширеного опису сценарію

The extended script description mode allows to have reported information on
scripts without description in input help mode.

When the Extended script description mode is active, the input help mode
(NVDA+1) is modified as follows.  If a script has no description, the
script's name and class are reported.  If a script has a description, its
description is reported as usual.  The gesture to activate or deactivate
this feature is `NVDA+X, D`.

Виконання жесту, прив’язаного до сценарію без опису в режимі допомоги при
введенні також створює запис для цього сценарію в діалозі керування
жестами.  Цей запис розташовано у спеціальній категорії під назвою «Сценарії
без опису (змінюйте на свій страх і ризик!)».  Це дозволяє легко додавати,
видаляти або змінювати рідні жести NVDA для цих сценаріїв.  Однак майте на
увазі: часто передбачається, що такий сценарій не має жодного опису, щоб
запобігти користувачеві змінити пов’язаний жест.  Дійсно, жест можна
визначити, щоб він відповідав клавіші швидкого доступу програми.  Наприклад,
сценарій увімкнення курсиву на NVDAObjects.window.winword.WordDocument
прив’язаний до control+I, і це не варто змінювати, оскільки жест передається
програмі для фактичного виконання комбінації клавіш.

### Приклад використання

Control+shift+I також перемикає курсив у Word, навіть якщо про це не
повідомляє NVDA. Щоб NVDA повідомила результат control+shift+I як control+I,
вам варто виконати такі кроки:

* Відкрити документ Word.
* Enable the extended script description mode with `NVDA+X, D`.
* Увімкніть режим допомоги при введенні за допомогою NVDA+1.
* Натисніть Control+I, щоб повідомити про курсив і додати його в діалог
  жестів.
* Вимкніть режим допомоги при введенні за допомогою NVDA+1.
* Відкрийте діалог  жестів вводу.
* У категорії «Сценарії без опису (змінюйте на свій страх і ризик!)»
  виберіть команду «toggleItalic на
  NVDAObjects.window.winword.WordDocument».
* Додайте комбінацію клавіш control+shift+I та перевірте.
* If you want, exit the extended script description mode with `NVDA+X, D`.

Відома помилка: сценарій, доданий для певного класу, видимий, навіть якщо
менеджер жестів відкрито в іншому контексті.

## Log reading and analyzing features

<a id="logPlaceMarkers"></a>
### Place markers in the log

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press `NVDA+X, K`.
A message as follows will be logged at INFO level:  
`-- NDTT marker 0 --`  
You can add as many markers as you want in the log.  The marker's number
will be incremented each time you place a marker in the log; it will only be
reset when NVDA is restarted.

### Log reader mode

A log reader mode provides commands to ease log reading and analyzing.  In
the log viewer window the log reader is enabled by default, thus log reading
commands are available immediately.  In another text reading area such as an
editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press
`NVDA+X, L` to enable log reader mode and use its commands.  When you are
done with log reading and analyzing tasks, you can disable again `NVDA+X, L`
to disable the log reader mode.

Команди, доступні в режимі читання журналу, описані нижче.

<a id="logReaderQuickNavigationCommands"></a>
#### Команди швидкої навігації

Команда з однієї літери, подібна до клавіш швидкої навігації в режимі
огляду, дозволяє переходити до різних типів повідомлень журналу:

* m: будь-яке повідомлення
* e: error messages (`ERROR` and `CRITICAL`)
* w: warning messages (`WARNING`)
* f: info messages (`INFO`)
* k: markers previously [placed in the log](#logPlaceMarkers)
* g: debug warning messages (`DEBUGWARNING`)
* i: input/output messages (`IO`)
* n: input messages
* s: speech messages
* d: debug messages (`DEBUG`)

Натискання однієї літери переходить до наступної події цього
повідомлення. Комбінування літери з клавішею shift дозволяє перейти до
попередньої події повідомлення.

#### Translation of speech message

Sometimes, you may have to look at a log taken on a system in a foreignh
language that you do not understand. E.g. the log was taken on a Chinese
system / NVDA, whereas you only understand French.  If you have [Instant
Translate][3] add-on installed, you may use it in conjonction with [quick
log navigation commands](#logReaderQuickNavigationCommands) to have speech
messages translated.

* First configure Instant Translate's languages. The source language should
  be the language of the system where the log has been taken
  (e.g. Chinese). The target language should be your language (e.g. French).
* Open the log
* Press T to enable automatic speech translation in the log
* Use Quick navigation commands in the log, e.g. S, I, etc. Whenever a
  speech message is encountered, it will be spoken in your language (French
  in our previous example)

If you want to disable speech translation, press T again.



<a id="logReaderOpenSourceFile"></a>
#### Відкрийте файл вихідного коду у вашому редакторі

У журналі деякі рядки можуть посилатися на вихідний код:

* Рядок, що належить до відстеження, містить шлях і рядок у файлі,
  наприклад:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* Рядок заголовка зареєстрованого повідомлення містить функцію, яка
  зареєструвала це повідомлення, наприклад.:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* The content of a message logged in input help mode (logged at info level):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Ви можете відкрити файл, що містить цей код, щоб зрозуміти контекст
відстеження або зареєстрованого повідомлення. Просто натисніть C, щоб
відкрити цей файл.

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source and want to open NVDA's code, the [location
of NVDA source code](#settingsNvdaSourcePath) should also have been
configured.

<a id="oldLogsBackup"></a>
## Резервне копіювання старих журналів

NVDA вже надає резервну копію журналу попереднього сеансу роботи NVDA; файл
називається `nvda-old.log`.  Однак іноді вам може знадобитися доступ до
старих журналів, наприклад, якщо вам довелося перезапустити NVDA, перш ніж
переглянути `nvda-old.log`.  За допомогою цього додатка ви можете
налаштувати, чи потрібно створювати резервну копію старих журналів і скільки
їх має бути; це робиться у [налаштуваннях додатка] (#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs and perform various actions on the selected log:

* open it (press `Enter`)
* delete it (press `Delete`)
* copy the log file (press `control+C`)

You can also select multiple logs to perform an actions on all of them.

To be able to open a log, you should first have configured the [Command to
open a file in your favorite editor](#settingsOpenCommand).

## Розширення консолі Python

<a id="pythonConsoleOpenCodeFile"></a>
### Функція openCodeFile

У консолі можна викликати таку функцію, щоб переглянути вихідний код, який визначає змінну `myVar`:
`openCodeFile(myVar)`

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source and want to open NVDA's code, the [location
of NVDA source code](#settingsNvdaSourcePath) should also have been
configured.

Функції `openCodeFile` можна викликати для об’єктів, розміщених у коді NVDA,
або для об’єктів, визначених додатками. Його не можна викликати на об’єктах,
вихідний код яких недоступний, наприклад, вбудовані модулі python.

Якщо ви ще не імпортували об’єкт у консоль, ви також можете передати його
ім’я як параметр у `openCodeFile`.

Нижче наведено приклади викликів у коді NVDA:

* Переглянути визначення функції `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`
  або з ім'ям, переданим як параметр:  
  `openCodeFile("speech.speech.speak")`  
* Переглянути визначення класу `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`  
* Переглянути визначення методу `copyToClipboard` класу `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Переглянути визначення класу вибраного об’єкта:
  `openCodeFile(focus)`  
* Відкрийте файл `api.py`, що визначає модуль `api`:
  `openCodeFile(api)`  

### Сценарій запуску консолі Python

Ви можете призначити спеціальний сценарій, який виконуватиметься в просторі
імен консолі Python під час її першого відкриття або перезавантаження
додатка (NVDA+F3) після того, як консоль уже відкриється.

Наприклад, сценарій дозволяє вам виконувати новий імпорт і визначати псевдоніми, які ви зможете використовувати безпосередньо в консолі, як показано нижче:

   # Різний імпорт, який я хочу в консолі.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

Сценарій консолі Python варто розмістити в такому місці: `pathToNVDAConfig\\ndtt\consoleStartup.py`
Наприклад:
`C:\Users\myUserName\AppData\Roaming\\nvda\\ndtt\consoleStartup.py`

## Журнал відстеження функцій мовлення

Sometimes, you may want to see which part of the code is responsible for
speaking something.  For this, you can enable the stack trace logging of the
speech function pressing `NVDA+X, S`.  Each time NVDA speaks, a
corresponding stack trace will be logged in the log.

Примітка. Ви можете змінити файл сценарію безпосередньо, щоб виправити іншу
функцію. Перегляньте всі інструкції у файлі, щоб дізнатися більше про
використання.

<a id="reverseTranslationCommand"></a>
## Reverse translation command

Many testers use NVDA in another language than English.  But when reporting
test results on GitHub, the description of the modified options or the
messages reported by NVDA should be written in English.  Its quite
frustrating and time consuming to have to restart NVDA in English to check
the exact wording of the options or messages.

To avoid this, the add-on provides a reverse translation command (`NVDA+X,
R`) allowing to reverse translate NVDA's interface such as messages, control
labels in the GUI, etc.  This command uses NVDA's gettext translation to try
to reverse translate the last speech.  More specifically, the first string
of the last speech sequence is reverse translated.

For example, in French NVDA, if I arrow down to the Tools menu named
"Outils", NVDA will say "Outils sous-Menu o" which stands for "Tools subMenu
o".  If I press the reverse translation command just after that, NVDA will
reverse translate "Outils" to "Tools".

Looking at the log afterwards, we can find the following lines:
```
IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]
```
This confirms that "Outils was the first string in the speech sequence.

In case the reverse translation leads to two or more possible results, a
context menu is opened listing all the possibilities.

The result of the reverse translation is also copied to the clipboard if the
corresponding [option](#settingsCopyReverseTranslation) is enabled, which is
the default value.

<a id="settings"></a>
## Налаштування

Деякі функції додатка можуть потребувати певної конфігурації.
Панель налаштувань дозволяє увімкнути їх або керувати їхньою роботою.
Щоб переглянути і змінити ці налаштування, перейдіть до меню NVDA -> Параметри -> Налаштування і виберіть категорію NVDA Dev & Test Toolbox.
До цього діалога  налаштувань також можна отримати доступ безпосередньо з діалога Менеджер журналів.

Ці параметри є глобальними, і їх можна налаштувати, лише коли активний
початковий профіль.

<a id="налаштування Відкрити Команду"></a>
### Команда для відкриття файлу у вашому улюбленому редакторі

Some features allow to see content in your favorite editor.  This includes
the commands to view the source file [from a log](#logReaderOpenSourceFile),
[from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed
gesture](#scriptOpener), as well as the [log manager](#oldLogsBackup)'s Open
button.

Щоб ними скористатися, спочатку потрібно налаштувати команду, яка буде викликати відкриття файлу у вашому улюбленому редакторі.
Команда повинна мати вигляд:
`"C:\path\до\мій\редактор\editor.exe" "{path}":{line}`  
Звичайно, вам слід змінити цей рядок відповідно до справжньої назви і розташування вашого редактора та синтаксису, який він використовує для відкриття файлів.
`{path}` буде замінено на повний шлях до файлу, який потрібно відкрити, а `{line}` - на номер рядка, на якому потрібно встановити курсор.
Для Notepad++, наприклад, команда для введення у консолі буде такою:  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Шлях вихідного коду NVDA

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\pathExample\GIT\nvda\source`  
Звісно ж, замініть шлях джерела NVDA на правильний.

Але переконайтеся, що версія вашого вихідного файлу (наприклад, GIT commit)
збігається з версією запущеного екземпляра NVDA.

<a id="Налаштування Журналівв Резервного копіювання"></a>\n
### Резервне копіювання старих журналів

Комбінований список Резервне копіювання старих журналів дозволяє увімкнути
або вимкнути [функцію](#oldLogsBackup).  Якщо її увімкнено, ви також можете
вказати нижче у полі "Обмежити кількість резервних копій" максимальну
кількість резервних копій, яку ви хочете зберегти.  Ці налаштування набудуть
чинності лише під час наступного запуску NVDA, коли буде виконано резервне
копіювання.

<a id="settingsCopyReverseTranslation"></a>
### Copy reverse translation to clipboard

This option allows to choose if the [reverse translation
command](#reverseTranslationCommand) also copies its result to the
clipboard.

## Журнал змін

### Version 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.  The
  existing commands have been modified accordingly.
* A new command (`NVDA+X, R`) to reverse translate the last spoken message.
* A new command (`NVDA+X, C`) to open the source code of the script
  associated to the next pressed gesture.
* Added speech on demand support.
* The log manager now allows more actions, either with the dedicated buttons
  in the dialogs or using keyboard shortcuts in the list: `enter` to open
  the log, `control+C` to copy the log file and `delete` to delete a log
  file.
* The sorting order in the log manager has been reversed (most recent log on
  top).
* Fixed an issue when trying to open a Python module with openCodeFile
  function.

### Version 6.3

* Compatibility with NVDA 2024.1.

### Version 6.2

* Restores console opening for NVDA < 2021.1.
* Addresses potential security issues related to [GHSA-xg6w-23rw-39r8][5]
  when using the add-on with older versions of NVDA. However, it is
  recommended to use NVDA 2023.3.3 or higher.

### Version 6.1

* Opening the source file of an object located in the submodule of a package
  is now working.
* Bugfix: The enhanced exit dialog can now be reopened and used as expected
  after having been closed. (contribution from Łukasz Golonka)

### Version 6.0

* While using object navigation commands, a specific object property can be
  reported instead of NVDA usual object reporting.
* In log reading mode, the "C" key to open a code file from the log now also
  works on an input help message.
* Bugfix: The add-on can now start successfully when the number of logs to
  save is set to its maximum value.
* Bugfix: Python console startup script's output does not prevent anymore to
  jump to the first result in the console when using result navigation
  commands.
* Note: From now on, localization updates will not appear anymore in the
  change log.

### Version 5.0

* If Instant Translate add-on is installed, it is now possible to have
  speech messages translated on the fly when using log reading commands.
* While in log reading mode, pressing E or shift+E now jumps to CRITICAL
  erorr messages as well as normal ERROR messages.
* New log quick navigation commands have been added to jump to input and to
  speech messages.
* A new command allow to place a marker in the log; and specific quick
  navigation commands in log reading mode allow to jump to them.
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
* The add-on's settings can now be modified only when the default profile is
  active to avoid config issues.

### Версія 4.0

* Можливість резервного копіювання старих журналів і впровадження менеджера
  журналів.
* Додано сценарій для повідомлення про останню зареєстровану помилку.
* Виправлено помилку, через яку в старіших версіях NVDA не можна було
  прочитати останнє повідомлення журналу.

### Версія 3.2

* Сумісність з NVDA 2023.1.

### Версія 3.1

* Виправлено помилку, що виникала при запиті недоступної інформації про
  об'єкт.

### Версія 3.0

* Тепер у журналі можна натиснути C у рядку заголовка повідомлення, щоб
  відкрити функцію/модуль, який його створив.
* У консолі функція `openCodeFile` тепер може отримувати параметр об'єкта
  або рядок, що містить його ім'я.
* Нова функція: файл запуску консолі NVDA: якщо він існує, файл
  YourNVDAConfigFolder\ndtt\consoleStartup.py буде виконано під час першого
  відкриття консолі NVDA або під час перезавантаження додатків.
* Різні незначні виправлення для функції консолі Python `openCodeFile` і
  команди для відкриття вихідного файлу, що відповідає рядку в журналі.
* Виправлено проблему під час спроби повідомити про ролі/стани для
  дослідника об’єктів у старішій версії NVDA.
* Додаток більше не створює проблем із перехоплювачем дерева під час
  використання UIA в Edge.

### Версія 2.1

* Various bugfixes and code refactoring/cleaning to address all use cases:
  all supported versions, installed vs. run from source, etc. (contribution
  from Łukasz Golonka)
* Rewriting of the compa module (contribution from Łukasz Golonka)
* Діалог перезапуску  можна відкрити лише один раз.
* Комбінації дослідника об’єктів тепер початково не призначені й повинні
  бути призначені користувачем.
* У досліднику об’єктів подвійне натискання при виклику сценарію для
  інформування про властивості поточного об’єкта тепер відображає інформацію
  в повідомленні для перегляду.

### Версія 2.0

* Нова функція: розширений діалог перезапуску для налаштування додаткових
  параметрів під час перезапуску NVDA.
* Нова функція: розширений режим опису.
* Функція відтворення звуку помилки гармонізована між версіями NVDA до та
  після 2021.3.
* Нова функція: команди читання журналу тепер доступні у переглядачі
  журналу, а також, за бажанням, у полях редагування або на веб-сторінках.
* Нова функція: у консолі Python доступна функція openCodeFile для перегляду
  вихідного коду об’єкта.
* Деякі функції тепер вимкнено в безпечному режимі з міркувань безпеки.
* Діапазон сумісності додатка розширено (з 2019.2 до 2021.1).
* Нові версії тепер виконуються за допомогою дії GitHub замість appVeyor.

### Версія 1.0

* Початкова версія.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/uk/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/uk/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
