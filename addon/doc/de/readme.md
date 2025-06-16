# Dev & Test-Toolbox für NVDA #

* Autor: Cyrille Bougot
* NVDA-Kompatibilität: 2019.2 und neuer
* [Stabile Version herunterladen][1]

Diese NVDA-Erweiterung enthält verschiedene NVDA-Funktionen für das Debuggen
und Testen.

## Features

* Ein erweitertes Dialogfeld zum Neustarten zur Angabe einiger zusätzlicher
  Optionen beim Neustart von NVDA.
* Ein Skript zum Umschalten und ein Backport der NVDA-Funktion "Einen Sound
  bei protokollierten Fehlern wiedergeben".
* Ein Explorer für Objekt-Eigenschaften.
* Script tools: an extended script description mode and a script opener.
* Befehle, die das Lesen und Analysieren von Protokollen erleichtern.
* Backups älterer Protokolle
* Im Arbeitsbereich der Python-Konsole eine Funktion zum Öffnen des
  Quellcodes eines Objekts.
* Ein benutzerdefiniertes Start-Script für die Python-Konsole
* Ein Befehl zur Protokollierung des Stacktrace der Funktion speech.speak.
* A command to reverse translate the items of the interface.

## Commands

This add-on uses layered commands for all of the new commands it adds.  The
entry point for these commands is `NVDA+X`; thus all the commands should be
executed by `NVDA+X` followed by another single letter or gesture.  You can
list all the available layered commands pressing `NVDA+X, H`.

For the commands that you use more frequently, you can also define a direct
gesture in the input gesture dialog.

## Erweitertes Dialogfeld zum Neustarten

The `NVDA+X, Q` command opens a dialog to specify some extra options before
restarting NVDA.  The options that can be specified correspond to the
[command line options][2] that can be used with `nvda.exe`, e.g. `-c` for
config path, `--disable-addons` to disable add-ons, etc.

## Features im Zusammenhang mit protokollierten Fehlern

### Zuletzt protokollierten Fehler mitteilen

Pressing `NVDA+X, E` allows to report the last error logged without needing
to open the log. A second press clears the memorized last error.

### Einen Sound bei protokollierten Fehlern wiedergeben

Die Einstellung ["Einen Sound bei protokollierten Fehlern wiedergeben"][4]
wurde in NVDA 2021.3 eingeführt und legt fest, ob NVDA einen Fehlerton
wiedergeben soll, wenn ein Fehler protokolliert wird.

This add-on provides an additional command (`NVDA+X, shift+E`) to toggle
this setting.  You can choose:

* "Nur in Testversionen" (Standardeinstellung), damit NVDA Signaltöne bei
  Fehlern nur dann abspielt, wenn es sich bei der aktuellen NVDA-Version um
  eine Testversion (Alpha, Beta oder aus dem Quellcode) handelt.
* "Ja", um Signaltöne bei Fehlern zu aktivieren, unabhängig von Ihrer
  aktuellen NVDA-Version.

Für NVDA-Versionen vor 2021.3 bietet diese NVDA-Erweiterung den Backport
dieser Funktion und die Möglichkeit, sie mit dem Tastaturbefehl zu steuern.
Das Kontrollkästchen im Bedienfeld Erweiterte Einstellungen wird jedoch
nicht zurückportiert.

## Explorer für die Objekt-Eigenschaften

Diese Funktion ermöglicht es, einige Eigenschaften des aktuellen
Navigator-Objekts mitzuteilen, ohne den Protokoll-Betrachter zu öffnen.

Um die Objekt-Eigenschaften aufzulisten, bewegen Sie den Navigator auf das
Objekt und verwenden Sie die folgenden Befehle:

* `NVDA+X, upArrow`: Selects the previous property and reports it for the
  navigator object.
* `NVDA+X, downArrow`: Selects the next property and reports it for the
  navigator object.
* `NVDA+X, N`: Reports the currently selected property for the navigator
  object
* `NVDA+X, shift+N`: Displays the currently selected property for the
  navigator object in a browseable message

Folgende Liste der unterstützten Eigenschaften: name, role, state, value,
windowClassName, windowControlID, windowHandle, location, Python class,
Python class mro.

When using object navigation commands, you can also choose to have the
currently selected property reported instead of NVDA usual object
reporting.  A toggle command, `NVDA+X, control+N`, allows to switch between
this custom reporting of objects and NVDA usual reporting.

