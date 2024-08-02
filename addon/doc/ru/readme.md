# NVDA Dev & Test Toolbox #
* Автор: Cyrille Bougot
* Совместимость с NVDA: 2019.2 и выше
* Загрузить [стабильную версию][1]

Это дополнение объединяет различные функции для отладки и тестирования NVDA.

## Возможности

* Расширенный диалог перезапуска для указания некоторых дополнительных
  параметров при перезапуске NVDA.
* Различные функции, связанные с зарегистрированными ошибками.
* Обозреватель свойств объекта.
* An extended script description mode: when enabled input help mode report
  information on scripts that have no description.
* Команды, помогающие считывать и анализировать журнал.
* Резервные копии старых журналов
* В рабочей области консоли Python есть функция для открытия исходного кода
  объекта.
* Пользовательский скрипт запуска для консоли Python
* Команда для регистрации трассировки стека функции speech.speak.

## Расширенный диалог перезапуска

Команда NVDA+shift+Q открывает диалог для указания некоторых дополнительных
параметров перед перезапуском NVDA.  Параметры, которые можно указать,
соответствуют [параметрам командной строки][2], которые можно использовать с
`nvda.exe`, например, `-c` для пути к конфигурации, `--disable-addons` для
отключения дополнений и т.д.

## Функции, связанные с зарегистрированными ошибками

### Сообщить о последней зарегистрированной ошибке

Нажатие клавиш NVDA+shift+alt+E позволяет сообщить о последней
зарегистрированной ошибке без необходимости открывать журнал. Повторное
нажатие удаляет сохранённую в памяти последнюю ошибку.

### Воспроизведение звука при обнаружении зарегистрированных ошибок

Параметр ["Воспроизводить звук при зарегистрированных ошибках"][4] был
введен в NVDA 2021.3 и позволяет указать, будет ли NVDA воспроизводить звук
ошибки в случае регистрации ошибки.

Это дополнение предоставляет дополнительную команду (NVDA+control+alt+E) для
переключения этой настройки.  Вы можете выбрать:

* "Только в тестовых версиях" (по умолчанию), чтобы ошибка воспроизведения
  NVDA воспроизводилась только в том случае, если текущая версия NVDA
  является тестовой (альфа, бета-версия или запущена из исходного кода).
* "Да", чтобы включить звуковые сигналы об ошибках, независимо от вашей
  текущей версии NVDA.

Для NVDA до 2021.3 это дополнение обеспечивает перенос этой функции и
возможность управлять ею с помощью команд с клавиатуры.  Однако флажок в
панель дополнительных настроек не перенесён.

## Object property explorer

This feature allows to report some properties of the current navigator
object without opening the log viewer.

To list the properties of an object, move the navigator object to it and use
the following commands:

* Selects the previous property and reports it for the navigator object.
* Selects the next property and reports it for the navigator object.
* Reports the currently selected property for the navigator object; two
  presses displays this information in a browseable message.

The list of the supported properties is the following: name, role, state,
value, windowClassName, windowControlID, windowHandle, location, Python
class, Python class mro.

When using object navigation commands, you can also choose to have the
currently selected property reported instead of NVDA usual object
reporting.  A toggle command allows to switch between this custom reporting
of objects and NVDA usual reporting.

For exemple, you may select "windowClassName" property and enable custom
object reporting.  Then when moving the navigator object to next or previous
object, you will hear the object's windowClassName instead of usual
reporting.

All the commands of the Object property explorer are unassigned by default;
you will have to assign them a shortcut in the Input gesture dialog to use
them.

## Extended script description mode

When the Extended script description mode is active, the input help mode
(NVDA+1) is modified as follows.  If a script has no description, the
script's name and class are reported.  If a script has a description, its
description is reported as usual.  The gesture to activate or deactivate
this feature is NVDA+control+alt+D.

