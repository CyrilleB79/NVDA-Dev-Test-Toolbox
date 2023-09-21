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
* Un mod extins de descriere a scriptului: când este activat, modul Ajutor
  pentru intrări raportează informații despre scripturile care nu au
  descriere.
* Comenzi care ajută la citirea și analiza log-urilor.
* Backup-uri ale log-urilor vechi
* În spațiul de lucru al consolei Python, o funcție cu ajutorul căreia se
  poate deschide codul sursă al unui obiect.
* Un script de pornire personalizat pentru consola Python
* O comandă pentru a înregistra urmărirea seriei ordonată de date a funcției
  speech.speak.

## Dialog de repornire îmbunătățit

Comanda NVDA+shift+Q deschide un dialog pentru a specifica unele opțiuni
suplimentare înainte de a reporni NVDA. Opțiunile care pot fi specificate
corespund [opțiunilor liniei de comandă][2] care pot fi utilizate cu
`nvda.exe`, de ex. `-c` pentru calea de configurare,
`--suplimente-dezactivate` pentru a dezactiva suplimentele, etc.

## Features related to logged errors

### Report last logged error

Pressing NVDA+shift+alt+E allows to report the last error logged without
needing to open the log. A second press clears the memorized last error.

### Redați un sunet pentru erorile înregistrate

Setarea ["Redați un sunet pentru erorile înregistrate"][4] a fost introdusă
în NVDA 2021.3 și permite să specificați dacă NVDA va reda un sunet de
eroare în cazul în care este înregistrată una.

Acest supliment oferă o comandă suplimentară (NVDA+control+alt+E) pentru a
comuta această setare. Puteţi alege:

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

* Selectează proprietatea anterioară și o raportează pentru obiectul
  navigator.
* Selectează următoarea proprietate și o raportează pentru obiectul
  navigator.
* Raportează proprietatea selectată pentru obiectul navigator; două apăsări
  afișează aceste informații într-un mesaj prin care se poate naviga.

These three commands are unassigned by default; you will have to assign them
a shortcut in the Input gesture dialog to use them.

Lista proprietăților acceptate este următoarea: nume, rol, stare, valoare,
windowClassName, windowControlID, windowHandle, locație, clasa Python, clasa
Python mro.

Această caracteristică este o îmbunătățire a unui exemplu din [Ghidul
dezvoltatorului NVDA][5].


## Modul extins de descriere a scriptului

Când modul de descriere extinsă a scriptului este activ, modul de ajutor
pentru intrare (NVDA+1) este modificat după cum urmează. Dacă un script nu
are descriere, sunt raportate numele și clasa scriptului. Dacă un script are
o descriere, descrierea acestuia este raportată ca de obicei. Gestul de
activare sau dezactivare a acestei funcții este NVDA+control+alt+D.

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
* Activați modul de descriere extinsă a scriptului cu NVDA+control+alt+D.
* Intrați în modul de ajutor pentru intrări cu NVDA+1.
* Apăsați control+I pentru a raporta scriptul italic pentru a fi adăugat în
  dialogul Gesturi de intrare.
* Ieșiți din modul de ajutor pentru intrări cu NVDA+1.
* Deschideți dialogul pentru gesturi de intrare.
* În categoria "Scripturi fără descriere (modificați pe propriul risc!)",
  selectați comanda "toggleItalic pe
  NVDAObjects.window.winword.WordDocument".
* Adăugați comanda rapidă control+shift+I și validați.
* Dacă doriți, ieşiţi din modul de descriere extinsă a scriptului cu
  NVDA+control+alt+D.

Eroare cunoscută: un script adăugat pentru o anumită clasă este vizibil
chiar dacă managerul de gesturi este deschis într-un alt context.

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

Un mod de citire a jurnalelor oferă comenzi pentru a ușura citirea și
analiza jurnalelor. În fereastra de vizualizare a jurnalelor, cititorul de
jurnal este activat implicit, astfel că comenzile de citire a jurnalelor
sunt disponibile imediat. Într-o altă zonă de citire a textului, cum ar fi
un editor (de exemplu, Notepad++) sau o pagină web (de exemplu, problema
GitHub), trebuie să apăsați pe NVDA+control+alt+L pentru a activa modul
cititor de jurnal și a utiliza comenzile acestuia. Când ați terminat cu
sarcinile de citire și analiză a jurnalelor, puteți dezactiva din nou
NVDA+control+alt+L pentru a dezactiva modul de citire a jurnalelor.

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