Zum Beispiel, können Sie die Eigenschaft "windowClassName" auswählen und die
benutzerdefinierte Objekt-Meldung aktivieren. Wenn Sie dann das
Navigationsobjekt zum nächsten oder vorherigen Objekt verschieben, erhalten
Sie den windowClassName des Objekts anstelle der üblichen Meldung.

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

### Erweiterter Skript-Beschreibungsmodus

The extended script description mode allows to have reported information on
scripts without description in input help mode.

When the Extended script description mode is active, the input help mode
(NVDA+1) is modified as follows.  If a script has no description, the
script's name and class are reported.  If a script has a description, its
description is reported as usual.  The gesture to activate or deactivate
this feature is `NVDA+X, D`.

Wenn Sie einen Tastenbefehl ausführen, die an ein Skript ohne Beschreibung
im Eingabehilfe-Modus gebunden ist, wird auch ein Eintrag für dieses Skript
im  Dialogfeld für die Tastenbefehle erstellt. Dieser Eintrag befindet sich
in einer eigenen Kategorie namens "Skripte ohne Beschreibung (Änderung auf
eigene Gefahr!)". Damit können Sie die nativen Tastenbefehle in NVDA für
diese Skripte einfach hinzufügen, löschen oder ändern. Beachten Sie jedoch,
dass es oft beabsichtigt ist, dass solche Skripte keine Beschreibung haben,
um den Benutzer daran zu hindern, den zugehörigen Tastenbefehl zu
ändern. Der Tastenbefehl kann sogar so definiert sein, dass sie einem
Tastenkürzel der Anwendung entspricht. Das Skript "script_toggleItalic on
NVDAObjects.window.winword.WordDocument" ist beispielsweise an die
Tastenkombination Strg+I festgelegt und sollte nicht verändert werden, da
der Tastenbefehl an die Anwendung übergeben wird, um die Tastenkombination
tatsächlich auszuführen.

### Anwendungsbeispiel

Die Tastenkombination Strg+Umschalt+I schaltet in Word auch die
Kursivschrift um, auch wenn sie von NVDA nicht nativ mitgeteilt wird. Damit
das Ergebnis von Strg+Umschalt+I von NVDA als Strg+I mitgeteilt wird,
sollten Sie die folgenden Schritte ausführen:

* Ein Word-Dokument öffnen.
* Enable the extended script description mode with `NVDA+X, D`.
* Starten Sie den Eingabehilfe-Modus mit NVDA+1.
* Drücken Sie die Tastenkombination Strg+I, um die kursive Schrift
  mitgeteilt zu bekommen und sie im Dialogfeld für die Tastenbefehle
  einzufügen.
* Beenden Sie den Eingabehilfe-Modus mit NVDA+1.
* Öffnen Sie das Dialogfeld für die Tastenbefehle.
* Wählen Sie in der Kategorie "Skripte ohne Beschreibung (Änderung auf
  eigene Gefahr!)" den Befehl "toggleItalic on
  NVDAObjects.window.winword.WordDocument" aus.
* Fügen Sie die Tastenkombination Strg+Umschalt+I hinzu und bestätigen Sie
  sie.
* If you want, exit the extended script description mode with `NVDA+X, D`.

Bekannter Fehler: Ein für eine bestimmte Klasse hinzugefügtes Skript ist
auch dann sichtbar, wenn das Dialogfeld für die Tastenbefehle in einem
anderen Kontext geöffnet wird.

## Features zum Lesen und Analysieren von Protokollen

<a id="logPlaceMarkers"></a>
### Lesezeichen im Protokoll setzen

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press `NVDA+X, K`.
A message as follows will be logged at INFO level:  
`-- NDTT-Lesezeichen 0 --`
Sie können beliebig viele Lesezeichen im Protokoll verwenden. Die Nummer des
Lesezeichens wird jedes Mal hochgezählt, sobald ein Lesezeichen gesetzt
wird; die Nummerierung wird nur beim Neustart von NVDA zurückgesetzt.

### Der Protokoll-Lesemodus

A log reader mode provides commands to ease log reading and analyzing.  In
the log viewer window the log reader is enabled by default, thus log reading
commands are available immediately.  In another text reading area such as an
editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press
`NVDA+X, L` to enable log reader mode and use its commands.  When you are
done with log reading and analyzing tasks, you can disable again `NVDA+X, L`
to disable the log reader mode.

