# NVDA Dev & Test Toolbox #

* Autor: Cyrille Bougot
* Compatibilitate NVDA: 2019.2 și versiunile ulterioare
* Descărcați [versiunea stabilă][1]

Acest supliment adună diverse caracteristici pentru depanarea și testarea
NVDA.

## Funcţii

* Un dialog de repornire îmbunătățit pentru a specifica unele opțiuni
  suplimentare la repornirea NVDA.
* Various features related to logged errors.
* Un explorator de proprietăți obiect.
* Script tools: an extended script description mode and a script opener.
* Comenzi care ajută la citirea și analiza log-urilor.
* Backup-uri ale log-urilor vechi
* În spațiul de lucru al consolei Python, o funcție cu ajutorul căreia se
  poate deschide codul sursă al unui obiect.
* Un script de pornire personalizat pentru consola Python
* O comandă pentru a înregistra urmărirea seriei ordonată de date a funcției
  speech.speak.
* A command to reverse translate the items of the interface.

## Commands

This add-on uses layered commands for all of the new commands it adds.  The
entry point for these commands is `NVDA+X`; thus all the commands should be
executed by `NVDA+X` followed by another single letter or gesture.  You can
list all the available layered commands pressing `NVDA+X, H`.

For the commands that you use more frequently, you can also define a direct
gesture in the input gesture dialog.

## Dialog de repornire îmbunătățit

The `NVDA+X, Q` command opens a dialog to specify some extra options before
restarting NVDA.  The options that can be specified correspond to the
[command line options][2] that can be used with `nvda.exe`, e.g. `-c` for
config path, `--disable-addons` to disable add-ons, etc.

## Features related to logged errors

### Report last logged error

Pressing `NVDA+X, E` allows to report the last error logged without needing
to open the log. A second press clears the memorized last error.

### Redați un sunet pentru erorile înregistrate

Setarea ["Redați un sunet pentru erorile înregistrate"][4] a fost introdusă
în NVDA 2021.3 și permite să specificați dacă NVDA va reda un sunet de
eroare în cazul în care este înregistrată una.

This add-on provides an additional command (`NVDA+X, shift+E`) to toggle
this setting.  You can choose:

* "Numai în versiunile de testare" (implicit) pentru ca eroarea de redare a
  NVDA să redea un sunet doar dacă versiunea curentă a NVDA este o versiune
  de testare (alfa, beta sau rulată de la sursă).
* "Yes" to enable error sounds no matter your current NVDA version.

Pentru NVDA anterior versiunii 2021.3, acest add-on oferă portarea inversă a
acestei funcționalități și posibilitatea de a o controla cu ajutorul
comenzilor de la tastatură. Cu toate acestea, caseta de bifare din panoul de
setări avansate nu este portată înapoi.

## Explorator de proprietăți obiect

Această caracteristică permite raportarea unor proprietăți ale obiectului de
navigare curent fără a deschide vizualizatorul de jurnal.

Pentru a lista proprietățile unui obiect, mutați obiectul navigator la
acesta și utilizați următoarele comenzi:

* `NVDA+X, upArrow`: Selects the previous property and reports it for the
  navigator object.
* `NVDA+X, downArrow`: Selects the next property and reports it for the
  navigator object.
* `NVDA+X, N`: Reports the currently selected property for the navigator
  object
* `NVDA+X, shift+N`: Displays the currently selected property for the
  navigator object in a browseable message

Lista proprietăților acceptate este următoarea: nume, rol, stare, valoare,
windowClassName, windowControlID, windowHandle, locație, clasa Python, clasa
Python mro.

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

### Modul extins de descriere a scriptului

The extended script description mode allows to have reported information on
scripts without description in input help mode.

When the Extended script description mode is active, the input help mode
(NVDA+1) is modified as follows.  If a script has no description, the
script's name and class are reported.  If a script has a description, its
description is reported as usual.  The gesture to activate or deactivate
this feature is `NVDA+X, D`.