Poate doriți să deschideți fișierul care conține acest cod pentru a înțelege
contextul urmăririi sau al mesajului înregistrat. Apăsați tasta C pentru a
deschide acest fișier.

Pentru ca această caracteristică să funcționeze, trebuie să fi configurat
[comanda editorului preferat](#settingsOpenCommand) în setările
suplimentului. Dacă nu rulați NVDA din sursă, ar trebui configurat și
[locația codului sursă NVDA](#settingsNvdaSourcePath).

<a id="backupJurnaleVechi"></a>
## Backup al jurnalelor vechi

NVDA oferă deja un backup a jurnalului sesiunii anterioare a NVDA; fișierul
se numește `nvda-old.log`. Uneori, totuși, poate doriți să accesați
jurnalele mai vechi, de ex. pentru că a trebuit să reporniți NVDA din nou
înainte să vă uitați la `nvda-old.log`. Acest program de completare vă
permite să configurați dacă doriți să faceți backup pentru jurnalele vechi
și câte dintre ele; acest lucru se face în [setările
suplimentului](#settingsLogsBackup).

Un dialog de gestionare a jurnalelor permite vizualizarea jurnalelor de rezervă.
Poate fi deschis accesând meniul NVDA -> Instrumente -> Manager jurnal
În acest dialog, puteți vedea lista tuturor jurnalelor de rezervă, le puteți deschide sau șterge.
Pentru a putea deschide un jurnal, ar trebui mai întâi să fi configurat [Comandă pentru a deschide un fișier în editorul tău preferat](#settingsOpenCommand).

## Extensia consolei Python

<a id="pythonConsoleDeschidețiFișierulSursă"></a>
### Funcția `openCodeFile`

În consolă, puteți apela următoarea funcție pentru a vizualiza codul sursă care definește variabila `myVar`:
`openCodeFile(myVar)`  

Pentru ca această caracteristică să funcționeze, trebuie să fi configurat
[comanda editorului preferat](#settingsOpenCommand) în setările
suplimentului. Dacă nu rulați NVDA din sursă, ar trebui configurat și
[locația codului sursă NVDA](#settingsNvdaSourcePath).

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

Uneori, este posibil să doriți să vedeți care parte a codului este
responsabilă pentru vorbire. Pentru aceasta, puteţi activa înregistrarea
urmăririi seriei ordonate a funcţiei de vorbire apăsând
NVDA+control+alt+S. De fiecare dată când NVDA vorbește, o urmărire a seriei
ordonate corespunzătoare va fi înregistrată în jurnal.

Notă: Puteți modifica fișierul scriptului direct pentru a corecta o altă
funcție. Consultați toate instrucțiunile din fișier pentru detalii despre
utilizare.

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

Unele funcții vă permit să vedeți conținutul în editorul
dvs. preferat. Aceasta include comenzile pentru vizualizarea fișierului
sursă [din jurnal](#logReaderOpenSourceFile) sau [dintr-un obiect din
consolă](#pythonConsoleOpenCodeFile), precum și butonul Deschidere al [log
manager](#oldLogsBackup).

Pentru a le folosi, mai întâi trebuie să configurați comanda care va fi apelată pentru a deschide fișierul în editorul dvs. preferat.
Comanda ar trebui să fie de forma:
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
Desigur, ar trebui să modificați această linie în funcție de numele real și locația editorului dvs. și de sintaxa folosită de acesta pentru a deschide fișierele.
`{path}` va fi înlocuit cu calea completă a fișierului de deschis și `{line}` cu numărul liniei în care doriți să fie setat cursorul.
Pentru Notepad++, de exemplu, comanda de tastat în consolă ar fi:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="setăriNVDACodSursă"></a>
### Locaţia codului sursă NVDA

Când utilizați o comandă pentru a [vizualiza fișierul sursă dintr-un jurnal](#logReaderOpenSourceFile) sau [dintr-un obiect din consolă](#pythonConsoleOpenCodeFile), fișierul poate aparține NVDA însuși.
Dacă nu rulați NVDA din sursă, NVDA conține doar fișiere compilate.
Astfel, puteți specifica aici o locație alternativă în care va fi găsit fișierul sursă corespunzător, de ex. locul în care ați clonat fișierele sursă NVDA, astfel încât un fișier sursă poate fi oricum deschis.
Locaţia ar trebui să fie astfel:  
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

## Noutăţi

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
https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#toc22
