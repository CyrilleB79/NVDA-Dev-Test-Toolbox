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
* Инструменты скрипта: расширенный режим описания скрипта и открытие
  скриптов.
* Команды, помогающие считывать и анализировать журнал.
* Резервные копии старых журналов
* В рабочей области консоли Python есть функция для открытия исходного кода
  объекта.
* Пользовательский скрипт запуска для консоли Python
* Команда для регистрации трассировки стека функции speech.speak.
* Команда обратного перевода элементов интерфейса.

## Команды

Это дополнение использует многослойные команды для всех новых команд,
которые оно добавляет.  Точка входа для этих команд - `nvda+x`; Таким
образом, все команды должны выполняться с помощью `nvda+x`, за которой
следует одна буква или жест.  Вы можете узнать все доступные многослойные
команды, нажимая `nvda+x, h`.

Для часто использующихся команд, вы также можете определить прямой жест в
диалоге жестов ввода.

## Расширенный диалог перезапуска

Команда `NVDA+X, Q` открывает диалог, чтобы указать некоторые дополнительные
параметры перед перезапуском NVDA.  Параметры, которые можно указать,
соответствуют параметрам [командной строки][2], которые можно использовать с
`nvda.exe`, например, `-c` для пути конфигурации, `--disable-addons`, чтобы
отключить дополнения и т. Д.

## Функции, связанные с зарегистрированными ошибками

### Сообщить о последней зарегистрированной ошибке

Нажатие `NVDA+X, E` позволяет сообщать о последней ошибке,
зарегистрированной без необходимости открывать журнал. Второе нажатие
очищает последнюю запомненную ошибку.

### Воспроизведение звука при обнаружении зарегистрированных ошибок

Параметр ["Воспроизводить звук при зарегистрированных ошибках"][4] был
введен в NVDA 2021.3 и позволяет указать, будет ли NVDA воспроизводить звук
ошибки в случае регистрации ошибки.

Это дополнение предоставляет дополнительную команду (`NVDA+X, shift+E`) для
переключения этой настройки.  Вы можете выбрать:

* "Только в тестовых версиях" (по умолчанию), чтобы ошибка воспроизведения
  NVDA воспроизводилась только в том случае, если текущая версия NVDA
  является тестовой (альфа, бета-версия или запущена из исходного кода).
* "Да", чтобы включить звуковые сигналы об ошибках, независимо от вашей
  текущей версии NVDA.

Для NVDA до 2021.3 это дополнение обеспечивает перенос этой функции и
возможность управлять ею с помощью команд с клавиатуры.  Однако флажок в
панель дополнительных настроек не перенесён.

## Обозреватель свойств объекта

Эта функция позволяет сообщать о некоторых свойствах текущего объекта
навигатора, не открывая просмотрщик журнала.

Чтобы просмотреть свойства объекта, переместите к нему объект навигатора и
используйте следующие команды:

* `NVDA+X, стрелка вверх`: Выбирает предыдущее свойство и сообщает его в
  объекте навигатора.
* `NVDA+X, стрелка вниз`: Выбирает следующее свойство и сообщает его в
  объекте навигатора.
* `NVDA+X, N`: Сообщает выбранное в настоящее время свойство в объекте
  навигатора
* `NVDA+X, shift+N`: Отображает выбранное в настоящее время свойство объекта
  навигатора в просмотровом сообщении

Список поддерживаемых свойств следующий: имя, роль, состояние, значение,
windowClassName, windowControlID, windowHandle, location, класс Python,
класс Python mro.

При использовании команд навигации объекта вы также можете выбирать в
настоящее время выбранное свойство вместо обычной отчётности по объектам
NVDA.  Команда переключения, `NVDA+X, control+N`, позволяет переключаться
между этой пользовательской отчётностью об объектах и обычной отчетностью
NVDA.

Например, вы можете выбрать свойство "windowClassName" и включить создание
объявлений по настраиваемым объектам.  Тогда при перемещении объекта
навигатора к следующему или предыдущему объекту вместо обычного сообщения вы
услышите имя класса окна объекта.

## Инструменты скрипта

<a id="scriptOpener"></a>
### Открытие скриптов

Команда открытия скриптов позволяет открывать код сценария, зная его жест.

Для её использования нажмите `NVDA+x, C` и затем жест скрипта, который вы
хотите увидеть.  Например, чтобы увидеть код скрипта, который сообщает
заголовок окна переднего плана, нажмите `NVDA+X, C` и затем `NVDA+T`.