Executarea unui gest legat de un script fără descriere în modul de ajutor
pentru intrări, creați și o intrare pentru acest script în dialogul de
gestionare a gesturilor. Această intrare se află într-o categorie dedicată
numită „Scripturi fără descriere (modificați pe propriul risc!)”. Acest
lucru permite adăugarea, ștergerea sau modificarea cu ușurință a gesturilor
NVDA native pentru aceste scripturi. Rețineți totuși că se intenționează
adesea ca un astfel de script să nu aibă nicio descriere pentru a împiedica
utilizatorul să modifice gestul asociat. Într-adevăr, gestul poate fi
definit pentru a se potrivi cu o tastă de comandă rapidă a aplicației. De
exemplu, scriptul script_toggleItalic de pe
NVDAObjects.window.winword.WordDocument este obligat să controleze+I și
acest lucru nu ar trebui modificat deoarece gestul este transmis aplicației
pentru a executa efectiv tasta de comandă rapidă.

### Exemplu de utilizare

Control+shift+I comută și în cursiv în Word, chiar dacă nu este raportat
nativ de NVDA. Pentru ca rezultatul control+shift+I să fie raportat de NVDA
ca control+I, ar trebui să efectuați următorii pași:

* Deschideți un document Word.
* Enable the extended script description mode with `NVDA+X, D`.
* Intrați în modul de ajutor pentru intrări cu NVDA+1.
* Apăsați control+I pentru a raporta scriptul italic pentru a fi adăugat în
  dialogul Gesturi de intrare.
* Ieșiți din modul de ajutor pentru intrări cu NVDA+1.
* Deschideți dialogul pentru gesturi de intrare.
* În categoria "Scripturi fără descriere (modificați pe propriul risc!)",
  selectați comanda "toggleItalic pe
  NVDAObjects.window.winword.WordDocument".
* Adăugați comanda rapidă control+shift+I și validați.
* If you want, exit the extended script description mode with `NVDA+X, D`.

Eroare cunoscută: un script adăugat pentru o anumită clasă este vizibil
chiar dacă managerul de gesturi este deschis într-un alt context.

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

Comenzile disponibile în modul cititor de jurnal sunt descrise mai jos.

<a id="logReaderQuickNavigationCommands"></a>
#### Comenzi de navigare rapidă

Comandă cu o singură literă similară cu tastele de navigare rapidă a modului
de navigare permit trecerea la diferite tipuri de mesaje de jurnal:

