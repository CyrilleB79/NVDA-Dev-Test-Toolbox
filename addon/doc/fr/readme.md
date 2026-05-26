# NVDA Dev & Test Toolbox

* Auteur : Cyrille Bougot
* Compatibilité NVDA : 2019.2 et au-delà

Cette extension rassemble diverses fonctionnalités pour le débogage et les tests dans NVDA.

## Fonctionnalités

* Un dialogue de redémarrage amélioré pour spécifier des options supplémentaires lors du redémarrage de NVDA.
* Diverses fonctionnalités liées aux erreurs enregistrées.
* Un explorateur de propriétés d'objets.
* Des outils pour les scripts et le code source : un mode de description étendue des scripts et des commandes d'ouverture du code source.
* Commendes pour aider à la lecture et l'analyse du journal.
* Sauvegardes des anciens journaux
* Une commande pour anonymiser un journal
* Améliorations de la console Python telles qu'un script de démarrage personnalisé et la possibilité de conserver l'historique des entrées en mémoire après le redémarrage de NVDA.
* Dans l'espace de travail de la console Python, une fonction pour ouvrir le code source d'un objet.
* Une commande pour enregistrer les appels d'une fonction spécifique (par exemple Speech.speech.speak`), y compris sa pile d'appel.
* Une commande pour effectuer une traduction inverse des éléments de l'interface.

## Commandes

Cette extension utilise des commandes séquentielles pour toutes les nouvelles commandes qu'elle ajoute.
Le point d'entrée de ces commandes est `NVDA+Z` ; ainsi, toutes les commandes doivent être exécutées par `NVDA+Z` suivi d'une autre lettre ou geste.
Si nécessaire, vous pouvez le modifier dans la boîte de dialogue Gestes de saisie.

Dans la suite de cette documentation, nous appellerons ce geste `GesteNDTT`.
Ainsi, par exemple, `GesteNDTT, S` signifie `NVDA+Z, S`, sauf si vous avez modifié le geste par défaut.
Vous pouvez obtenir la liste de toutes les commandes séquentielles en appuyant sur `GesteNDTT, H`.

Pour les commandes que vous utilisez plus fréquemment, vous pouvez également définir un geste direct dans la boîte de dialogue Gestes de commandes.

## Dialogue de redémarrage amélioré

La commande `GesteNDTT, Q` ouvre un dialogue pour indiquer des options supplémentaires avant de redémarrer NVDA.
Les options qui peuvent être spécifiées correspondent aux [options de ligne de commande][2] qui peuvent être utilisées avec `nvda.exe`, telles que `-c` pour le chemin de configuration, `--disable-addons` pour désactiver les extensions, etc.

## Fonctionnalités liées aux erreurs enregistrées

### Annoncer la dernière erreur enregistrée

Un appui sur `GesteNDTT, E` permet d'annoncer la dernière erreur enregistrée sans avoir à ouvrir le journal.
Un deuxième appui efface la dernière erreur mémorisée.

### Jouer un son pour les erreurs journalisées

Le [paramètre "Jouer un son pour les erreurs journalisées"][4] a été introduit dans NVDA 2021.3 et vous permet de spécifier si NVDA jouera un son d'erreur dans le cas où une erreur est journalisée.

Cette extension fournit une commande supplémentaire (`GesteNDTT, maj+E`) pour basculer ce paramètre.
Vous pouvez choisir :

* "Uniquement dans les versions de test de NVDA" (par défaut) de sorte que NVDA joue les sons d'erreur uniquement si la version NVDA actuelle est une version de test (alpha, bêta ou exécuté à partir du code source).
* "Oui" pour activer les sons d'erreur quelle que soit votre version de NVDA.

Dans les versions NVDA avant la 2021.3, cette extension fournit le portage de cette fonctionnalité et la possibilité de la contrôler avec la commande clavier.
La case à cocher du panneau des paramètres avancés n'est cependant pas disponible.

## Explorateur de propriétés d'objets

Cette fonction permet d'annoncer certaines propriétés de l'objet navigateur courant sans ouvrir la visionneuse du journal.

Pour lister les propriétés d'un objet, déplacez-y le l'objet navigateur et utilisez les commandes suivantes :

* `GesteNDTT, flècheHaut` : Sélectionne la propriété précédente et l'annonce pour l'objet navigateur.
* `GesteNDTT, flècheBas` :Sélectionne la propriété suivante et l'annonce pour l'objet navigateur.
* `GesteNDTT, N` : Annonce la propriété actuellement sélectionnée pour l'objet navigateur
* `GesteNDTT, maj+N` : Affiche la propriété actuellement sélectionnée pour l'objet navigateur dans un message en mode navigation

La liste des propriétés prises en charge est la suivante :
name, role, state, value, windowClassName, windowControlID, windowHandle, location, Python class, Python class mro.

Lorsque vous utilisez les commandes de navigation par objet, vous pouvez également choisir que la propriété actuellement sélectionnée soit annoncée au lieu de l'annonce habituelle des objets de NVDA.
Une commande bascule, `GesteNDTT, contrôle+N`, permet d'alterner entre cette annonce personnalisée des objets et l'annonce habituel de NVDA.

Par exemple, vous pouvez sélectionner la propriété « windowClassName » et activer l'annonce des objets personnalisée.
Ensuite, lorsque vous déplacez l'objet navigateur vers l'objet suivant ou précédent, vous entendrez la propriété windowClassName de l'objet au lieu de l'annonce habituel.

## Outils pour les scripts et le code source

<a id="sourceCodeOpeningCommands"></a>
### Les commandes d'ouverture du code source

L'extension fournit trois commandes permettant d'ouvrir le code source.

