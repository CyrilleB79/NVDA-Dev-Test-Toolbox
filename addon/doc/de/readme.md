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
* Ein erweiterter Skript-Beschreibungsmodus: Wenn der Eingabehilfe-Modus
  aktiviert ist, werden Informationen über Skripte mitgeteilt, die keine
  Beschreibung haben.
* Befehle, die das Lesen und Analysieren von Protokollen erleichtern.
* Backups älterer Protokolle
* Im Arbeitsbereich der Python-Konsole eine Funktion zum Öffnen des
  Quellcodes eines Objekts.
* Ein benutzerdefiniertes Start-Script für die Python-Konsole
* Ein Befehl zur Protokollierung des Stacktrace der Funktion speech.speak.

## Erweitertes Dialogfeld zum Neustarten

Der Befehl NVDA+Umschalt+Q öffnet einen Dialog, in dem Sie einige
zusätzliche Optionen angeben können, bevor Sie NVDA neu starten.  Die
Optionen, die angegeben werden können, entsprechen den
[Kommandozeilenoptionen][2], die mit `nvda.exe` verwendet werden können,
z. B. `-c` für den Konfigurationspfad, `--disable-addons` zum Deaktivieren
von NVDA-Erweiterungen, etc.

## Features im Zusammenhang mit protokollierten Fehlern

### Zuletzt protokollierten Fehler mitteilen

Mit der Tastenkombination NVDA+Umschalt+Alt+E können Sie den zuletzt
gespeicherten Fehler abrufen, ohne das Protokoll öffnen zu müssen. Ein
zweiter Druck löscht den zuletzt gespeicherten Fehler.

### Einen Sound bei protokollierten Fehlern wiedergeben

Die Einstellung ["Einen Sound bei protokollierten Fehlern wiedergeben"][4]
wurde in NVDA 2021.3 eingeführt und legt fest, ob NVDA einen Fehlerton
wiedergeben soll, wenn ein Fehler protokolliert wird.

Diese NVDA-Erweiterung richtet einen zusätzlichen Befehl  ein
(NVDA+Strg+Alt+E), um diese Einstellung umzuschalten.  Sie können auswählen
zwischen:

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

* Wählt die vorherige Eigenschaft aus und teilt sie dem Navigator-Objekt
  mit.
* Wählt die nächste Eigenschaft aus und teilt sie dem Navigator-Objekt mit.
* Teilt die aktuell ausgewählte Eigenschaft für das Navigator-Objekt mit;
  zweimaliges Drücken zeigt diese Information in einem lesbaren
  Meldungs-Fenster an.

Diese drei Befehle sind standardmäßig nicht zugewiesen; Sie müssten ihnen im
Dialogfeld für die Tastenbefehle zuweisen, um sie verwenden zu können.

Folgende Liste der unterstützten Eigenschaften: name, role, state, value,
windowClassName, windowControlID, windowHandle, location, Python class,
Python class mro.

Diese Funktion ist eine Verbesserung eines Beispiels im
[NVDA-Entwicklerhandbuch][5].


## Erweiterter Skript-Beschreibungsmodus

Wenn der Modus für die erweiterte Skript-Beschreibung aktiv ist, wird der
Eingabehilfemodus (NVDA+1) wie folgt geändert.  Wenn ein Skript keine
Beschreibung hat, werden der Name und die Klasse des Skripts mitgeteilt.
Wenn ein Skript eine Beschreibung hat, wird die Beschreibung wie üblich
angezeigt. Der Tastenbefehl zum Aktivieren oder Deaktivieren dieser Funktion
ist NVDA+Strg+Alt+D.

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
* Aktivieren Sie den erweiterten Skript-Beschreibungsmodus mit
  NVDA+Strg+Alt+D.
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
* Bei Bedarf können Sie den erweiterten Skript-Beschreibungsmodus mit
  NVDA+Strg+Alt+D beenden.

Bekannter Fehler: Ein für eine bestimmte Klasse hinzugefügtes Skript ist
auch dann sichtbar, wenn das Dialogfeld für die Tastenbefehle in einem
anderen Kontext geöffnet wird.

## Features zum Lesen und Analysieren von Protokollen

<a id="logPlaceMarkers"></a>
### Lesezeichen im Protokoll setzen

Beim Testen oder während des Arbeitens möchten Sie vielleicht einen bestimmten Bereich im Protokoll markieren, so dass Sie ihn später beim Lesen leicht wiederfinden.
Drücken Sie die Tastenkombination NVDA+Strg+K, um ein Lesezeichen im Protokoll einzufügen.
Eine Meldung wie die Folgende wird im Level INFO protokolliert:
`-- NDTT-Lesezeichen 0 --`
Sie können beliebig viele Lesezeichen im Protokoll verwenden. Die Nummer des
Lesezeichens wird jedes Mal hochgezählt, sobald ein Lesezeichen gesetzt
wird; die Nummerierung wird nur beim Neustart von NVDA zurückgesetzt.

### Der Protokoll-Lesemodus

Der Protokoll-Lesemodus erleichtert mittels Befehle das Lesen und
Analysieren von Protokollen. Im Fenster des Protokoll-Betrachters ist der
Modus standardmäßig aktiviert, sodass die Befehle zum Lesen des Protokolls
sofort verfügbar sind. In einem anderen Textlesebereich wie einem Editor
(z. B. Notepad++) oder einer Webseite (z. B. Meldung eines Problems über
GitHub) müssen Sie NVDA+Strg+Alt+L drücken, um den Protokoll-Lesemodus zu
aktivieren, um die Befehle verwenden zu können. Wenn Sie mit dem Lesen und
Analysieren von Protokollen fertig sind, können Sie mit NVDA+Strg+Alt+L ihn
wieder deaktivieren, um den Protokoll-Lesemodus auszuschalten.

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
* Drücken Sie den Buchstaben T, um die automatische Sprach-Übersetzung im
  Protokoll zu aktivieren.
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