* m: orice mesaj
* e: error messages (`ERROR` and `CRITICAL`)
* w: warning messages (`WARNING`)
* f: info messages (`INFO`)
* k: markers previously [placed in the log](#logPlaceMarkers)
* g: debug warning messages (`DEBUGWARNING`)
* i: input/output messages (`IO`)
* n: input messages
* s: speech messages
* d: debug messages (`DEBUG`)

Apăsarea unei singure litere trece la următoarea apariție a acestui
mesaj. Combinarea literei cu tasta Shift trece la apariția anterioară a
acestui mesaj.

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



<a id="cititorJurnalFișierCodSursa"></a>
#### Deschideți fișierul codului sursă în editorul dvs

În jurnal, unele linii se pot referi la codul sursă:

* O linie aparținând unui traceback conține calea și linia într-un fișier,
  de exemplu:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* The header line of a logged message contains the function which has logged
  this message, e.g.:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* The content of a message logged in input help mode (logged at info level):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Poate doriți să deschideți fișierul care conține acest cod pentru a înțelege
contextul urmăririi sau al mesajului înregistrat. Apăsați tasta C pentru a
deschide acest fișier.

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source, the [location of NVDA source
code](#settingsNvdaSourcePath) should also have been configured.

<a id="backupJurnaleVechi"></a>
## Backup al jurnalelor vechi

NVDA oferă deja un backup a jurnalului sesiunii anterioare a NVDA; fișierul
se numește `nvda-old.log`. Uneori, totuși, poate doriți să accesați
jurnalele mai vechi, de ex. pentru că a trebuit să reporniți NVDA din nou
înainte să vă uitați la `nvda-old.log`. Acest program de completare vă
permite să configurați dacă doriți să faceți backup pentru jurnalele vechi
și câte dintre ele; acest lucru se face în [setările
suplimentului](#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs and perform various actions on the selected log:

* open it (press `Enter`)
* delete it (press `Delete`)
* copy the log file (press `control+C`)

You can also select multiple logs to perform an actions on all of them.

To be able to open a log, you should first have configured the [Command to
open a file in your favorite editor](#settingsOpenCommand).

## Extensia consolei Python

<a id="pythonConsoleDeschidețiFișierulSursă"></a>
### Funcția `openCodeFile`

În consolă, puteți apela următoarea funcție pentru a vizualiza codul sursă care definește variabila `myVar`:
`openCodeFile(myVar)`  

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source, the [location of NVDA source
code](#settingsNvdaSourcePath) should also have been configured.

Funcțiile `openCodeFile` pot fi apelate pe obiecte definite în codul NVDA
sau pe obiecte definite de suplimente. Nu poate fi apelat pe obiecte al
căror cod sursă nu este disponibil, cum ar fi modulele integrate Python.

Dacă nu ați importat încă obiectul în consolă, puteți, de asemenea, să
transmiteți numele acestuia ca parametru funcției `openCodeFile`.

Mai jos sunt exemple de apel în codul NVDA:

* Vedeți definiția funcției `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`  
  sau cu numele trecut ca parametru:  
  `openCodeFile("speech.speech.speak")`  
* View the definition of the class `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`  
* View the definition of the method `copyToClipboard` of the class
  `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* View the definition of the class of the focused object:
  `openCodeFile(focus)`  
* Open the file `api.py` defining the module `api`:
  `openCodeFile(api)`  

### Scriptul de pornire al consolei Python

Puteți defini un script personalizat care va fi executat în spațiul de nume
al consolei Python atunci când este deschis pentru prima dată sau dacă
suplimentul este reîncărcat (NVDA+F3) după ce consola a fost deja deschisă.

De exemplu, scriptul vă permite să executați noi importuri și să definiți aliasuri pe care le veți putea folosi direct în consolă, după cum se arată mai jos:

    # Various import that I want in the console.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

Scriptul consolei Python ar trebui să fie plasat în următoarea locație: `pathToNVDAConfig\ndtt\consoleStartup.py`
De exemplu:
`C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Înregistrează urmărirea seriei ordonate a funcţiei de vorbire

Sometimes, you may want to see which part of the code is responsible for
speaking something.  For this, you can enable the stack trace logging of the
speech function pressing `NVDA+X, S`.  Each time NVDA speaks, a
corresponding stack trace will be logged in the log.

Notă: Puteți modifica fișierul scriptului direct pentru a corecta o altă
funcție. Consultați toate instrucțiunile din fișier pentru detalii despre
utilizare.

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

<a id="setări
## Setări

Unele caracteristici ale suplimentului pot necesita o configurație specifică.
Un panou de setări vă permite să le activați sau să controlați modul în care funcționează.
Pentru a vizualiza și modifica aceste setări, accesați meniul NVDA -> Preferințe și selectați categoria NVDA Dev & Test Toolbox.
Acest dialog de setări poate fi accesat și direct din dialogul Manager jurnal.

These settings are global and can only be configured when the default
profile is active.

<a id="comandăDeschidereSetări
### Comanda pentru a deschide un fișier în editorul tău preferat

Some features allow to see content in your favorite editor.  This includes
the commands to view the source file [from a log](#logReaderOpenSourceFile),
[from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed
gesture](#scriptOpener), as well as the [log manager](#oldLogsBackup)'s Open
button.

Pentru a le folosi, mai întâi trebuie să configurați comanda care va fi apelată pentru a deschide fișierul în editorul dvs. preferat.
Comanda ar trebui să fie de forma:
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
Desigur, ar trebui să modificați această linie în funcție de numele real și locația editorului dvs. și de sintaxa folosită de acesta pentru a deschide fișierele.
`{path}` va fi înlocuit cu calea completă a fișierului de deschis și `{line}` cu numărul liniei în care doriți să fie setat cursorul.
Pentru Notepad++, de exemplu, comanda de tastat în consolă ar fi:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="setăriNVDACodSursă"></a>
### Locaţia codului sursă NVDA

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\pathExample\GIT\nvda\source`  
Desigur, înlocuiți locaţia sursei NVDA cu cea corectă.

Asigurați-vă totuși că versiunea fișierului sursă (de exemplu, GIT commit)
este aceeași cu cea a instanței care rulează NVDA.

<a id="setăriBackupJurnal"></a>
### Backup al jurnalelor vechi

Caseta combinată Backup jurnale vechi permite activarea sau dezactivarea
[funcției](#oldLogsBackup). Dacă este activat, puteți specifica mai jos în
"imitați numărul de back-up-uri numărul maxim de backup-uri de siguranţă pe
care doriți să le păstrați. Aceste setări au efect numai la următoarea
pornire a NVDA, când are loc backup-ul.

<a id="settingsCopyReverseTranslation"></a>
### Copy reverse translation to clipboard

This option allows to choose if the [reverse translation
command](#reverseTranslationCommand) also copies its result to the
clipboard.

## Noutăţi

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

### Versiunea 4.0

* Posibilitatea de a face backup-uri pentru jurnalele vechi și introducerea
  unui manager de jurnale.
* S-a adăugat un script care raportează ultima eroare înregistrată.
* S-a remediat o eroare care împiedica citirea ultimului mesaj de jurnal în
  versiunile NVDA mai vechi.

### Versiunea 3.2

* Compatibilitate cu NVDA 2023.1.

### Versiunea3.1

* S-a remediat o eroare care apărea la solicitarea informaţiilor
  indisponibile despre un anume obiect.

### Versiunea 3.0

* Într-un jurnal, acum puteți apăsa C pe linia antetului unui mesaj pentru a
  deschide funcția/modulul care l-a emis.
* În consolă, funcția `openCodeFile` poate primi acum ca parametru obiectul
  sau un șir care conține numele acestuia.
* Caracteristică nouă: Fișierul de pornire al consolei NVDA: Dacă există,
  fișierul YourNVDAConfigFolder\ndtt\consoleStartup.py va fi executat la
  prima deschidere a consolei NVDA sau la reîncărcarea suplimentelor.
* Diverse remedieri minore pentru funcția consolei Python `openCodeFile` și
  comanda de deschidere a fișierului sursă corespunzător unei linii din
  jurnal.
* S-a rezolvat o problemă la încercarea de a raporta roluri/stări pentru
  exploratorul de obiecte în versiunea mai veche a NVDA.
* Suplimentul nu mai provoacă o problemă cu interceptorul arborelui când
  utilizați UIA în Edge.

### Versiunea 2.1

* Various bugfixes and code refactoring/cleaning to address all use cases:
  all supported versions, installed vs. run from source, etc. (contribution
  from Łukasz Golonka)
* Rewriting of the compa module (contribution from Łukasz Golonka)
* Acum dialogul de repornire poate fi deschis doar o singură dată.
* Comenzile rapide ale exploratorului de obiecte sunt acum nealocate în mod
  implicit și trebuie să fie setate de utilizator.
* Cu exploratorul de obiecte, o apăsare dublă pentru a apela scriptul care
  raportează proprietatea obiectului curent afișează acum informațiile
  raportate într-un mesaj prin care se poate naviga.

### Versiunea 2.0

* Funcție nouă: Dialog de repornire îmbunătățit pentru a specifica unele
  opțiuni suplimentare la repornirea NVDA.
* Funcție nouă: modul de descriere extinsă.
* Funcția de sunet de eroare de redare armonizată între versiunile NVDA
  înainte și după 2021.3.
* Funcție nouă: comenzile cititorului de jurnal sunt acum disponibile în
  vizualizatorul de jurnal și, opțional, în câmpurile de editare sau
  paginile web.
* Funcție nouă: În consola Python, este disponibilă o funcție "openCodeFile"
  pentru a vizualiza codul sursă al unui obiect.
* Unele funcții sunt acum dezactivate în modul securizat din motive de
  securitate.
* Raza de compatibilitate a suplimentului a fost extinsă (de la 2019.2 la
  2021.1).
* Lansările sunt acum efectuate cu acțiune GitHub în loc de appVeyor.

### Versiunea 1.0

* Lansare inițială.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