Nachfolgend werden die im Protokoll-Lesemodus verfügbaren Befehle
beschrieben.

<a id="logReaderQuickNavigationCommands"></a>
#### Befehle für die Schnellnavigation

Einzelne Buchstabenbefehle, die den Schnellnavigationstasten im Lesemodus
ähneln, ermöglichen den Wechsel zu verschiedenen Arten von
Protokollmeldungen:

* m: jede Meldung
* e: Fehlermeldungen (`ERROR` und `CRITICAL`)
* w: Warnmeldungen (`WARNING`)
* f: Informationen (`INFO`)
* k: Zuvor [im Protokoll platzierte](#logPlaceMarkers) Lesezeichen
* g: Debug-Warnungen (`DEBUGWARNING`)
* i: Ein-/Ausgabe-Meldungen (`IO`)
* n: Eingabe-Meldungen
* s: Meldungen über die Sprachausgabe
* d: Debug-Meldungen (`DEBUG`)

Durch Drücken des einzelnen Buchstabens gelangen Sie zum nächsten Vorkommen
dieser Nachricht. Wenn Sie den Buchstaben mit der Umschalttaste kombinieren,
gelangen Sie zum vorherigen Vorkommen dieser Nachricht.

#### Übersetzung der Sprachausgaben-Meldungen

Es kann vielleicht vorkommen, dass Sie sich ein Protokoll, welches in einer
Fremdsprache erstellt wurde, einsehen müssen, die Sie jedoch nicht
verstehen. So wurde das Protokoll z. B. auf einem chinesischen System mit
NVDA erstellt, während Sie nur Deutsch verstehen. Wenn Sie die
NVDA-Erweiterung [Sofort-Übersetzer][3] installiert haben, können Sie es in
Verbindung mit den [Befehlen für die
Schnellnavigation](#logReaderQuickNavigationCommands) verwenden, um die
Sprachmeldungen sich übersetzen zu lassen.

* Konfigurieren Sie zunächst die Sprache in dem Sofort-Übersetzer. Die
  Ausgangssprache sollte die Sprache des Systems sein, in dem das Protokoll
  erstellt wurde (z. B. Chinesisch). Die Zielsprache sollte Ihre Sprache
  sein (z. B. Deutsch).
* Das Protokoll öffnen
* Drücken Sie T, um die automatische Übersetzung im Protokoll über die
  Sprachausgabe zu aktivieren
* Verwenden Sie die Befehle für die Schnellnavigation im Protokoll, z. B. S,
  I, etc. Wenn eine Sprachausgaben-Meldung auftaucht, wird sie in Ihre
  Sprache übersetzt (in unserem Beispiel Deutsch)

Drücken Sie ganz einfach erneut den Buchstaben T, falls Sie die Übersetzung
der Sprachausgaben-Meldungen deaktivieren möchten.



<a id="logReaderOpenSourceFile"></a>
#### Öffnen Sie die Datei mit dem Quellcode im Editor

Im Protokoll können sich einige Zeilen auf den Quellcode beziehen:

* Eine Zeile, die zu einem Traceback gehört, enthält den Pfad und die Zeile
  in einer Datei, z. B.:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`
* Die Kopfzeile einer protokollierten Meldung enthält die Funktion, die
  diese Nachricht protokolliert hat, z. B.:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`
* Der Inhalt einer im Eingabehilfe-Modus protokollierten Meldung (auf
  Info-Ebene protokolliert):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Sicherlich möchten Sie die Datei mit diesem Code öffnen, um den Kontext des
Tracebacks oder der protokollierten Meldung einzusehen. Drücken Sie einfach
den Buchstaben C, um diese Datei zu öffnen.

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source, the [location of NVDA source
code](#settingsNvdaSourcePath) should also have been configured.

<a id="oldLogsBackup"></a>
## Backup älterer Protokolle

NVDA bietet bereits eine Sicherungskopie des Protokolls der letzten
NVDA-Sitzung an; die Datei heißt `nvda-old.log`. Manchmal möchten Sie jedoch
auf ältere Protokolle zugreifen, z. B. weil Sie NVDA neu starten mussten,
bevor Sie die Datei `nvda-old.log` einsehen konnten. Mit dieser
NVDA-Erweiterung können Sie konfigurieren, ob und wie viele alte Protokolle
Sie sichern wollen; dies geschieht in den [Einstellungen der
NVDA-Erweiterung](#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs and perform various actions on the selected log:

* open it (press `Enter`)
* delete it (press `Delete`)
* copy the log file (press `control+C`)

You can also select multiple logs to perform an actions on all of them.

To be able to open a log, you should first have configured the [Command to
open a file in your favorite editor](#settingsOpenCommand).

## Erweiterte Python-Konsole

<a id="pythonConsoleOpenCodeFile"></a>
### `openCodeFile`-Funktion

In der Konsole können Sie die folgende Funktion aufrufen, um den Quellcode anzuzeigen, der die Variable `myVar` definiert:
`openCodeFile(myVar)`  

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source, the [location of NVDA source
code](#settingsNvdaSourcePath) should also have been configured.

Die Funktion `openCodeFile` kann für Objekte aufgerufen werden, die im
NVDA-Code oder in NVDA-Erweiterungen definiert sind.  Sie kann nicht für
Objekte aufgerufen werden, deren Quellcode nicht verfügbar ist, wie
z. B. Python-eigene Funktionen.

Wenn Sie das Objekt noch nicht in die Konsole importiert haben, können Sie
dessen Namen auch als Parameter an die Funktion `openCodeFile` übergeben.

Nachfolgend finden Sie Beispiele für Aufrufe im Code von NVDA:

* Zeigt die Definition der Funktion `speech.speech.speak` an:
  `openCodeFile(speech.speech.speak)`  
  oder mit dem als Parameter übergebenen Namen:
  `openCodeFile("speech.speech.speak")`  
* Sehen Sie sich die Definition der Klasse `TextInfo` an:
  `openCodeFile(textInfos.TextInfo)`  
* Sehen Sie sich die Definition der Methode `copyToClipboard` der Klasse
  `TextInfo` an:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Sehen Sie sich die Definition der Klasse des fokussierten Objekts an:
  `openCodeFile(focus)`  
* Öffnen Sie die Datei `api.py`, die das Modul `api` definiert:
  `openCodeFile(api)`  

### Skript zum Starten der Python-Konsole

Sie können ein benutzerdefiniertes Skript definieren, das im Namensraum der
Python-Konsole ausgeführt wird, wenn diese zum ersten Mal geöffnet wird,
oder wenn die NVDA-Erweiterung neu geladen wird (NVDA+F3), nachdem die
Konsole bereits geöffnet wurde.

Mit diesem Skript können Sie beispielsweise neu importierte Submodule ausführen und Aliase definieren, die Sie direkt in der Konsole verwenden können, wie unten dargestellt:  

    # Verschiedene zu importierende Module:
    import globalVars as gv
    import core
    import ui
    # Aliase
    ocf = openCodeFile

Das Python-Skript sollte an folgendem Ort abgelegt werden: `<PfadZurNVDAKonfiguration>\NDTT\consoleStartup.py`
Zum Beispiel:
`C:\Users\<Benutzername>\AppData\Roaming\NVDA\NDTT\consoleStartup.py`

## Den Stack-Trace der Sprachfunktion protokollieren

Sometimes, you may want to see which part of the code is responsible for
speaking something.  For this, you can enable the stack trace logging of the
speech function pressing `NVDA+X, S`.  Each time NVDA speaks, a
corresponding stack trace will be logged in the log.

Hinweis: Sie können die Datei des Skripts direkt ändern, um eine andere
Funktion zu patchen.  Siehe alle Anweisungen in der Datei für Details zur
Verwendung.

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
## Einstellungen

Einige Funktionen der NVDA-Erweiterung benötigen möglicherweise eine spezielle Konfiguration.
Ein Einstellungsfeld ermöglicht es, diese zu aktivieren oder ihre Funktionsweise zu steuern.
Um diese Einstellungen anzuzeigen und zu ändern, gehen Sie über das NVDA-Menü zu Einstellungen und wählen Sie die Kategorie "Dev & Test-Toolbox für NVDA" aus.
Dieser Einstellungsdialog kann auch direkt aus dem Dialogfeld für die Protokollierungsverwaltung aufgerufen werden.

Diese Einstellungen sind global und werden vom Profilwechsel nicht
beeinflusst.

<a id="settingsOpenCommand"></a>
### Befehl zum Öffnen einer Datei im bevorzugten Editor

Some features allow to see content in your favorite editor.  This includes
the commands to view the source file [from a log](#logReaderOpenSourceFile),
[from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed
gesture](#scriptOpener), as well as the [log manager](#oldLogsBackup)'s Open
button.

Um sie zu verwenden, müssen Sie zunächst den Befehl konfigurieren, der aufgerufen wird, um die Datei im bevorzugten Editor zu öffnen.
Der Befehl sollte die folgende Form haben:
`"C:\<Pfad>\Editor.exe" "{path}":{line}`  
Sie sollten diese Zeile natürlich entsprechend dem tatsächlichen Namen und Ort des Editors und der von ihm zum Öffnen von Dateien verwendeten Syntax ändern.
Der Pfad `{path}` wird durch den vollständigen Pfad der zu öffnenden Datei und die Zeile `{line}` durch die zu fokussierende Zeilennummer ersetzt.
Bei Notepad++ wäre der Befehl, der in die Konsole eingegeben werden muss, beispielsweise Folgender:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA-Quellcode-Pfad

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\<Pfad>\GIT\NVDA\source`
Ersetzen Sie natürlich den Pfad der NVDA-Quelle durch den richtigen Pfad.

Vergewissern Sie sich jedoch, dass die Version Ihrer Quelldatei
(z. B. GIT-Commit) mit der Version der laufenden NVDA-Instanz übereinstimmt.

<a id="settingsLogsBackup"></a>
### Backup älterer Protokolle

Mit dem Kombinationsfeld für die Backups ältere protokolle können Sie die
[Funktion](#oldLogsBackup) aktivieren oder deaktivieren. Wenn sie aktiviert
ist, können Sie unter "Anzahl der Backups begrenzen" die maximale Anzahl der
Backups angeben, die Sie behalten möchten.  Diese Einstellungen werden erst
beim nächsten Start von NVDA wirksam, sobald die Sicherung durchgeführt
wird.

<a id="settingsCopyReverseTranslation"></a>
### Copy reverse translation to clipboard

This option allows to choose if the [reverse translation
command](#reverseTranslationCommand) also copies its result to the
clipboard.

## Änderungsprotokoll

### Version 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.
  The existing commands have been modified accordingly.  
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

* Bei der Verwendung von Befehlen der Objekt-Navigation kann eine bestimmte
  Objekt-Eigenschaft anstelle der üblichen Objjekte in NVDA mitgeteilt
  werden.
* Im Lesemodus des Protokolls funktioniert die Taste "C" zum Öffnen einer
  Code-Datei aus dem Log nun auch bei einer Eingabehilfe-Meldung.
* Bugfix: Die NVDA-Erweiterung kann nun erfolgreich gestartet werden, wenn
  die Anzahl der zu speichernden Protokolle auf den Maximalwert gesetzt
  wird.
* Bugfix: Die Ausgabe des Startskripts der Python-Konsole verhindert nicht
  mehr den Sprung zum ersten Ergebnis in der Konsole, sobald die Befehle zur
  Ergebnisnavigation verwendet werden.
* Hinweis: Von nun an werden Updates von Lokalisierung nicht mehr im
  Änderungsprotokoll angezeigt.

### Version 5.0

* Wenn die NVDA-Erweiterung Sofort-Übersetzer installiert ist, können Sie
  die Sprachausgaben-Meldungen unter Verwendung der Befehle des
  Protokoll-Lesemodus sich übersetzen lassen.
* Im Protokoll-Lesemodus kann durch Drücken von E oder Umschalt+E nun nicht
  nur zu normalen FEHLER-Meldungen, sondern auch zu KRITISCHEN
  FEHLER-Meldungen navigiert werden.
* Es wurden neue Befehle für die Schnellnavigation im Protokoll hinzugefügt,
  um zur Eingabe und zu den Sprachausgaben-Meldungen zu gelangen.
* A new command allow to place a marker in the log; and specific quick
  navigation commands in log reading mode allow to jump to them.
  Credit: the initial idea for this feature comes from Debug Helper add-on by Luke Davis.  
* Bubfix: Die Speicherung des letzten Fehlers schlägt in einigen Fällen
  nicht mehr fehl.
* Bugfix: Die NVDA-Erweiterung kann mit NVDA 2019.2.1 wieder gestartet
  werden.
* Bugfix: Das Speichern von Protokollen schlägt bei Nicht-ASCII-Protokollen
  nicht mehr fehl.

### Version 4.2

* Ein Fehler bei älteren NVDA-Versionen vor 2021.3 wurde behoben.
* Die Formatierung des Stack-Trace-Protokolls wurde korrigiert.
* Erste Lokalisierungen.

### Version 4.1

* Es wurde ein Fehler behoben, der in einigen Situationen bei der
  Protokollierung eines Fehlers auftrat.
* Die Einstellungen der NVDA-Erweiterung können jetzt nur geändert werden,
  wenn das Standard-Profil aktiv ist, um Konfigurationsprobleme vorzubeugen.

### Version 4.0

* Möglichkeit, ältere Protokolle zu sichern und Einführung einer
  Protokollverwaltung.
* Es wurde ein Skript hinzugefügt, das den zuletzt protokollierten Fehler
  abruft.
* Es wurde ein Fehler behoben, der das Lesen der letzten Protokollmeldung in
  älteren NVDA-Versionen verhinderte.

### Version 3.2

* Kompatibel mit NVDA 2023.1.

### Version 3.1

* Es wurde ein Fehler behoben, der auftrat, wenn nicht verfügbare
  Informationen über ein Objekt angefordert wurden.

### Version 3.0

* In einem Protokoll können Sie jetzt in der Kopfzeile einer Meldung C
  drücken, um die Funktion/das Modul zu öffnen, die/der die Meldung
  ausgegeben hat.
* In der Konsole kann die Funktion `openCodeFile` jetzt als Parameter das
  Objekt oder eine Zeichenkette mit seinem Namen erhalten.
* Neue Funktion: NVDA-Konsolen-Startup-Datei: Wenn sie existiert, wird die
  Datei <Pfad_zur_NVDA_Konfiguration>\NDTT\consoleStartup.py ausgeführt,
  wenn die NVDA-Konsole zum ersten Mal geöffnet wird oder sobald
  NVDA-Erweiterungen neu geladen werden.
* Verschiedene kleinere Korrekturen für die Funktion `openCodeFile` der
  Python-Konsole und den Befehl zum Öffnen der Quelldatei, die einer Zeile
  im Log entspricht.
* Es wurde ein Problem behoben, das beim Versuch auftrat, Rollen/Status für
  den Objekt-Explorer in älteren NVDA-Versionen mitzuteilen.
* Die NVDA-Erweiterung verursacht keine Probleme mehr mit dem Tree
  Interceptor bei der UIA-Verwendung in Microsoft Edge.

### Version 2.1

* Various bugfixes and code refactoring/cleaning to address all use cases:
  all supported versions, installed vs. run from source, etc. (contribution
  from Łukasz Golonka)
* Rewriting of the compa module (contribution from Łukasz Golonka)
* Das Dialogfeld zum Neustarten von NVDA kann jetzt nur noch einmal geöffnet
  werden.
* Die Verknüpfungen für den Objekt-Explorer sind nicht mehr standardmäßig
  zugewiesen und müssen vom Benutzer zugewiesen werden.
* Mit dem Objekt-Explorer zeigt ein Doppelklick zum Aufrufen des Skripts, um
  die Eigenschaft des aktuellen Objekts zu melden, jetzt die gemeldeten
  Informationen in einer lesbaren Meldung an.

### Version 2.0

* Neue Funktion: Verbessertes Dialogfeld zum Neustarten zur Angabe einiger
  zusätzlicher Optionen beim Neustart von NVDA.
* Neue Funktion: Modus für die erweiterten Beschreibungen.
* Die Funktion zur Wiedergabe von Sounds bei Fehlern wurde zwischen den
  Versionen vor und nach 2021.3 von NVDA verbessert.
* Neue Funktion: Befehle zum Protokoll-Lesen sind jetzt im Log-Viewer und
  optional auch in Bearbeitungsfeldern oder Webseiten verfügbar.
* Neue Funktion: In der Python-Konsole ist eine Funktion `openCodeFile`
  verfügbar, um den Quellcode eines Objekts einzusehen.
* Einige Funktionen sind jetzt im geschützten Modus aus Sicherheitsgründen
  deaktiviert.
* Der Kompatibilitätsbereich der NVDA-Erweiterung wurde erweitert (von
  2019.2 auf 2021.1).
* Releases werden nun mit GitHub-Aktion statt mit appVeyor durchgeführt.

### Version 1.0

* Erstveröffentlichung.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=ndtt

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