Executing a gesture bound to a script without description in input help mode
also create an entry for this script in the gesture management dialog.  This
entry is located in a dedicated category called "Scripts without description
(modify at your own risk!)".  This allow to easily add, delete or change the
native NVDA gestures for these script.  Be aware however that it is often
intended that such script do not have any description to prevent the user to
modify the associated gesture.  Indeed, the gesture may be defined to match
an application shortcut key.  For example the script script_toggleItalic on
NVDAObjects.window.winword.WordDocument is bound to control+I and this
should not be modified since the gesture is passed to the application to
actually execute the shortcut key.

### Usage example

Control+shift+I also toggle italic in Word, even if it is not natively
reported by NVDA.  To have the control+shift+I result reported by NVDA as
control+I, you should perform the following steps:

* Open a Word document.
* Enable the extended script description mode with NVDA+control+alt+D.
* Enter input help mode with NVDA+1.
* Press control+I to report the italic script and have it added in the
  gesture dialog.
* Exit input help mode with NVDA+1.
* Open the input gestures dialog.
* In the category "Scripts without description (modify at your own risk!)",
  select the command "toggleItalic on
  NVDAObjects.window.winword.WordDocument".
* Add the control+shift+I shortcut and validate.
* If you want, exit the extended script description mode with
  NVDA+control+alt+D.

Known bug: A script added for a specific class is visible even if gesture
manager is opened in another context.

## Функции чтения и анализа журналов

<a id="logPlaceMarkers"></a>
### Place markers in the log

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press NVDA+control+K.
A message as follows will be logged at INFO level:  
`-- NDTT marker 0 --`  
You can add as many markers as you want in the log.  The marker's number
will be incremented each time you place a marker in the log; it will only be
reset when NVDA is restarted.

### Режим чтения журналов

Режим чтения журналов предоставляет команды, облегчающие чтение и анализ
журналов.  В окне просмотра журналов функция чтения журналов включена по
умолчанию, поэтому команды чтения журналов доступны немедленно.  В другой
области чтения текста, такой как редактор (например, Notepad++) или
веб-страница (например, GitHub issue), вам нужно нажать NVDA+control+alt+L,
чтобы включить режим чтения журнала и использовать его команды.  Когда вы
закончите чтение журнала и анализ задач, вы можете снова нажать
NVDA+control+alt+L, чтобы отключить режим чтения журнала.

Команды, доступные в режиме чтения журнала, описаны ниже.

<a id="logReaderQuickNavigationCommands"></a>
#### Команды быстрой навигации

Однобуквенная команда, аналогичная клавишам быстрой навигации в режиме
обзора, позволяет переходить к различным типам сообщений журнала:

* m: любое сообщение
* e: сообщения об ошибках (`ERROR` и `CRITICAL`)
* w: предупреждающие сообщения (`WARNING`)
* f: информационные сообщения (`INFO`)
* k: маркеры, ранее [помещенные в журнал](#logPlaceMarkers)
* g: предупреждающие сообщения об отладке (`DEBUGWARNING`)
* i: сообщения ввода/вывода (`IO`)
* n: сообщения ввода
* s: речевые сообщения
* d: сообщения отладки (`DEBUG`)

Нажатие на одну букву приводит к переходу к следующему появлению этого
сообщения. Сочетание буквы с клавишей shift приводит к переходу к
предыдущему появлению этого сообщения.

#### Перевод речевого сообщения

Иногда вам может потребоваться просмотреть журнал, созданный в системе на
иностранном языке, который вы не понимаете. Например, журнал был создан в
китайской системе / NVDA, в то время как вы понимаете только французский.
Если у вас установлено дополнение [Instant Translate][3], вы можете
использовать его в сочетании с [командами быстрой навигации по
журналу](#logReaderQuickNavigationCommands) для перевода речевых сообщений.

* Сначала настройте языки Instant Translate. Исходным языком должен быть
  язык системы, в которой был создан журнал (например, китайский). Целевым
  языком должен быть ваш язык (например, французский).
* Откройте журнал
* Нажмите T, чтобы включить автоматический перевод речи в журнале
* Используйте команды быстрой навигации в журнале, например, S, I и т.д. При
  появлении речевого сообщения оно будет передано на вашем языке (в нашем
  предыдущем примере - на французском)

Если вы хотите отключить перевод речи, нажмите T ещё раз.



<a id="logReaderOpenSourceFile"></a>
#### Откройте файл с исходным кодом в вашем редакторе

В журнале какая-то строка может ссылаться на исходный код:

* Строка, относящаяся к обратной трассировке, содержит путь и строку в
  файле, например:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* Строка заголовка зарегистрированного сообщения содержит функцию, которая
  зарегистрировала это сообщение, например:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* Содержимое сообщения, зарегистрированного в режиме справки по вводу
  (регистрируется на информационном уровне):
  Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Возможно, вы захотите открыть файл, содержащий этот код, чтобы понять
контекст обратной трассировки или зарегистрированного сообщения.  Просто
нажмите C, чтобы открыть этот файл.

Чтобы эта функция работала, вам необходимо настроить [команду вашего
любимого редактора](#settingsOpenCommand) в настройках дополнения.  Если вы
не запускаете NVDA из исходного кода, то [расположение исходного кода
NVDA](#settingsNvdaSourcePath) также должно быть настроено.

<a id="oldLogsBackup"></a>
## Резервное копирование старых журналов

NVDA уже предоставляет резервную копию журнала предыдущей сессии NVDA; файл
называется "nvda-old.log`.  Однако иногда вам может потребоваться получить
доступ к более старым журналам, например, из-за того, что вам пришлось снова
перезапустить NVDA, прежде чем просматривать "nvda-old.log`.  Это дополнение
позволяет вам настроить, хотите ли вы создавать резервные копии старых
журналов и сколько их; это делается в [настройках
дополнения](#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs, open or delete them.
To be able to open a log, you should first have configured the [Command to open a file in your favorite editor](#settingsOpenCommand).

## Расширение консоли Python

<a id="pythonConsoleOpenCodeFile"></a>
### функция `openCodeFile`

В консоли вы можете вызвать следующую функцию для просмотра исходного кода, который определяет переменную `myVar`:  
`openCodeFile(myVar)`  

Чтобы эта функция работала, вам необходимо настроить [команду вашего
любимого редактора](#settingsOpenCommand) в настройках дополнения.  Если вы
не запускаете NVDA из исходного кода, то [расположение исходного кода
NVDA](#settingsNvdaSourcePath) также должно быть настроено.

Функции `openCodeFile` могут быть вызваны для объектов, определённых в коде
NVDA, или для объектов, определённых дополнениями.  Они не могут быть
вызваны для объектов, исходный код которых недоступен, таких как встроенные
модули python.

Если вы ещё не импортировали объект в консоль, вы также можете передать его
имя в качестве параметра функции `openCodeFile`.

Ниже приведены примеры вызовов в коде NVDA:

* Просмотреть определение функции `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`  
  или с именем, переданным в качестве параметра:  
  `openCodeFile("speech.speech.speak")`  
* Просмотреть определение класса `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`  
* Просмотреть определение метода `copyToClipboard` класса `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Просмотр определения класса объекта в фокусе:
  `openCodeFile(focus)`  
* Открыть файл "api.py`, определяющий модуль `api`:
  `openCodeFile(api)`  

### Python console startup script

You can define a custom script which will be executed in the Python
console's namespace when it is first opened, or if the add-on is reloaded
(NVDA+F3) after the console has already been opened.

For example, the script allows you to execute new imports and define aliases that you will be able to use directly in the console, as shown below:  

    # Various import that I want in the console.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

The Python console script should be placed in the following location: `pathToNVDAConfig\ndtt\consoleStartup.py`  
For example:
`C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Log the stack trace of the speech function

Sometimes, you may want to see which part of the code is responsible for
speaking something.  For this, you can enable the stack trace logging of the
speech function pressing NVDA+control+alt+S.  Each time NVDA speaks, a
corresponding stack trace will be logged in the log.

Note: You may modify the script's file directly to patch another function.
See all instructions in the file for details on usage.

<a id="settings"></a>
## Settings

Some features of the add-on may require a specific configuration.
A settings panel allows to enable them or to control how they work.
To view and modify these settings, go to NVDA menu -> Preferences and select the category NVDA Dev & Test Toolbox.
This settings dialog can also be accessed directly from the Logs Manager dialog.

These settings are global and can only be configured when the default
profile is active.

<a id="settingsOpenCommand"></a>
### Command to open a file in your favorite editor

Some features allow to see content in your favorite editor.  This includes
the commands to view the source file [from a log](#logReaderOpenSourceFile)
or [from an object in the console](#pythonConsoleOpenCodeFile) as well as
the [log manager](#oldLogsBackup)'s Open button.

To use them, you first need to configure the command that will be called to open the file in your favorite editor.
The command should be of the form:  
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
You should of course modify this line according to the real name and location of your editor and the syntax used by it to open files.
`{path}` will be replaced by the full path of the file to open and `{line}` by the line number where you want the cursor to be set.
For Notepad++ for example the command to type in the console would be:  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA source code path

When using a command to [view the source file from a log](#logReaderOpenSourceFile) or [from an object in the console](#pythonConsoleOpenCodeFile), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\pathExample\GIT\nvda\source`  
Of course, replace the path of NVDA source with the correct one.

Be sure however that the version of your source file (e.g. GIT commit) is
the same as the one of the running instance of NVDA.

<a id="settingsLogsBackup"></a>
### Резервное копирование старых журналов

The combobox Backup of old logs allows to enable or disable the
[feature](#oldLogsBackup).  If it is enabled, you can also specify below in
"Limit the number of backups" the maximum number of backups you want to
keep.  These settings only take effect at next NVDA startup when the backup
takes place.

## Журнал изменений

### Версия 6.2

* Восстанавливает открытие консоли для NVDA < 2021.1.
* Устраняет потенциальные проблемы безопасности, связанные с
  [GHSA-xg6w-23rw-39r8][5] при использовании дополнения со старыми версиями
  NVDA. Однако рекомендуется использовать NVDA 2023.3.3 или выше.

### Версия 6.1

* Открытие исходного файла объекта, расположенного в подмодуле пакета,
  теперь работает.
* Исправлена ошибка: расширенный диалог выхода теперь можно снова открыть и
  использовать как положено после его закрытия. (автор Łukasz Golonka)

### Версия 6.0

* При использовании команд навигации по объектам можно сообщать о конкретном
  свойстве объекта вместо обычных отчетов об объектах NVDA.
* В режиме чтения журнала нажатие клавиши "C" для открытия файла кода из
  журнала теперь также работает с справочным сообщением ввода.
* Исправлена ошибка: теперь дополнение может успешно запускаться, если
  количество сохраняемых журналов установлено на максимальное значение.
* Исправлена ошибка: вывод скрипта запуска консоли Python больше не мешает
  переходить к первому результату в консоли при использовании команд
  навигации по результатам.
* Примечание: Отныне обновления локализации больше не будут отображаться в
  журнале изменений.

### Версия 5.0

* Если установлено дополнение Instant Translate, теперь можно переводить
  речевые сообщения "на лету" при использовании команд чтения журнала.
* В режиме чтения журнала нажатие E или shift+E теперь приводит к появлению
  критических сообщений об ошибках, а также обычных сообщений об ошибках.
* Добавлены новые команды быстрой навигации по журналу для перехода к
  вводимым данным и речевым сообщениям.
* Новая команда позволяет размещать маркер в журнале, а специальные команды
  быстрой навигации в режиме чтения журнала позволяют переходить к
  ним. Автор: первоначальная идея этой функции взята из дополнения Debug
  Helper от Luke Davis.
* Исправление ошибок: в некоторых случаях запоминание последней ошибки
  больше не приводит к сбоям.
* Исправлена ошибка: Дополнение может быть снова инициализирована с помощью
  NVDA 2019.2.1.
* Исправлена ошибка: функция сохранения журналов больше не будет сбоить при
  использовании журналов, отличных от ASCII.

### Версия 4.2

* Исправлена ошибка с версией NVDA ниже 2021.3.
* Исправлено форматирование журнала трассировки стека.
* Первые локализации.

### Версия 4.1

* Исправлена ошибка, возникавшая в некоторых ситуациях при регистрации
  ошибки.
* Настройки дополнения теперь можно изменять только при активном профиле по
  умолчанию, чтобы избежать проблем с настройкой.

### Версия 4.0

* Возможность создания резервных копий старых журналов и внедрение менеджера
  журналов.
* Добавлен скрипт для сообщения о последней зарегистрированной ошибке.
* Исправлена ошибка, из-за которой в старых версиях NVDA не считывалось
  последнее сообщение журнала.

### Версия 3.2

* Совместимость с NVDA 2023.1.

### Версия 3.1

* Исправлена ошибка, возникавшая при запросе недоступной информации об
  объекте.

### Версия 3.0

* В журнале теперь вы можете нажать C в строке заголовка сообщения, чтобы
  открыть функцию/ модуль, который его отправил.
* В консоли функция `openCodeFile` теперь может принимать в качестве
  параметра объект или строку, содержащую его имя.
* Новая функция: файл запуска консоли NVDA: если он существует, то файл
  YourNVDAConfigFolder\\ndtt\consoleStartup.py будет запущен при первом
  открытии консоли NVDA или при перезагрузке дополнений.
* Различные мелкие исправления для работы консоли Python `openCodeFile` и
  команды для открытия исходного файла, соответствующего строке в журнале.
* Исправлена ошибка при попытке создания отчета о ролях/состояниях для
  обозревателя объектов в более старой версии NVDA.
* Дополнение больше не вызывает проблем с перехватчиком дерева при
  использовании UIA в Edge.

### Версия 2.1

* Различные исправления ошибок и рефакторинг / очистка кода для решения всех
  вариантов использования: все поддерживаемые версии, установленные по
  сравнению с предыдущими. запуск из исходного кода и т.д. (вклад Łukasz
  Golonka)
* Переписан модуль compa (автор Łukasz Golonka)
* Диалог перезапуска теперь можно открыть только один раз.
* Горячие клавиши обозревателя объектов теперь по умолчанию не назначены и
  должны быть сопоставлены пользователем.
* С помощью обозревателя объектов двойное нажатие для вызова сценария,
  сообщающего о свойстве текущего объекта, теперь отображает полученную
  информацию в виде сообщения, доступного для просмотра.

### Версия 2.0

* Новая функция: Расширенный диалог перезапуска для указания некоторых
  дополнительных параметров при перезапуске NVDA.
* Новая функция: расширенный режим описания.
* Функция воспроизведения звука при ошибке была согласована в версиях NVDA
  до и после 2021.3.
* Новая функция: Команды чтения журналов теперь доступны в программе
  просмотра журналов, а также, при необходимости, в полях редактирования или
  на веб-страницах.
* Новая функция: В консоли Python доступна функция "openCodeFile" для
  просмотра исходного кода объекта.
* Некоторые функции теперь отключены в защищённом режиме по соображениям
  безопасности.
* Диапазон совместимости дополнения был расширен (с 2019.2 по 2021.1).
* Выпуски теперь выполняются с помощью GitHub action, а не AppVeyor.

### Версия 1.0

* Первоначальный выпуск.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