La première commande permet d'ouvrir le code source d'un script connaissant son geste de commande.
Pour l'utiliser, appuyez sur `GesteNDTT, C` puis le geste du script dont vous souhaitez voir le code.
Par exemple, pour voir le code du script qui annonce le titre de la fenêtre au premier plan, appuyez sur `GesteNDTT, C` et ensuite `NVDA+T`.

Les deux autres commandes permettent d'ouvrir le code source depuis son chemin :

* `GesteNDTT, maj+C`, ouvre le code source dont le chemin est situé sous le curseur système.
* `GesteNDTT, contrôle+C`, ouvre le code source dont le chemin se trouve sous le curseur de revue.

Par exemple. si le curseur système ou le curseur de revue se trouve sur la ligne suivante, la commande ouvrira le fichier correspondant dans votre éditeur :  
`C:\Users\username\AppData\Roaming\nvda\addons\addonName\globalPlugins\addonName\__init__.py:48`

Pour utiliser ces commandes, vous devez avoir configuré [la ligne de commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres de l'extension.
Si vous n'exécutez pas NVDA à partir des sources, [l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également avoir été configuré.

### Mode de description étendu des scripts

Le mode de description étendu pour les scripts permet l'annonce d'informations pour les scripts qui n'ont aucune description en mode d'aide à la saisie.

Lorsque le mode de description étendu des scripts est activé, le mode d'aide à la saisie (NVDA+1) est modifié comme suit.
Si un script n'a aucune description, son nom et sa classe sont annoncés.
Si un script a une description, il est annoncé de la manière habituelle.
Le geste pour activer ou désactiver cette fonction est `GesteNDTT, D`.

L'exécution d'un geste associé à un script sans description dans le mode d'aide à la saisie crée également une entrée pour ce script via le dialogue Geste de Saisie.
Cette entrée est située dans une catégorie dédiée appelée "Scripts sans description (modifiez à vos risques et périls !)".
Cela permet de supprimer ou de modifier facilement les gestes natifs de NVDA pour ces scripts.
Gardez à l'esprit, cependant, qu'il est souvent intentionnel que ces scripts n'aient pas de description afin que l'utilisateur ne puisse pas le modifier.
Le script peut être conçu pour correspondre à un raccourci d'une application spécifique.
Par exemple, le script script_toggleItalic dans NVDAObjects.window.winword.WordDocument est assigné à contrôle+I, et ne doit pas être modifié, car le geste est transmis à l'application pour qu'elle exécute effectivement ce raccourci clavier.

#### Exemple d'utilisation

Contrôle+maj+I bascule également l'italique dans Word, même si NVDA ne l'annonce pas nativement.
Afin que le résultat par l'appui sur contrôle+maj+I soit annoncé comme contrôle+I, vous devez suivre les étapes suivantes :

* Ouvrir un document Word.
* Activer le mode de description étendu des scripts avec `GesteNDTT, D`.
* Entrer en mode d'aide à la saisie avec NVDA+1.
* Appuyer sur contrôle+I pour annoncer le script italique et l'ajouter dans le dialogue des gestes de commande.
* Quitter le mode d'aide à la saisie avec NVDA+1.
* Ouvrir le dialogue Gestes de commandes.
* Dans la catégorie "Scripts sans description (modifiez à vos risques et périls !)", sélectionnez la commande "toggleItalic dans NVDAObjects.window.winword.WordDocument".
* Ajouter le raccourci contrôle+maj+I et valider.
* Si vous le souhaitez, quittez le mode description étendu des scripts avec `GesteNDTT, D`.

Bogue connue : un script ajouté pour une classe spécifique est visible même si le dialogue Geste de Saisie est ouvert dans un autre contexte.

## Fonctionnalités de lecture et analyse du journal

<a id="logPlaceMarkers"></a>
### Placer des marqueurs dans le journal

Lorsque vous faites des tests ou travaillez, vous voudrez peut-être marquer un moment spécifique dans le journal, afin que vous puissiez y retourner facilement plus tard lorsque vous lisez le journal.
Pour ajouter un message de marqueur dans le journal, appuyez sur `GesteNDTT, K`.
Un message comme suit sera enregistré au niveau info :  
`-- NDTT marker 0 --`  

Vous pouvez ajouter autant de marqueurs que vous le souhaitez dans le journal.
Le numéro du marqueur sera incrémenté chaque fois que vous placez un marqueur dans le journal; Il ne sera réinitialisé que lorsque NVDA sera redémarré.

### Mode lecture du journal

Un mode lecture du journal fournit des commandes pour en faciliter la lecture et l'analyse.
Dans la fenêtre de la visionneuse du journal et dans la zone de sortie de la console Python, le mode lecture du journal est activé par défaut, de sorte que les commandes de lecture du journal sont immédiatement disponibles.
Dans d'autres zones de lecture de texte, tels qu'un éditeur (par exemple, Notepad ++) ou une page Web (par exemple, un ticket sur GitHub),, il est nécessaire d'appuyer sur `GesteNDTT, L` pour activer le mode lecture du journal et Utilisez ses commandes.
Lorsque vous avez terminé les tâches d'analyse et de lecture du journal, vous pouvez appuyer à nouveau sur `GesteNDTT, L` pour désactiver le mode lecture du journal.

Les commandes disponibles en mode lecture du journal sont décrites ci-après.
Dans ce mode, vous pouvez également appuyer sur `contrôle+H` pour afficher toutes les commandes disponibles.

<a id="logReaderQuickNavigationCommands"></a>
#### Commandes de navigation rapide

Des commandes de navigation par lettre, similaires à celles utilisées en mode navigation, permettent de se déplacer à différents types de messages dans le journal :

* m : n'importe quel message
* e : messages d'erreur (`ERROR` and `CRITICAL`)
* w : messages d'avertissement (`WARNING`)
* f : messages d'info (`INFO`)
* k : marqueurs précédemment [placés dans le journal](#logPlaceMarkers)
* g : messages d'avertissement de débogage (`DEBUGWARNING`)
* i : messages d'entrée/sortie (`IO`)
* n : messages d'entrée
* s : messages de parole
* b : message braille
* d : messages de débogage (`DEBUG`)

Un appui sur la lettre seule permet de se déplacer à la prochaine occurrence de ce message.
Un appui combiné de la lettre avec la touche majuscule, permet de se déplacer à l'occurrence précédente.

De plus, dans certains types de messages, vous pouvez sauter de bloc en bloc en appuyant sur `o` ou `maj+o`.
Les types de messages et les blocs associés suivants sont pris en charge :

* Dans les messages contenant des piles d'appel (traceback) par ex. messages d'erreur, la navigation par blocs vous permet de passer d'une pile d'appel à l'autre
  C'est particulièrement utile lorsque plusieurs piles d'appel sont présentes, par ex. lorsqu'une erreur est générée dans la partie "except" d'une clause try/except.
* Dans le message listant les piles des threads Python lorsqu'un freeze se produit, la navigation par blocs vous permet de passer d'une pile de threads à l'autre.
* Dans le message fournissant des informations pour développeur pour l'objet navigateur enregistré lorsque vous appuyez sur `NVDA+F1`, la navigation par bloc vous permet de passer d'un groupe de propriétés à l'autre.
  Il y a quatre groupes de propriétés : les propriétés générales, les propriétés de l'appModule, les propriétés de la fenêtre et les propriétés spécifiques à l'interface (IAccessible, UIA).

Enfin, à l'intérieur d'un bloc, vous souhaiterez peut-être passer rapidement à la première ou à la dernière ligne d'intérêt du bloc.
Utilisez `maj+L` pour accéder à la première ligne du contenu du bloc actuel qui vous intéresse, par ex. la première frame d’une pile d'appel.
Et `L` pour passer à la dernière ligne d'intérêt du contenu du bloc, par ex. dernière frame d’une pile d'appel de threads ou erreur sous une pile d'appel.

#### Traduction des messages de parole

Parfois, vous devrez peut-être consulter un journal pris sur un système dans une langue étrangère que vous ne comprenez pas.
Par exemple. Le journal a été pris sur un système / NVDA chinois, alors que vous ne comprenez que le français.
Si vous avez installé l'extension [Instant Translate][3], vous pouvez l'utiliser en conjonction avec les [commandes de navigation rapide dans le journal](#logReaderQuickNavigationCommands) pour traduire les messages vocaux.

* Configurez d'abord les langues d'Instant Translate.  
  La langue source doit être la langue du système où le journal a été pris (par exemple chinois).  
  La langue cible doit être votre langue (par exemple français).
* Ouvrez le journal
* Appuyez sur `contrôle+T` pour activer la traduction automatique de la parole dans le journal
* Utilisez les commandes de navigation rapide dans le journal, par exemple, S, I, etc. Chaque fois qu'un message de parole est rencontré, il sera annoncé dans votre langue (français dans notre exemple précédent)

Si vous souhaitez désactiver la traduction de la parole, appuyez à nouveau sur `contrôle+T`.

<a id="logReaderOpenSourceFile"></a>
#### Ouvrir le fichier source dans votre éditeur

Dans le journal, une ligne peut faire référence au code source :

* Une ligne issue d'une pile d'appel contient le chemin et la ligne dans un fichier, par exemple :  
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* La ligne d'en-tête d'un message journalisée contient la fonction qui a journalisée le message, par exemple :  
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* Le contenu d'un message enregistré en mode aide à la saisie (enregistré au niveau info) :  
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Vous pouvez ouvrir le fichier qui contient le code pour comprendre le contexte de la pile d'appel ou du message journalisé.
Appuyez sur C pour ouvrir le fichier.

Pour utiliser cette fonctionnalité, vous devez avoir configuré [la ligne de commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres de l'extension.
Si vous n'exécutez pas NVDA à partir des sources, [l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également avoir été configuré.

#### Analyser une pile d'appel

Parfois, des traces d'erreurs peuvent apparaître dans le journal, comme dans l'exemple suivant :  

    ERROR - scriptHandler.executeScript (14:47:43.426) - MainThread (15492):
    error executing script: <bound method LogContainer.script_openSourceFile of <NVDAObjects.Dynamic_LogViewerLogContainerIAccessibleRichEdit50WindowNVDAObject object at 0x34C1E510>> with gesture 'c'
    Traceback (most recent call last):
      File "scriptHandler.pyc", line 300, in executeScript
      File "C:\Users\myUserName\AppData\Roaming\nvda\addons\nvdaDevTestToolbox\globalPlugins\ndtt\logReader.py", line 603, in script_openSourceFile
        if self.openStackTraceLine(line):
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
      File "C:\Users\myUserName\AppData\Roaming\nvda\addons\nvdaDevTestToolbox\globalPlugins\ndtt\logReader.py", line 667, in openStackTraceLine
        0 / 0  # Une ligne de code erronée
        ~~^~~
    ZeroDivisionError: division by zero

Pour les frames où le code source est disponible, vous avez peut-être remarqué des marqueurs avec des caractères `^` (accent circonflexe) et `~` (tilde).
C'est la façon dont Python indique visuellement l'emplacement de l'erreur ainsi que son contexte dans une frame de pile d'appel.
Un appui sur `contrôle+E` déplace le curseur au début de l'erreur dans la ligne du code source, c'est-à-dire le texte marqué par le caractère `^` (accent circonflexe).
Un double appui sélectionne ce texte.
Un triple appui sélectionne l'erreur avec son contexte, c'est-à-dire le texte de la ligne de code source marqué par les caractères `^` (accent circonflexe) et `~` (tilde).

Veuillez noter que pour les journaux pris avec une version de NVDA antérieure à 2024.1, donc avec Python 3.7 ou version antérieure, Python n'indique l'erreur qu'avec un seul caractère `^` (accent circonflexe).
Les actions pour un double ou triple appui de cette commande deviennent donc plutôt inutile.

#### Obtenir un résumé des commandes disponibles

Pour afficher une liste de toutes les commandes disponibles en mode lecture du journal, appuyez sur `contrôle+H`.

## Anonymiser un journal

Lorsque vous signalez des problèmes, il se peut que vous ayez à fournir un journal.
Cependant, les journaux peuvent contenir des informations sensibles (noms d'utilisateurs, e-mails, etc.).
Cette extension fournit une commande pour anonymiser le contenu d'un journal.

Sélectionnez une partie du journal ou tout son contenu et appuyez sur `GesteNDTT, A`.
Le contenu du journal anonymisé sera placé dans le presse-papiers.
Vous pouvez le coller sur la sélection actuelle pour la remplacer ou n'importe où ailleurs.

Pour utiliser cette fonctionnalité, vous devez personnaliser les règles d'anonymisation utilisées par cette commande.
Le fichier permettant de configurer ces règles se trouve dans : `pathToNVDAConfig\ndtt\anonymizationRules.dic` (par exemple `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\anonymizationRules.dic`).
Vous trouverez toutes les instructions pour écrire ce fichier dans son en-tête.
Dans le cas où vous auriez corrompu votre fichier de règles d'anonymisation ou si vous avez supprimé les instructions de l'en-tête, supprimez ou renommez simplement ce fichier et une nouvelle version de ce fichier sera générée au prochain démarrage.

<a id="oldLogsBackup"></a>
## Sauvegarde des anciens journaux

NVDA fournit déjà une sauvegarde du journal de la session précédente de NVDA; le fichier s'appelle `nvda-old.log`.
Parfois, cependant, vous souhaiterez peut-être accéder à des journaux plus anciens, par ex. parce que vous avez dû redémarrer NVDA avant de regarder `nvda-old.log`.
Cette extension vous permet de configurer si vous souhaitez sauvegarder les anciens journaux et combien d'entre eux ; cela se fait dans les [paramètres de l'extension](#settingsLogsBackup).

Une boîte de dialogue Gestionnaire de journaux permet d'afficher les journaux sauvegardés.
Elle peut être ouverte en allant dans le menu NVDA -> Outils -> Gestionnaire de journaux
Dans cette boîte de dialogue, vous pouvez voir la liste de tous les journaux sauvegardés et effectuer diverses actions sur le journal sélectionné.

* l'ouvrir (appuyer sur `Entrée`)
* le supprimer (appuyer sur `suppr`)
* copier le fichier journal (appuyer sur `contrôle+C`)

Vous pouvez également sélectionner plusieurs journaux pour effectuer des actions sur tous ceux-ci.

Pour pouvoir ouvrir un log, vous devez avoir configuré la [Commande pour ouvrir un fichier dans votre éditeur préféré](#settingsOpenCommand).

## Extension de la console Python

<a id="pythonConsoleOpenCodeFile"></a>
### Fonction `openCodeFile`

Dans la console, vous pouvez appeler la fonction suivante pour voir le code source qui définit la variable `myVar`:  
`openCodeFile(myVar)`    

Pour utiliser cette fonctionnalité, vous devez avoir configuré [la ligne de commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres de l'extension.
Si vous n'exécutez pas NVDA à partir des sources, [l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également avoir été configuré.

Vous pouvez appeler la fonction `openCodeFile` sur des objets définis dans le code NVDA ou dans des objets définis par les extensions.
Vous ne pouvez pas l'appeler sur des objets dont le code source n'est pas disponible, tels que les objets natifs (builtins) de Python.

Si vous n'avez pas encore importé l'objet dans la console, vous pouvez également passer son nom en tant que paramètre à la fonction `openCodeFile`.

Vous trouverez ci-dessous des exemples d'appels au code de NVDA :

* Voir la définition de la fonction `speech.speech.speak`:  
  `openCodeFile(speech.speech.speak)`  
  ou avec le nom passé comme paramètre :  
  `openCodeFile("speech.speech.speak")`  
* Voir la définition de la classe `TextInfo` :  
  `openCodeFile(textInfos.TextInfo)`  
* Voir la définition de la méthode `copyToClipboard` de la classe `TextInfo` :  
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Voir la définition de la classe de l'objet ayant le focus :  
  `openCodeFile(focus)`  
* Ouvrir le fichier `api.py` qui définit le module `api` :  
  `openCodeFile(api)`  

### Script de démarrage de la console Python

Vous pouvez définir un script personnalisé, qui sera exécuté dans l'espace de nom de la console Python lors de sa première ouverture.

Par exemple, le script vous permet d'exécuter de nouvelles importations et de définir des alias que vous pourrez utiliser directement dans la console, comme indiqué ci-dessous :  

    # Divers import que je souhaite dans la console.
    import globalVars as gv
    import core
    import ui
    # Alias
    ocf = openCodeFile

Le script de console Python doit être placé à l'emplacement suivant : `pathToNVDAConfig\ndtt\consoleStartup.py`  
Par exemple : `C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

Remarque : en Python 2, c'est-à-dire avec NVDA 2019.2.1 ou version antérieure, seuls les scripts ASCII purs sont pris en charge ; tout autre codage tel qu'Unicode n'est pas pris en charge.

### Conserver l'historique des entrées de la console Python

Dans l'historique de la console Python, vous pouvez utiliser les flèches haut et bas pour consulter et modifier les entrées précédentes.
Cependant, la liste des entrées précédentes est effacée lorsque vous quittez NVDA.
Cette extension fournit [une option](#settingsPreserveHistory), activée par défaut, permettant de conserver l'historique des entrées de la console Python même au redémarrage de NVDA.

<a id="loggingFunctionCall"></a>
## Journaliser les appels de fonction

Parfois, vous voulez savoir quelle partie du code est responsable de l'annonce de quelque chose.
Pour cela, vous pouvez activer la journalisation des appels de fonction pour la fonction `speech.speech.speak` en appuyant sur `GesteNDTT, S`.
Chaque fois que NVDA parle, un message correspondant sera journalisé, incluant la trace de la pile d'appel, vous permettant d'identifier le code qui a causé cette sortie de parole.
Une fois que vous avez terminé, désactivez la journalisation des appels de fonction avec le même geste.

De la même manière, vous pouvez choisir de journaliser les appels des fonctions de sortie `tones.beep`, `braille.BrailleBuffer.update` ou `nvwave.playWaveFile` pour suivre l'origine d'un bip, d'une sortie braille ou d'un son (par exemple un son d'erreur d'orthographe).
La [fonction cible](#targetFunctionForCallLogSetting) peut être choisie dans les paramètres de l'extension.
Vous pouvez même journaliser la pile d'appels d'une fonction personnalisée.

Par défaut, la journalisation des appels de fonction est effectué à l'aide de la méthode `settrace` : elle utilise `sys.settrace`, `threading.settrace` et/ou `threading.settrace_all_threads` pour installer une fonction de récupération de la pile d'appel qui est invoquée lors de l'événement de retour de la fonction cible.
Alternativement, si vous n'obtenez pas de résultats satisfaisants, vous pouvez opter pour la méthode du "monkey patching" où la fonction cible (par exemple `speech.speech.speak`) est patchée.
Les deux méthodes présentent des limitations qui peuvent empêcher la journalisation des appels de fonction dans des conditions combinées spécifiques.
Par exemple, la méthode `settrace` peut ne pas fonctionner avec une version de NVDA inférieure à 2026.1, lorsque la fonction cible est exécutée à partir d'un thread non principal et que la journalisation des appels de fonction est activée après le démarrage du thread de la fonction cible.
D'un autre côté, la méthode « Monkey Patching » peut ne pas fonctionner lorsque la fonction cible est importée via une instruction "from import" (par exemple `from Tones Import Beep`).

Vous pouvez choisir la méthode utilisée pour enregistrer les appels de fonction dans [le paramètre dédié](#functionCallLogMethodSetting) ou en appuyant sur `GesteNDTT, maj+S`.

<a id="reverseTranslationCommand"></a>
## Commande de traduction inverse

De nombreux testeurs utilisent NVDA dans une autre langue que l'anglais.
Mais lorsqu'on rapporte des résultats de tests sur GitHub, la description des options modifiées ou les messages annoncés par NVDA doivent être écrits en anglais.
C'est assez frustrant et long de devoir redémarrer NVDA en anglais pour vérifier le libellé exact des options ou des messages.

Pour éviter cela, l'extension fournit deux commandes de traduction inverse permettant de traduire l'interface de NVDA telle que les messages, les labels des contrôle dans l'interface graphique, etc.

* `GesteNDTT, R` utilise la traduction gettext de NVDA pour essayer de fournir une traduction inverse de la dernière annonce vocale.
* `GesteNDTT, maj+R` utilise la traduction gettext de NVDA et de ses extensions pour essayer de fournir une traduction inverse de la dernière annonce vocale.

Plus précisément, une traduction inverse de la première chaîne de la dernière séquence de parole est fournie.

Par exemple, dans NVDA en français, si je descends sur le menu outils nommé "Outils", NVDA dira "Outils Sous-menu O". 
Si j'appelle la commande de traduction inverse juste après cela, NVDA annoncera la traduction "Tools", la traduction inverse de "Outils".

En regardant le journal après cela, nous pouvons trouver les lignes suivantes :

    IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
    Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]

Cela confirme que "Outils" était la première chaîne de la séquence de parole.

Dans le cas où la traduction inverse conduit à deux ou plusieurs résultats possibles, un menu contextuel s'ouvre et liste toutes les possibilités.

Le résultat de la traduction inverse est également copié dans le presse-papiers si l'[option correspondante](#settingScopyReverseTranslation) est activée, ce qui est la valeur par défaut.

La traduction inversée des chaînes de NVDA n'est disponible que pour la version NVDA 2022.1 ou supérieure.
Pour les versions antérieures de NVDA, seules les chaînes des extensions sont disponibles pour la traduction inverse.

De plus, dans NVDA version 2019.2.1 ou antérieure, si aucune traduction inverse n'est trouvée, une deuxième tentative est effectuée dans la première partie de la chaîne.
En effet, dans ces versions de NVDA, la séquence de parole ressemble à ceci :

    IO - speech.speak (12:39:12.684):
    Speaking [u'Outils  sous-Menu  o']

Nous pouvons voir qu'un label d'objet peut être concaténée avec un rôle, un état, un raccourci, etc.
Ainsi si la traduction inverse ne donne aucun résultat sur la chaîne entière, une seconde tentative est effectuée sur la partie de la chaîne située avant le double espace (" ").
Cependant, cela n’est pas totalement fiable puisque nous ne pouvons pas exclure qu’une chaîne contienne réellement un double espace de manière native.

<a id="settings"></a>
## Paramètres

Certaines fonctionnalités de l'extension peuvent nécessiter une configuration spécifique.
Un panneau de configuration permet de les activer ou de contrôler leur fonctionnement.
Pour afficher et modifier ces paramètres, allez dans le menu NVDA -> Préférences et sélectionnez la catégorie NVDA Dev & Test Toolbox.
Cette boîte de dialogue de paramètres est également accessible directement à partir de la boîte de dialogue Gestionnaire de journaux.

Ces paramètres sont globaux et ne peuvent être configurés que lorsque le profil par défaut est actif.

<a id="settingsOpenCommand"></a>
### Commande pour ouvrir un fichier dans votre éditeur préféré

Certaines fonctionnalités permettent de voir le contenu dans votre éditeur préféré.
Cela inclut les commandes pour afficher le fichier source [à partir d'un journal](#logReaderOpenSourceFile), [d'un objet dans la console](#pythonConsoleOpenCodeFile) ou [d'un geste exécuté](#scriptOpener), ainsi que le bouton Ouvrir du [gestionnaire de journaux](#oldLogsBackup).

Pour les utiliser, vous devez d'abord configurer la commande qui sera appelée pour ouvrir le fichier dans votre éditeur préféré.
La commande doit être de la forme :  
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
Vous devez bien sûr modifier cette ligne en fonction du vrai nom et de l'emplacement de votre éditeur et de la syntaxe utilisée par celui-ci pour ouvrir les fichiers.
`{path}` sera remplacé par le chemin complet du fichier à ouvrir et `{line}` par le numéro de ligne où vous souhaitez placer le curseur.
Pour Notepad++ par exemple la commande à taper dans la console serait :  
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Chemin du code source de NVDA

Lors de l'utilisation d'une commande pour [afficher le fichier source à partir d'un journal](#logReaderOpenSourceFile), [d'un objet dans la console](#pythonConsoleOpenCodeFile) ou [d'un geste exécuté ou d'un chemin](#scriptOpener), le fichier peut appartenir à NVDA lui-même.
Si vous n'exécutez pas NVDA à partir des sources, votre NVDA ne contient que des fichiers compilés.
Ainsi, vous pouvez spécifier ici un emplacement alternatif où le fichier source correspondant sera trouvé, par ex. l'endroit où vous avez cloné les fichiers source NVDA, afin qu'un fichier source puisse être ouvert malgré tout.
Le chemin doit être de la forme :  
`C:\exemplechemin\GIT\\nvda\source`  
Bien sûr, remplacez le chemin de la source NVDA par le chemin correct.

Assurez-vous, cependant, que la version de votre fichier source (par exemple, Git commit) est la même que celle de l'instance de NVDA en exécution.

<a id="settingsLogsBackup"></a>
### Sauvegarde des anciens journaux

La liste déroulante Sauvegarde des anciens journaux permet d'activer ou de désactiver la [fonctionnalité](#oldLogsBackup).
Si elle est activée, vous pouvez également spécifier en-dessous dans "Limiter le nombre de sauvegardes à" le nombre maximum de sauvegardes que vous souhaitez conserver.
Ces paramètres ne prennent effet qu'au prochain démarrage de NVDA lorsque la sauvegarde a lieu.

<a id="settingsCopyReverseTranslation"></a>
### Copier la traduction inverse dans le presse-papiers

Cette option permet de choisir si le résultat de la [Commande de traduction inverse](#ReverseTranslationCommand) est également copié dans le presse-papiers.

<a id="settingsPreserveHistory"></a>
### Conserver l'historique des entrées de la console après le redémarrage

Si cette case est cochée, l'historique des entrées de la console Python sera conservé au redémarrage de NVDA.
Si elle est cochée, vous pouvez également préciser en-dessous le nombre maximum d'entrées qui seront enregistrées.
Si elle n'est pas cochée, NVDA se comportera comme d'habitude, c'est à dire que l'historique de la console sera vide après le redémarrage.

<a id="targetFunctionForCallLogSetting"></a>
### Fonction cible pour la journalisation des appels de fonction

Cette liste déroulante définit la fonction dont les appels seront enregistrés lors de l'activation de la [journalisation des appels de fonction](#loggingFunctionCall).
Vous pouvez choisir la fonction parmi différentes fonctions de sortie ou opter pour l'option de fonctions personnalisées.

Si vous sélectionnez l'option fonction personnalisée, vous devrez saisir le nom complet de la fonction dont vous souhaitez enregistrer les appels.
Ce nom complet doit inclure son emplacement (package, module, classe, etc.).
Veillez à définir la fonction avec son emplacement d'origine, c'est-à-dire là où elle a été réellement définie, sinon la journalisation des appels aura moins de chances de fonctionner.
Par exemple, utilisez `speech.speech.getCurrentLanguage` qui cible la fonction définie dans `speech\speech.py`, et non `speech.getCurrentLanguage` qui cible le symbole importé dans `speech\__init__.py`.

<a id="functionCallLogMethodSetting"></a>
### Méthode de journalisation des appels de fonction

Cette liste déroulante définit la méthode utilisée pour identifier les appels de fonction lorsque la [journalisation des appels de fonction](#loggingFunctionCall) est activé.
Ce paramètre peut également être basculé en appuyant sur `GesteNDTT, maj+S`.
Lorsque cette méthode est modifiée, cela s'appliquera en premier lors de la prochaine activation du journal des appels de fonction ; c'est-à-dire qu'elle ne s'applique pas à la journalisation des appels de fonction courante si celle-ci est activée.

## Journal des modifications

### Version 10.0

* Lecture de journal : lors de la journalisation des appels de fonction, les arguments et les valeurs de retour sont désormais également enregistrés. (avec la contribution de hwf1324)
* Lecture de journal : lors de l'utilisation des commandes de navigation, certains messages ne sont plus annoncés comme tronqués ou vides.
* Lors de l'annonce de la dernière erreur, certains messages ne sont plus annoncés sans interpolation (par exemple contenant "%s").
* Correction d'erreurs avec NVDA 2019.2 : première utilisation de l'historique de la console Python, annonce des noms d'objets non-ASCII avec l'explorateur de propriétés d'objet.
* Compatibilité avec NVDA 2026.1.

### Version 9.0

* Une nouvelle commande pour ouvrir un fichier de code lorsque le curseur se trouve sur un chemin/une ligne de fichier a été ajoutée.
* La journalisation des appels de fonction (anciennement connue sous le nom de journalisation de pile) a été améliorée, offrant la possibilité de journaliser l'appel de n'importe quelle fonction et fournissant une méthode plus fiable pour identifier les appels de fonction.
* Correction d'un problème de sécurité avec la lecture de journaux ([GHSA-39pg-6xpm-mjgf](https://github.com/CyrilleB79/NVDA-Dev-Test-Toolbox/security/advisories/GHSA-39pg-6xpm-mjgf)).
* Les messages IO de bip sont désormais correctement annoncés avec NVDA 2019.2.1.
* Les commandes de lecture du journal n'échouent plus à lire certaines commandes de parole (par exemple lors de l'utilisation de l'extension Console Toolkit)
* Correction d'un problème où, en cas de plusieurs traductions inversées possibles, le dernier élément de menu était copié dans le presse-papiers, quel que soit l'élément réellement sélectionné.
* Preparation de la compatibilité pour NVDA 2026.1

### Version 8.0

* L'historique de la console Python peut désormais être conservé lors des redémarrages.
* Traduction inversée : Ajout d'une deuxième commande pour fournir une traduction inversée d'une chaîne en utilisant à la fois les traductions de NVDA et de ses extensions.
* Nouvelles commandes de lecture de journal pour passer au message de sortie braille précédent ou suivant
* Nouvelles commandes de lecture de journal pour aller au bloc précédent ou suivant dans un message, par ex. pile de threads précédente ou suivante dans un rapport watchdog de freeze, bloc de propriétés précédent ou suivant dans les informations du développeur pour l'objet navigateur, etc.
* Nouvelles commandes de lecture de journal pour aller à la première ou à la dernière ligne intéressante d'un bloc, par ex. première ou dernière frame d'une pile d'appel (traceback)
* Une nouvelle commande de lecture de journal "Aller à l'erreur" pour accéder à l'erreur dans une frame de trace de pile d'appel.
* Une nouvelle commande du mode lecture de journal pour afficher un message d'aide listant toutes les commandes disponibles lors de la lecture d'un journal.
* Le mode de lecture du journal est désormais activé par défaut dans le volet de sortie de la console Python.
* Une nouvelle commande pour anonymiser un journal
* Le script de démarrage de la console prend désormais en charge les chaînes Unicode (pour Python 3 uniquement) ; Cependant, un fichier Unicode complet peut ne pas être pris en charge.
* Le script de démarrage de la console Python ne sera désormais exécuté qu'une seule fois à l'ouverture de la console.
Un bug où ce script pouvait être exécuté plusieurs fois lors du rechargement des extensions a été corrigé.
* Amélioration de la gestion des erreurs dans le script de démarrage de la console.
* Correctif : les fichiers journaux vides créés lorsque le journal est désactivé n'échouent plus à être enregistrés en tant qu'ancien journal.
* La parole à la demande est désormais prise en charge dans les commandes séquentielles
* Amélioration de la gestion des erreurs de la commande d'ouverture de script (en cas de configuration erronée ou manquante, ou lorsqu'une plage braille est utilisée).

### Version 7.3

* Correction de bogue : il est maintenant possible dassigner un autre geste à la commande permettant d'activer les commandes séquentielles de l'extension.

### Version 7.1

* Compatibilité avec NVDA 2025.1.

### Version 7.0

* Les commandes séquentielles ont été introduites; Le point d'entrée est `NVDA+X`.  
  Les commandes existantes ont été modifiées en conséquence.  
* Une nouvelle commande (`NVDA+X, R`) pour effectuer une traduction inverse du dernier message annoncé.
* Une nouvelle commande (`NVDA+X, C`) pour ouvrir le code source du script associé au geste suivant exécuté.
* Ajout de la prise en charge de la parole à la demande.
* Le gestionnaire de journaux permet désormais plus d'actions, soit à l'aide des boutons dédiés dans la boîtes de dialogue, soit avec des raccourcis clavier dans la liste: `entrée` pour ouvrir le fichier journal,`contrôle+C` pour copier le fichier et `suppr` pour supprimer un fichier.
* L'ordre de tri dans le gestionnaire de journaux a été inversé (fichier de journal le plus récent en haut).
* Correction d'un problème lorsqu'on tente d'ouvrir un module Python avec la fonction `openCodeFile`.

### Version 6.3

* Compatibilité avec NVDA 2024.1.

### Version 6.2

* Restaure l'ouverture de la console pour NVDA < 2021.1.
* Résout des problèmes de sécurité potentiels liés à [GHSA-xg6w-23rw-39r8][5] lors de l'utilisation de l'extension avec des versions plus anciennes de NVDA.
Cependant, il est recommandé d'utiliser NVDA 2023.3.3 ou supérieur.

### Version 6.1

* L'ouverture du fichier source d'un objet situé dans le sous-module d'un package fonctionne désormais.
* Correctif : la boîte de dialogue de redémarrage améliorée peut désormais être rouverte et utilisée comme prévu après avoir été fermée. (contribution de Łukasz Golonka)

### Version 6.0

* Lors de l'utilisation des commandes de navigation par objet, une propriété spécifique des objets peut être annoncée au lieu de l'annonce des objets habituel de NVDA.
* En mode lecture du journal, la touche "C" pour ouvrir un fichier de code à partir du journal fonctionne désormais également sur un message d'aide à la saisie.
* Correctif : l'extension peut désormais démarrer avec succès lorsque le nombre de journaux à sauvegarder est défini sur sa valeur maximale.
* Correctif : la sortie du script de démarrage de la console Python n'empêche plus de passer au premier résultat dans la console lors de l'utilisation des commandes de navigation dans les résultats.
* Remarque : À partir de maintenant, les mises à jour de localisation n'apparaîtront plus dans le journal des modifications.

### Version 5.0

* Si l'extension Instant Translate est installée, il est désormais possible de traduire des messages de parole à la volée lors de l'utilisation des commandes de lecture du journal.
* Dans le Mode lecture du journal, un appui sur E ou Maj+E passe maintenant aux messages d'erreur CRITICAL ainsi qu'aux messages ERROR normaux.
* De nouvelles commandes de navigation rapide dans le journal ont été ajoutées pour passer aux messages d'entrée et de parole.
* Une nouvelle commande permet de placer un marqueur dans le journal; et des commandes de navigation rapide spécifiques en mode lecture du journal permettent de s'y rendre.  
  Crédit: L'idée initiale de cette fonctionnalité provient de l'extension Debug Helper par Luke Davis.  
* Correctif : La mémorisation de la dernière erreur n'échoue plus dans certains cas.
* Correctif : l'extension peut s'initialiser à nouveau avec NVDA 2019.2.1.
* Correctif : la fonctionnalité de sauvegarde des journaux n'échouera plus avec les journaux non-ASCII.

### Version 4.2

* Correction d'une erreur avec les versions de NVDA avant la 2021.3.
* Correction du formatage de la journalisation de la trace de pile.
* Premières traductions.

### Version 4.1

* Correction d'un bogue se produisant dans certaines situations lors de la journalisation d'une erreur.
* Les paramètres de l'extension ne peuvent désormais être modifiés que lorsque le profil par défaut est actif pour éviter les problèmes de configuration.

### Version 4.0

* Possibilité de sauvegarder les anciens journaux et introduction d'un gestionnaire de journaux.
* Ajout d'un script pour annoncer la dernière erreur enregistrée.
* Correction d'un bogue empêchant la lecture du dernier message du journal dans les anciennes versions de NVDA.

### Version 3.2

* Compatibilité avec NVDA 2023.1.

### Version 3.1

* Correction d'une erreur survenant lors de la demande d'une information non disponibles sur un objet.

### Version 3.0

* Dans un journal, vous pouvez maintenant appuyer sur C dans une ligne d'en-tête de message pour ouvrir le module ou la fonction qui l'a émis.
* Dans la console, la fonction `openCodeFile` peut désormais recevoir comme paramètre l'objet ou une chaîne contenant son nom.
* Nouvelle fonctionnalité : fichier de démarrage de la console NVDA : s'il existe, le fichier YourNVDAConfigFolder\ndtt\consoleStartup.py sera exécuté lorsque la console NVDA est ouverte pour la première fois ou lorsque les extensions sont rechargées.
* Divers correctifs mineurs pour la fonction de la console Python `openCodeFile` et la commande pour ouvrir le fichier source correspondant à une ligne du journal.
* Correction d'un problème lorsque vous essayez d'annoncer les rôles / états de l'Explorateur d'objets dans une version ancienne de NVDA.
* L'extension ne cause plus de problème avec le tree interceptor lors de l'utilisation d'UIA dans Edge.

### Version 2.1

* Divers correctifs et refactorisation et nettoyage du code pour prendre en compte tous les cas d'utilisation : toutes les versions prises en charge, installées vs. exécutées à partir du code source, etc. (contribution de Łukasz Golonka)
* Réécriture du module compa (contribution de Łukasz Golonka)
* Le dialogue de redémarrage ne peut désormais être ouvert qu'une seule fois.
* Les raccourcis de l'Explorateur d'objets ne sont désormais pas assignées par défaut et doivent être mappés par l'utilisateur.
* Avec l'Explorateur d'objets, un double appui pour appeler le script pour annoncer la propriété de l'objet courant affiche désormais les informations annoncées dans un message navigable.

### Version 2.0

* Nouvelle fonctionnalité : dialogue de redémarrage amélioré afin de spécifier des options supplémentaires lors du redémarrage de NVDA.
* Nouvelle fonctionnalité : mode de description étendu.
* Fonction pour jouer des sons d'erreur harmonisés entre les versions avant et après la version 2021.3 de NVDA.
* Nouvelle fonctionnalité : Des commandes de lecture du journal sont désormais disponibles dans la visionneuse du journal et, éventuellement, dans n'importe quelle champ d'édition et sur les pages Web.
* Nouvelle fonctionnalité : dans la console Python, une fonction `openCodeFile` est disponible pour afficher le code source d'un objet.
* Certaines fonctionnalités sont désormais désactivées en mode sécurisé pour des raisons de sécurité.
* La plage de compatibilité de l'extension a été étendue (de 2019.2 à 2021.1).
* Les versions sont désormais effectuées avec GitHub action au lieu de appVeyor.

### Version 1.0

* Première version.

[2]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]: https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]: https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
