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
* Розширений опис сценарію: якщо ввімкнено режим допомоги при введенні,
  повідомляє інформацію про сценарії, які не мають опису.
* Команди, які допомагають читати та аналізувати журнали.
* Резервні копії старих журналів
* У робочій області консолі Python — функція для відкриття вихідного коду
  об’єкта.
* Спеціальний сценарій запуску для консолі Python
* Команда для журналу відстеження функції speech.speak.

## Розширений діалог перезапуску

Команда NVDA+shift+Q відкриває діалог для встановлення додаткових параметрів
перед перезапуском NVDA. Параметри, які можна вказати, відповідають
[параметрам командного рядка][2], які можна використовувати з `nvda.exe`,
напр. `-c` для шляху конфігурації, `--disable-addons` для вимкнення додатків
тощо.

## Функції, пов’язані з зареєстрованими помилками

### Додано сценарій для повідомлення про останню зареєстровану помилку

Натискання NVDA+shift+alt+E дозволяє повідомити про останню зареєстровану
помилку без необхідності відкривати журнал. Повторне натискання видаляє
останню запам’ятовану помилку.

### Відтворення звуку під час журналювання помилок

Налаштування [«Відтворення звуку під час журналювання помилок»][4] було
представлено в NVDA 2021.3 і дозволяє вказати, чи NVDA відтворюватиме звук
помилки, якщо помилка зареєстрована.

Додаток надає ще одну команду (NVDA+control+alt+E) для перемикання цього
параметра. Можна вибрати:

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

* Вибирає попередню властивість і повідомляє її для об’єкта навігатора.
* Вибирає наступну властивість і повідомляє її для об’єкта навігатора.
* Повідомляє поточну вибрану властивість для об’єкта навігатора; два
  натискання відображають цю інформацію у повідомленні для перегляду.

Список підтримуваних властивостей такий: ім’я, роль, стан, значення,
windowClassName, windowControlID, windowHandle, місцезнаходження, клас
Python, клас Python mro.

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

## Режим розширеного опису сценарію

Коли режим розширеного опису сценарію активний, режим допомоги при введенні
(NVDA+1) змінюється наступним чином. Якщо сценарій не має опису,
повідомляється ім’я та клас сценарію. Якщо сценарій має опис, його опис
повідомляється як зазвичай. Жест для ввімкнення або вимкнення цієї функції:
NVDA+control+alt+D.

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
* Вмикає режим розширеного опису сценарію за допомогою NVDA+control+alt+D.
* Увімкніть режим допомоги при введенні за допомогою NVDA+1.
* Натисніть Control+I, щоб повідомити про курсив і додати його в діалог
  жестів.
* Вимкніть режим допомоги при введенні за допомогою NVDA+1.
* Відкрийте діалог  жестів вводу.
* У категорії «Сценарії без опису (змінюйте на свій страх і ризик!)»
  виберіть команду «toggleItalic на
  NVDAObjects.window.winword.WordDocument».
* Додайте комбінацію клавіш control+shift+I та перевірте.
* Якщо хочете, вимкніть режим розширеного опису сценарію за допомогою
  NVDA+control+alt+D.

Відома помилка: сценарій, доданий для певного класу, видимий, навіть якщо
менеджер жестів відкрито в іншому контексті.

## Log reading and analyzing features

<a id="logPlaceMarkers"></a>
### Place markers in the log

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press NVDA+control+K.
A message as follows will be logged at INFO level:  
`-- NDTT marker 0 --`  
You can add as many markers as you want in the log.  The marker's number
will be incremented each time you place a marker in the log; it will only be
reset when NVDA is restarted.

### Log reader mode

Режим читання журналу надає команди для полегшення читання та аналізу
журналу. У вікні перегляду журналу читання журналу початково ввімкнено, тому
команди читання журналу доступні негайно. В іншій області читання тексту,
наприклад у редакторі (Notepad++) або на веб-сторінці (наприклад, GitHub),
вам потрібно натиснути NVDA+control+alt+L, щоб увімкнути режим читання
журналу та використовувати його команди. Коли ви закінчите з читанням
журналу та аналізом завдань, ви можете знову натиснути NVDA+control+alt+L,
щоб вимкнути режим читання журналу.

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
  Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Ви можете відкрити файл, що містить цей код, щоб зрозуміти контекст