Sicherlich möchten Sie die Datei mit diesem Code öffnen, um den Kontext des
Tracebacks oder der protokollierten Meldung einzusehen. Drücken Sie einfach
den Buchstaben C, um diese Datei zu öffnen.

Damit diese Funktion funktioniert, müssen Sie den [bevorzugten
Editor-Befehl](#settingsOpenCommand) in den Einstellungen der
NVDA-Erweiterung konfiguriert haben.  Wenn Sie NVDA nicht aus dem Quellcode
ausführen, sollte der [Speicherort des
NVDA-Quellcodes](#settingsNvdaSourcePath) ebenfalls festgelegt worden sein.

<a id="oldLogsBackup"></a>
## Backup älterer Protokolle

NVDA bietet bereits eine Sicherungskopie des Protokolls der letzten
NVDA-Sitzung an; die Datei heißt `nvda-old.log`. Manchmal möchten Sie jedoch
auf ältere Protokolle zugreifen, z. B. weil Sie NVDA neu starten mussten,
bevor Sie die Datei `nvda-old.log` einsehen konnten. Mit dieser
NVDA-Erweiterung können Sie konfigurieren, ob und wie viele alte Protokolle
Sie sichern wollen; dies geschieht in den [Einstellungen der
NVDA-Erweiterung](#settingsLogsBackup).

Mit dem Dialogfeld für die Protokollverwaltung können Sie die gespeicherten Protokolldateien einsehen.
Zu finden über das NVDA-Menü -> Werkzeuge -> Protokollverwaltung geöffnet werden.
In diesem Dialogfeld können Sie die Liste aller gespeicherten Protokolle einsehen, sie öffnen oder löschen.
Um ein Protokoll öffnen zu können, sollten Sie zunächst den [Befehl zum Öffnen einer Datei im bevorzugten Editor](#settingsOpenCommand) konfiguriert haben.

## Erweiterte Python-Konsole

<a id="pythonConsoleOpenCodeFile"></a>
### `openCodeFile`-Funktion

In der Konsole können Sie die folgende Funktion aufrufen, um den Quellcode anzuzeigen, der die Variable `myVar` definiert:
`openCodeFile(myVar)`  

Damit diese Funktion funktioniert, müssen Sie den [bevorzugten
Editor-Befehl](#settingsOpenCommand) in den Einstellungen der
NVDA-Erweiterung konfiguriert haben.  Wenn Sie NVDA nicht aus dem Quellcode
ausführen, sollte der [Speicherort des
NVDA-Quellcodes](#settingsNvdaSourcePath) ebenfalls festgelegt worden sein.

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

Manchmal möchten Sie vielleicht sehen, welcher Teil des Codes für die
Sprachausgabe verantwortlich ist. Zu diesem Zweck können Sie die
Stack-Trace-Protokollierung der Sprachausgaben-Funktion aktivieren, indem
Sie NVDA+Strg+Alt+S drücken. Jedes Mal, wenn NVDA spricht, wird ein
entsprechender Stack-Trace im Protokoll aufgezeichnet.

Hinweis: Sie können die Datei des Skripts direkt ändern, um eine andere
Funktion zu patchen.  Siehe alle Anweisungen in der Datei für Details zur
Verwendung.

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

Mit einigen Funktionen können Sie den Inhalt im bevorzugten Editor
einsehen. Dazu gehören die Befehle zum Anzeigen der Quelldatei [aus einem
Protokoll](#logReaderOpenSourceFile) oder [aus einem Objekt in der
Konsole](#pythonConsoleOpenCodeFile) sowie die Schaltfläche zum Öffnen der
[Protokollverwaltung](#oldLogsBackup).

Um sie zu verwenden, müssen Sie zunächst den Befehl konfigurieren, der aufgerufen wird, um die Datei im bevorzugten Editor zu öffnen.
Der Befehl sollte die folgende Form haben:
`"C:\<Pfad>\Editor.exe" "{path}":{line}`  
Sie sollten diese Zeile natürlich entsprechend dem tatsächlichen Namen und Ort des Editors und der von ihm zum Öffnen von Dateien verwendeten Syntax ändern.
Der Pfad `{path}` wird durch den vollständigen Pfad der zu öffnenden Datei und die Zeile `{line}` durch die zu fokussierende Zeilennummer ersetzt.
Bei Notepad++ wäre der Befehl, der in die Konsole eingegeben werden muss, beispielsweise Folgender:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### NVDA-Quellcode-Pfad

Wenn Sie einen Befehl zum [Anzeigen der Quelldatei aus einem Protokoll](#logReaderOpenSourceFile) oder [aus einem Objekt in der Konsole](#pythonConsoleOpenCodeFile) verwenden, kann die Datei zu NVDA selbst gehören.
Wenn Sie NVDA nicht aus dem Quellcode ausführen, enthält NVDA nur die kompilierte Dateien.
Daher können Sie hier einen alternativen Ort angeben, an dem die entsprechende Quelldatei zu finden ist, z. B. den Ort, an dem Sie NVDA-Quelldateien geklont haben, so dass eine Quelldatei trotzdem geöffnet werden kann.
Der Pfad sollte wie folgt lauten:
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

## Änderungsprotokoll

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

* Bubfix: The memorization of the last error do not fail anymore in some
  cases.
* Bugfix: The add-on can initialize again with NVDA 2019.2.1.
* Bugfix: Log saving feature will not fail anymore with non-ASCII logs.

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
https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#toc22