Чтобы эта функция работала, вам нужно настроить [команду любимого
редактора](#settingsOpenCommand) в настройках дополнения.  Если вы не
запускаете NVDA из исходного кода и хотите открывать код NVDA, также нужно
настроить [местоположение исходного кода NVDA](#settingsNvdaSourcePath).

### Расширенный режим описания скрипта

Режим расширенного описания скрипта позволяет сообщать информацию о скриптах
без описания в режиме справки по вводу.

Когда активен режим расширенного описания скрипта, режим справки по вводу
(NVDA+1) изменяется следующим образом.  Если скрипт не имеет описания,
сообщаются имя и класс скрипта.  Если скрипт имеет описание, его описание
сообщается как обычно.  Жест для активации или деактивации этой функции -
`NVDA+X, D`.

Выполнение жеста, привязанного к сценарию без описания в режиме справки по
вводу, также создаёт запись для этого скрипта в диалоге управления жестами.
Эта запись находится в специальной категории "Скрипты без описания
(изменяйте на свой страх и риск!)".  Это позволяет легко добавлять, удалять
или изменять собственные жесты NVDA для этих скриптов.  Однако имейте в
виду, что часто предполагается, что такой скрипт не содержит никакого
описания, чтобы пользователь не мог изменить связанный жест.  Действительно,
жест может быть определён в соответствии с клавишей быстрого доступа
приложения.  Например, скрипт script_toggleItalic в
NVDAObjects.window.winword.WordDocument привязан к control+I, и его не
следует изменять, поскольку жест передаётся приложению для фактического
выполнения сочетания клавиш.

### Пример использования

Control+shift+I также переключает курсив в Word, даже если NVDA не сообщает
об этом изначально.  Чтобы NVDA сообщала о результате control+shift+I как
control+I, вам необходимо выполнить следующие шаги:

* Откройте документ Word.
* Включите режим расширенного описания скрипта с помощью `NVDA+X, D`.
* Войдите в режим справки по вводу с помощью NVDA+1.
* Нажмите Control+I, чтобы сообщить о курсиве и добавить его в диалог жестов
  ввода.
* Выйдите из режима справки по вводу с помощью NVDA+1.
* Откройте диалог жестов ввода.
* В категории "Скрипты без описания (изменяйте на свой страх и риск!)"
  выберите команду "toggleItalic в NVDAObjects.window.winword.WordDocument".
* Добавьте сочетание клавиш control+shift+I и подтвердите.
* Если хотите, выйдите из режима расширенного описания скрипта с помощью
  `NVDA+X, D`.

Известная ошибка: скрипт, добавленный для определённого класса, виден, даже
если диалог жестов ввода открыт в другом контексте.

## Функции чтения и анализа журналов

<a id="logPlaceMarkers"></a>
### Размещайте маркеры в журнале

Во время тестирования или работы вы можете отметить определенный момент в журнале, чтобы вы могли легко обратиться к нему позже при чтении журнала.
Чтобы добавить маркерное сообщение в журнал, нажмите `NVDA+X, K`.
Сообщение следующим образом будет зарегистрировано на уровне информации:  
`-- NDTT marker 0 --`  
Вы можете добавить в журнал столько маркеров, сколько захотите.  Номер
маркера будет увеличиваться каждый раз, когда вы помещаете его в журнал; он
будет сброшен только при перезапуске NVDA.

### Режим чтения журналов

Режим чтения журнала предоставляет команды для облегчения чтения журнала и
анализа.  В окне просмотра журнала чтец журнала включён по умолчанию,
поэтому команды чтения журнала доступны немедленно.  В другой области
считывания текста, такой как редактор (например, Notepad ++) или веб
-страница (например, проблема Github), вам необходимо нажать `NVDA+X, L`,
чтобы включить режим чтения журнала и использовать его команды.  Когда вы
закончите с чтением журнала и анализом задач, вы можете снова нажать
`NVDA+X, L`, чтобы отключить режим чтения журнала.

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
* Содержимое сообщения журналируется  в режиме справки по вводу (на уровне
  основной информации):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Возможно, вы захотите открыть файл, содержащий этот код, чтобы понять
контекст обратной трассировки или зарегистрированного сообщения.  Просто
нажмите C, чтобы открыть этот файл.

Чтобы эта функция работала, вам нужно настроить [команду любимого
редактора](#settingsOpenCommand) в настройках дополнения.  Если вы не
запускаете NVDA из исходного кода и хотите открывать код NVDA, также нужно
настроить [местоположение исходного кода NVDA](#settingsNvdaSourcePath).

<a id="oldLogsBackup"></a>
## Резервное копирование старых журналов

NVDA уже предоставляет резервную копию журнала предыдущей сессии NVDA; файл
называется "nvda-old.log`.  Однако иногда вам может потребоваться получить
доступ к более старым журналам, например, из-за того, что вам пришлось снова
перезапустить NVDA, прежде чем просматривать "nvda-old.log`.  Это дополнение
позволяет вам настроить, хотите ли вы создавать резервные копии старых
журналов и сколько их; это делается в [настройках
дополнения](#settingsLogsBackup).

Диалог диспетчера журнала позволяет просматривать резервные журналы.
Его можно открыть, переходя в меню NVDA -> Сервис -> Диспетчер журналов
В этом диалоге вы можете увидеть список всех журналов резервного копирования и выполнить различные действия в выбранном журнале:

* для его открытия (нажмите `Enter`)
* для его удаления (нажмите `Delete`)
* копировать файл журнала (нажмите `control+C`)

Вы также можете выбрать несколько журналов для выполнения действий по всем
им.

Чтобы иметь возможность открыть журнал, вы должны сначала настроить [команду
для открытия файла в вашем любимом редакторе](#settingsOpenCommand).

## Расширение консоли Python

<a id="pythonConsoleOpenCodeFile"></a>
### функция `openCodeFile`

В консоли вы можете вызвать следующую функцию для просмотра исходного кода, который определяет переменную `myVar`:  
`openCodeFile(myVar)`  

Чтобы эта функция работала, вам нужно настроить [команду любимого
редактора](#settingsOpenCommand) в настройках дополнения.  Если вы не
запускаете NVDA из исходного кода и хотите открывать код NVDA, также нужно
настроить [местоположение исходного кода NVDA](#settingsNvdaSourcePath).

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

### Скрипт при запуске консоли Python

Вы можете определить собственный скрипт, который будет выполняться в
пространстве имен консоли Python при ее первом открытии или при перезагрузке
дополнения (NVDA+F3) после того, как консоль уже была открыта.

Например, скрипт позволяет вам выполнять новый импорт и определять псевдонимы, которые вы сможете использовать непосредственно в консоли, как показано ниже:  

    # Various import that I want in the console.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

Консольный скрипт Python следует разместить в следующем месте: `pathToNVDAConfig\ndtt\consoleStartup.py`  
Например: `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Зарегистрируйте трассировку стека речевой функции

Иногда вы можете посмотреть, какая часть кода отвечает за то, что говорить.
Для этого вы можете включить регистрацию трассировки стека речевой функции,
нажимая `NVDA+X, S`.  Каждый раз, когда говорит NVDA, соответствующая
трассировка стека будет регистрироваться в журнале.

Примечание: Вы можете изменить файл скрипта напрямую, чтобы исправить другую
функцию.  Подробную информацию об использовании смотрите во всех инструкциях
в файле.

<a id="reverseTranslationCommand"></a>
## Команда обратного перевода

Многие тестеры используют NVDA на другом языке, а не на английском.  Но при
объявлениях результатов теста на GitHub описание изменённых параметров или
сообщений, представленных NVDA, должны быть написаны на английском.  Это
довольно разочаровывает и требует много времени, чтобы перезапустить NVDA на
английском языке для проверки точной формулировки вариантов или сообщений.

Чтобы избежать этого, дополнение предоставляет команду обратного перевода
(`NVDA+X, R`), позволяющую перевернуть перевод интерфейса NVDA, такой как
сообщения, метки управления в графическом интерфейсе и т. Д. Эта команда
использует перевод NVDA GetText, чтобы попытаться перевернуть последнюю
речь.  Более конкретно, первая строка последней речевой последовательности
переводится.

Например, во французской NVDA, если я стрелкой вниз перейду к меню сервиса
под названием "Outils", NVDA скажет "Outils sous-Menu o", что означает
"Tools subMenu o".  Если я сразу после этого нажму команду обратного
перевода, NVDA будет отменять перевод "Outils" в "Сервис".

Глядя на журнал после этого, мы можем найти следующие строки:
```
IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]
```
Это подтверждает, что "Outils" была первой строкой в ​​последовательности
речи.

В случае, если обратный перевод приводит к двум или более возможным
результатам, контекстное меню открывается в перечислении всех возможностей.

Результат обратного перевода также копируется в буфер обмена, если включена
соответствующая [опция](#settingsCopyReverseTranslation), что является
значением по умолчанию.

<a id="settings"></a>
## Настройки

Некоторые функции дополнения могут потребовать определённой настройки.
Панель настроек позволяет включать их или контролировать их работу.
Чтобы просмотреть и изменить эти настройки, перейдите в меню NVDA -> Настройки и выберите категорию NVDA Dev & Test Toolbox.
Доступ к этому диалогу настроек также можно получить непосредственно из диалога диспетчера журналов.

Эти параметры являются глобальными и могут быть настроены только в том
случае, если активен профиль по умолчанию.

<a id="settingsOpenCommand"></a>
### Команда для открытия файла в вашем любимом редакторе

Некоторые функции позволяют просматривать содержимое в вашем любимом
редакторе.  Сюда входят команды для просмотра исходного файла [из
журнала](#logReaderOpenSourceFile), [из объекта в
консоли](#pythonConsoleOpenCodeFile) или [для введённого
жеста](#scriptOpener), а также кнопка открытия [менеджера
журналов](#oldLogsBackup).

Чтобы их использовать, сначала необходимо настроить команду, которая будет вызываться для открытия файла в вашем любимом редакторе.
Команда должна иметь вид:  
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
Разумеется, вам следует изменить эту строку в соответствии с настоящим именем и местоположением вашего редактора, а также синтаксисом, используемым им для открытия файлов.
`{path}` будет заменён полным путём к файлу, который нужно открыть и `{line}` номером строки, на которую вы хотите установить курсор.
Например, для Notepad++ команда для ввода в консоли будет такой:  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Путь к исходному коду NVDA

При использовании команды для [просмотра исходного файла из журнала](#logReaderOpenSourceFile), [из объекта в консоли](#pythonConsoleOpenCodeFile) или [для введённого жеста](#scriptOpener)файл может принадлежать самой NVDA.
Если вы не используете NVDA из исходного кода, ваша NVDA содержит только скомпилированные файлы.
Таким образом, вы можете указать здесь альтернативное местоположение, где будет найден соответствующий исходный файл, например, место, где вы клонировали исходные файлы NVDA, чтобы исходный файл всё равно можно было открыть.
Путь должен быть таким:  
`C:\pathExample\GIT\nvda\source`  
Конечно, замените путь к исходному коду NVDA на правильный.

Однако убедитесь, что версия вашего исходного файла (например, коммита GIT)
совпадает с версией работающего экземпляра NVDA.

<a id="settingsLogsBackup"></a>
### Резервное копирование старых журналов

Комбинированный список резервного копирования старых журналов позволяет
включить или отключить [функцию](#oldLogsBackup).  Если эта функция
включена, вы также можете указать ниже в разделе ограничения количество
резервных копий максимальное количество резервных копий, которые вы хотите
сохранить.  Эти настройки вступят в силу только при следующем запуске NVDA,
когда будет выполнено резервное копирование.

<a id="settingsCopyReverseTranslation"></a>
### Копировать обратный перевод в буфер обмена

Эта опция позволяет выбирать, будет ли [команда обратного
перевода](#reverseTranslationCommand) копировать свой результат в буфер
обмена.

## Журнал изменений

### Версия 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.
  The existing commands have been modified accordingly.  
* Новая команда (`NVDA+X, R`) обратного перевода последнего произнесённого
  сообщения.
* Новая команда (`NVDA+X, C`) для открытия исходного скрипта, связанного со
  следующим нажатым жестом.
* Добавлена поддержка речи по требованию.
* Диспетчер журналов теперь содержит больше действий, либо выбором кнопок в
  диалогах, либо с использованием сочетания клавиш в списке: `enter` для
  открытия журнала, `control+C` для копирования файла журнала и `delete` для
  удаления файла журнала.
* Порядок сортировки в диспетчере журнала был изменён (самый последний
  журнал вверху).
* Исправлена ​​проблема при попытке открыть модуль Python с функцией
  openCodeFile.

### Версия 6.3

* Совместимость с NVDA 2024.1.

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
* A new command allow to place a marker in the log; and specific quick
  navigation commands in log reading mode allow to jump to them.
  Credit: the initial idea for this feature comes from Debug Helper add-on by Luke Davis.  
* Исправлена ошибка: Запоминание последней ошибки в некоторых случаях больше
  не терпит неудачу.
* Исправлена ошибка: Дополнение может снова инициализироваться с NVDA
  2019.2.1.
* Исправлена ошибка: Функция сохранения журнала больше не потерпит неудачу с
  журналами не-ASCII.

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