відстеження або зареєстрованого повідомлення. Просто натисніть C, щоб
відкрити цей файл.

Щоб ця функція працювала, вам потрібно налаштувати [улюблену команду
редактора] (#settingsOpenCommand) у налаштуваннях додатка.  Якщо ви не
запускаєте NVDA з вихідного коду, слід також налаштувати [місце розташування
вихідного коду NVDA](#settingsNvdaSourcePath).

<a id="oldLogsBackup"></a>
## Резервне копіювання старих журналів

NVDA вже надає резервну копію журналу попереднього сеансу роботи NVDA; файл
називається `nvda-old.log`.  Однак іноді вам може знадобитися доступ до
старих журналів, наприклад, якщо вам довелося перезапустити NVDA, перш ніж
переглянути `nvda-old.log`.  За допомогою цього додатка ви можете
налаштувати, чи потрібно створювати резервну копію старих журналів і скільки
їх має бути; це робиться у [налаштуваннях додатка] (#settingsLogsBackup).

Діалог менеджера журналів дозволяє переглядати резервні копії журналів.
Його можна відкрити за допомогою меню NVDA -> Інструменти -> Менеджер журналів
У цьому діалозі ви можете переглянути список усіх журналів резервного копіювання, відкрити або видалити їх.
Щоб мати змогу відкрити журнал, вам слід попередньо налаштувати [Команду для відкриття файлу у вашому улюбленому редакторі] (#settingsOpenCommand).

## Розширення консолі Python

<a id="pythonConsoleOpenCodeFile"></a>
### Функція openCodeFile

У консолі можна викликати таку функцію, щоб переглянути вихідний код, який визначає змінну `myVar`:
`openCodeFile(myVar)`

Щоб ця функція працювала, вам потрібно налаштувати [улюблену команду
редактора] (#settingsOpenCommand) у налаштуваннях додатка.  Якщо ви не
запускаєте NVDA з вихідного коду, слід також налаштувати [місце розташування
вихідного коду NVDA](#settingsNvdaSourcePath).

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

Іноді вам потрібно буде подивитися, яка частина коду відповідає за
мовлення. Для цього ви можете ввімкнути журнал відстеження функції мовлення,
натиснувши NVDA+control+alt+S. Кожного разу, коли NVDA говорить, відповідна
інформація буде записана в журналі.

Примітка. Ви можете змінити файл сценарію безпосередньо, щоб виправити іншу
функцію. Перегляньте всі інструкції у файлі, щоб дізнатися більше про
використання.

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

Деякі функції дозволяють переглядати вміст у вашому улюбленому редакторі.
До них належать команди перегляду вихідного файлу [з
журналу](#logReaderOpenSourceFile) або [з об'єкта у
консолі](#pythonConsoleOpenCodeFile), а також кнопка Відкрити [менеджер
журналів](#oldLogsBackup)

Щоб ними скористатися, спочатку потрібно налаштувати команду, яка буде викликати відкриття файлу у вашому улюбленому редакторі.
Команда повинна мати вигляд:
`"C:\path\до\мій\редактор\editor.exe" "{path}":{line}`  
Звичайно, вам слід змінити цей рядок відповідно до справжньої назви і розташування вашого редактора та синтаксису, який він використовує для відкриття файлів.
`{path}` буде замінено на повний шлях до файлу, який потрібно відкрити, а `{line}` - на номер рядка, на якому потрібно встановити курсор.
Для Notepad++, наприклад, команда для введення у консолі буде такою:  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Шлях вихідного коду NVDA

При використанні команди для [перегляду вихідного файлу з журналу] (#logReaderOpenSourceFile) або [з об'єкта у консолі] (#pythonConsoleOpenCodeFile), файл може належати самій NVDA.
Якщо ви не запускаєте NVDA з вихідного джерела, ваша NVDA містить лише скомпільовані файли.
Таким чином, ви можете вказати тут альтернативне місце, де буде знайдено відповідний вихідний файл, наприклад, місце, куди ви клонували вихідні файли NVDA, щоб вихідний файл можна було відкрити у будь-якому випадку.
Шлях має бути таким:  
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

## Журнал змін

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
  navigation commands in log reading mode allow to jump to them. Credit: the
  initial idea for this feature comes from Debug Helper add-on by Luke
  Davis.
* Bubfix: The memorization of the last error do not fail anymore in some
  cases.
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
