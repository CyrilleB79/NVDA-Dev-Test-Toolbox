# NVDA Dev & Test Toolbox #

* Auteur : Cyrille Bougot
* Compatibilité NVDA : 2019.2 et au-delà
* Télécharger [version stable][1]

Cette extension rassemble diverses fonctionnalités pour le débogage et les
tests dans NVDA.

## Fonctionnalités

* Un dialogue de redémarrage amélioré pour spécifier des options
  supplémentaires lors du redémarrage de NVDA.
* Diverses fonctionnalités liées aux erreurs enregistrées.
* Un explorateur de propriétés d'objets.
* Des outils pour les scripts : un mode de description étendue des scripts
  et une ouverture facile des scripts.
* Commendes pour aider à la lecture et l'analyse du journal.
* Sauvegardes des anciens journaux
* Dans l'espace de travail de la console Python, une fonction pour ouvrir le
  code source d'un objet.
* Un script personnalisé de démarrage pour la console Python
* Une commande pour journaliser la pile d'appels de la fonction
  speech.speak.
* Une commande pour effectuer une traduction inverse des éléments de
  l'interface.

## Commandes

Cette extension utilise des commandes séquentielles pour toutes les
nouvelles commandes qu'elle ajoute.  Le point d'entrée de ces commandes est
`NVDA+X` ; ainsi, toutes les commandes doivent être exécutées par `NVDA+X`
suivi d'une autre lettre ou geste.  Vous pouvez obtenir la liste de toutes
les commandes séquentielles en appuyant sur `NVDA+X, H`.

Pour les commandes que vous utilisez plus fréquemment, vous pouvez également
définir un geste direct dans la boîte de dialogue Gestes de commandes.

## Dialogue de redémarrage amélioré

La commande `NVDA+X, Q` ouvre un dialogue pour indiquer des options
supplémentaires avant de redémarrer NVDA. Les options qui peuvent être
spécifiées correspondent aux [options de ligne de commande][2] qui peuvent
être utilisées avec `nvda.exe`, telles que  `-c` pour le chemin de
configuration, `--disable-addons` pour désactiver les extensions, etc.

## Fonctionnalités liées aux erreurs enregistrées

### Annoncer la dernière erreur enregistrée

Un appui sur `NVDA+X, E` permet d'annoncer la dernière erreur enregistrée
sans avoir à ouvrir le journal. Un deuxième appui efface la dernière erreur
mémorisée.

### Jouer un son pour les erreurs journalisées

Le [paramètre "Jouer un son pour les erreurs journalisées"][4] a été
introduit dans NVDA 2021.3 et vous permet de spécifier si NVDA jouera un son
d'erreur dans le cas où une erreur est journalisée.

Cette extension fournit une commande supplémentaire (`NVDA+X, maj+E`) pour
basculer ce paramètre. Vous pouvez choisir :

* "Uniquement dans les versions de test de NVDA" (par défaut) de sorte que
  NVDA joue les sons d'erreur uniquement si  la version NVDA actuelle est
  une version de test (alpha, bêta ou exécuté à partir du code source).
* "Oui" pour activer les sons d'erreur quelle que soit votre version de
  NVDA.

Dans les versions NVDA avant la 2021.3, cette extension fournit le backport
de cette fonctionnalité et la possibilité de le contrôler avec la commande
clavier. La case à cocher du panneau des paramètres avancés n'est cependant
pas disponible.

## Explorateur de propriétés d'objets

Cette fonction permet d'annoncer certaines propriétés de l'objet actuel dans
le navigateur d'objet sans ouvrir la visionneuse du journal.

Pour lister les propriétés d'un objet, déplacez-y le navigateur d'objets et
utilisez les commandes suivantes :

* `NVDA+X, flècheHaut` : Sélectionne la propriété précédente et l'annonce
  pour l'objet navigateur.
* `NVDA+X, flècheBas` :Sélectionne la propriété suivante et l'annonce pour
  l'objet navigateur.
* `NVDA+X, N` : Annonce la propriété actuellement sélectionnée pour l'objet
  navigateur
* `NVDA+X, maj+N` : Affiche la propriété actuellement sélectionnée pour
  l'objet navigateur dans un message en mode navigation

La liste des propriétés prises en charge est la suivante : name, role,
state, value, windowClassName, windowControlID, windowHandle, location,
Python class, Python class mro.

Lorsque vous utilisez les commandes de navigation par objet, vous pouvez
également choisir que la propriété actuellement sélectionnée soit annoncée
au lieu de l'annonce habituelle des objets de NVDA. Une commande bascule,
`NVDA+X, contrôle+N`, permet d'alterner entre cette annonce personnalisée
des objets et l'annonce habituel de NVDA.

Par exemple, vous pouvez sélectionner la propriété « windowClassName » et
activer l'annonce des objets personnalisée. Ensuite, lorsque vous déplacez
l'objet navigateur vers l'objet suivant ou précédent, vous entendrez la
propriété windowClassName de l'objet au lieu de l'annonce habituel.

## Outils pour les scripts

<a id="scriptOpener"></a>
### La commande d'ouverture de script

La commande d'ouverture de script permet d'ouvrir le code d'un script en
connaissant son geste associé.

Pour l'utiliser, appuyez sur `NVDA+x, C` puis le geste du script dont vous
souhaitez voir le code.  Par exemple, pour voir le code du script qui
annonce le titre de la fenêtre au premier plan, appuyez sur `NVDA+X, C` et
ensuite `NVDA+T`.

Pour utiliser cette fonctionnalité, vous devez avoir configuré [la ligne de
commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres
de l'extension. Si vous n'exécutez pas NVDA à partir des sources,
[l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également
avoir été configuré.

### Mode de description étendu des scripts

Le mode de description étendu pour les scripts permet l'annonce
d'informations pour les scripts qui n'ont aucune description en mode d'aide
à la saisie.

Lorsque le mode de description étendu des scripts est activé, le mode d'aide
à la saisie (NVDA+1) est modifié comme suit. Si un script n'a aucune
description, son nom et sa classe sont annoncés. Si un script a une
description, il est annoncé de la manière habituelle. Le geste pour activer
ou désactiver cette fonction est `NVDA+X, D`.

L'exécution d'un geste associé à un script sans description dans le mode
d'aide à la saisie crée également une entrée pour ce script via le dialogue
Geste de Saisie. Cette entrée est située dans une catégorie dédiée appelée
"Scripts sans description (modifiez à vos risques et périls !)". Cela permet
de supprimer ou de modifier facilement les gestes natifs de NVDA pour ces
scripts. Gardez à l'esprit, cependant, qu'il est souvent intentionnel que
ces scripts n'aient pas de description afin que l'utilisateur ne puisse pas
le modifier. Le script peut être conçu pour correspondre à un raccourci
d'une application spécifique. Par exemple, le script script_toggleItalic
dans NVDAObjects.window.winword.WordDocument est assigné à contrôle+I, et ne
doit pas être modifié, car le geste est transmis à l'application pour
vraiment exécuter ce raccourci clavier.

### Exemple d'utilisation

Contrôle+maj+I bascule également l'italique dans Word, même si NVDA ne
l'annonce pas nativement. Afin que le résultat par l'appui sur
contrôle+maj+I soit annoncé comme contrôle+I, vous devez suivre les étapes
suivantes :

* Ouvrir un document Word.
* Activer le mode de description étendu des scripts avec `NVDA+X, D`.
* Entrer en mode d'aide à la saisie avec NVDA+1.
* Appuyer sur contrôle+I pour annoncer le script italique et l'ajouter dans
  le dialogue des gestes de commande.
* Quitter le mode d'aide à la saisie avec NVDA+1.
* Ouvrir le dialogue Gestes de commandes.
* Dans la catégorie "Scripts sans description (modifiez à vos risques et
  périls !)", Sélectionnez la commande "toggleItalic dans
  NVDAObjects.window.winword.WordDocument".
* Ajouter le raccourci contrôle+maj+I et valider.
* Si vous le souhaitez, quittez le mode description étendu des scripts avec
  `NVDA+X, D`.

Bogue connue : un script ajouté pour une classe spécifique est visible même
si le dialogue Geste de Saisie est ouvert dans un autre contexte.

## Fonctionnalités de lecture et analyse du journal

<a id="logPlaceMarkers"></a>
### Placer des marqueurs dans le journal

Lorsque vous faites des tests ou travaillez, vous voudrez peut-être marquer un moment spécifique dans le journal, afin que vous puissiez y retourner facilement plus tard lorsque vous lisez le journal.
Pour ajouter un message de marqueur dans le journal, appuyez sur `NVDA+X, K`.
Un message comme suit sera enregistré au niveau information :  
`-- NDTT marker 0 --`  
Vous pouvez ajouter autant de marqueurs que vous le souhaitez dans le
journal. Le numéro du marqueur sera incrémenté chaque fois que vous placez
un marqueur dans le journal; Il ne sera réinitialisé que lorsque NVDA sera
redémarré.

### Mode lecture du journal

Un mode lecture du journal fournit des commandes pour faciliter la lecture
et l'analyse du journal. Dans la fenêtre de la visionneuse du journal, le
mode lecture du journal est activé par défaut, de sorte que les commandes de
lecture  du journal sont immédiatement disponibles. Dans d'autres zones de
lecture de texte, tels qu'un éditeur (par exemple, Notepad ++) ou une page
Web (par exemple, un ticket sur GitHub),, il est nécessaire d'appuyer sur
`NVDA+X, L` pour activer le mode lecture du journal et Utilisez ses
commandes. Lorsque vous avez terminé les tâches d'analyse et de lecture du
journal, vous pouvez appuyer à nouveau sur `NVDA+X, L` pour désactiver le
mode lecture du journal.

Les commandes disponibles en mode lecture du journal sont décrites ci-après.

<a id="logReaderQuickNavigationCommands"></a>
#### Commandes de navigation rapide

Des commandes de navigation par lettre, similaires à celles utilisées en
mode navigation, permettent de se déplacer à différents types de messages
dans le journal :

* m : n'importe quel message
* e : messages d'erreur (`ERROR` and `CRITICAL`)
* w : messages d'avertissement (`WARNING`)
* f : messages d'info (`INFO`)
* k : marqueurs précédemment [placés dans le journal](#logPlaceMarkers)
* g : messages d'avertissement de débogage (`DEBUGWARNING`)
* i : messages d'entrée/sortie (`IO`)
* n : messages d'entrée
* s : messages de parole
* d : messages de débogage (`DEBUG`)

Un simple appui sur la lettre permet de se déplacer à la prochaine
occurrence de ce message. Un appui combiné de la lettre avec la touche
majuscule, permet de se déplacer à l'occurrence précédente.

#### Traduction des messages de parole

Parfois, vous devrez peut-être regarder un journal pris sur un système dans
une langue étrangère que vous ne comprenez pas. Par exemple. Le journal a
été pris sur un système / NVDA chinois, alors que vous ne comprenez que le
français. Si vous avez installé l'extension [Instant Translate][3], vous
pouvez l'utiliser en conjonction avec les [commandes de navigation rapide
dans le journal](#logReaderQuickNavigationCommands) pour traduire les
messages vocaux.

* Configurez d'abord les langues d'Instant Translate. La langue source doit
  être la langue du système où le journal a été pris (par exemple
  chinois). La langue cible doit être votre langue (par exemple français).
* Ouvrez le journal
* Appuyez sur T pour activer la traduction automatique de la parole dans le
  journal
* Utilisez les commandes de navigation rapide dans le journal, par exemple,
  S, I, etc. Chaque fois qu'un message de parole est rencontré, il sera
  annoncé dans votre langue (français dans notre exemple précédent)

Si vous souhaitez désactiver la traduction de la parole, appuyez à nouveau
sur T.



<a id="logReaderOpenSourceFile"></a>
#### Ouvrir le fichier source dans votre éditeur

Dans le journal, une ligne peut faire référence au code source :

* Une ligne issue d'une pile d'appel contient le chemin et la ligne dans un
  fichier, par exemple :
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`  
* La ligne d'en-tête d'un message journalisée contient la fonction qui a
  journalisée le message, par exemple :
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* Le contenu d'un message enregistré en mode aide à la saisie (enregistré au
  niveau info) :
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Vous pouvez ouvrir le fichier qui contient le code pour comprendre le
contexte de la pile d'appel ou du message journalisé. Appuyez sur C pour
ouvrir le fichier.

Pour utiliser cette fonctionnalité, vous devez avoir configuré [la ligne de
commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres
de l'extension. Si vous n'exécutez pas NVDA à partir des sources,
[l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également
avoir été configuré.

<a id="oldLogsBackup"></a>
## Sauvegarde des anciens journaux

NVDA fournit déjà une sauvegarde du journal de la session précédente de NVDA
; le fichier s'appelle `nvda-old.log`. Parfois, cependant, vous souhaiterez
peut-être accéder à des journaux plus anciens, par ex. parce que vous avez
dû redémarrer NVDA avant de regarder `nvda-old.log`. Cette extension vous
permet de configurer si vous souhaitez sauvegarder les anciens journaux et
combien d'entre eux ; cela se fait dans les [paramètres de
l'extension](#settingsLogsBackup).

Une boîte de dialogue Gestionnaire de journaux permet d'afficher les journaux sauvegardés.
Elle peut être ouverte en allant dans le menu NVDA -> Outils -> Gestionnaire de journaux
Dans cette boîte de dialogue, vous pouvez voir la liste de tous les journaux sauvegardés et effectuer diverses actions sur le journal sélectionné.

* l'ouvrir (appuyer sur `Entrée`)
* le supprimer (appuyer sur `suppr`)
* copier le fichier journal (appuyer sur `contrôle+C`)

Vous pouvez également sélectionner plusieurs journaux pour effectuer des
actions sur tous ceux-ci.

Pour pouvoir ouvrir un log, vous devez avoir configuré la [Commande pour
ouvrir un fichier dans votre éditeur préféré](#settingsOpenCommand).

## Extension de la console Python

<a id="pythonConsoleOpenCodeFile"></a>
### Fonction `openCodeFile`

Dans la console, vous pouvez appeler la fonction suivante pour voir le code source qui définit la variable `myVar`:
`openCodeFile(myVar)`  

Pour utiliser cette fonctionnalité, vous devez avoir configuré [la ligne de
commande de votre éditeur préféré](#settingsOpenCommand) dans les paramètres
de l'extension. Si vous n'exécutez pas NVDA à partir des sources,
[l'emplacement du code source NVDA](#settingsNvdaSourcePath) doit également
avoir été configuré.

Vous pouvez appeler la fonction `openCodeFile` dans des objets définis dans
le code NVDA ou dans des objets définis par les extensions. Vous ne pouvez
pas l'appeler sur des objets dont le code source n'est pas disponible, comme
les objets natifs (builtins) de Python.

Si vous n'avez pas encore importé l'objet dans la console, vous pouvez
également passer son nom en tant que paramètre à la fonction `openCodeFile`.

Vous trouverez ci-dessous des exemples d'appels au code de NVDA :

* Voir la définition de la fonction `speech.speech.speak`:  
  `openCodeFile(speech.speech.speak)`  
  ou avec le nom passé comme paramètre :  
  `openCodeFile("speech.speech.speak")`  
* Voir la définition de la classe `TextInfo` :  
  `openCodeFile(textInfos.TextInfo)`  
* Voir la définition de la méthode `copyToClipboard` de la classe
  `TextInfo` :  
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Voir la définition de la classe de l'objet ayant le focus :  
  `openCodeFile(focus)`  
* Ouvrir le fichier `api.py` qui définit le module `api` :  
  `openCodeFile(api)`  

### Script de démarrage de la console Python

Vous pouvez définir un script personnalisé, qui sera exécuté dans l'espace
de nom de la console Python lors de l'ouverture pour la première fois, ou si
l'extension est rechargée (NVDA+contrôle+F3) après avoir déjà ouvert la
console.

Par exemple, le script vous permet d'exécuter de nouvelles importations et de définir des alias que vous pourrez utiliser directement dans la console, comme indiqué ci-dessous :  

    # Divers import que je souhaite dans la console.
    import globalVars as gv
    import core
    import ui
    # Alias
    ocf = openCodeFile

Le script de console Python doit être placé à l'emplacement suivant : `pathToNVDAConfig\ndtt\consoleStartup.py`  
Par exemple :
`C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Journaliser la pile d'appels de la fonction speech

Parfois, vous voulez savoir quelle partie du code est responsable de
l'annonce de quelque chose. Pour ce faire, vous pouvez activer la
journalisation de la trace de pile d'appel de la fonction speech en appuyant
sur `NVDA+X, S`. Chaque fois que NVDA parle, une trace de la pile d'appel
sera enregistrée dans le journal.

Remarque : vous pouvez modifier directement le fichier du script pour
patcher une autre fonction. Voir toutes les instructions dans le fichier
pour plus de détails sur l'utilisation.

<a id="reverseTranslationCommand"></a>
## Commande de traduction inverse

De nombreux testeurs utilisent NVDA dans une autre langue que l'anglais.
Mais lorsqu'on rapporte des résultats de tests sur GitHub, la description
des options modifiées ou les messages annoncés par NVDA doivent être écrit
en anglais.  C'est assez frustrant et long de devoir redémarrer NVDA en
anglais pour vérifier le libellé exact des options ou des messages.

Pour éviter cela, l'extension fournit une commande de traduction inverse
(`NVDA+X, R`) permettant la traduction inverse de l'interface de NVDA,
telles que les messages, les labels des contrôles dans l'interface
graphique, etc. Cette commande utilise la traduction GetText de NVDA pour
essayer de fournir une traduction inverse de la dernière annonce.  Plus
précisément, une traduction inverse de la première chaîne de la dernière
séquence de parole est fournie.

Par exemple, dans NVDA en français, si je descends sur le menu outils nommé
"Outils", NVDA dira "Outils Sous-menu O".  Si j'appelle la commande de
traduction inverse juste après cela, NVDA annoncera la traduction "Tools",
la traduction inverse de "Outils".

En regardant le journal après cela, nous pouvons trouver les lignes
suivantes :
```
IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
Speaking ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (still valid)]
```
Cela confirme que "Outils" était la première chaîne de la séquence de
parole.

Dans le cas où la traduction inverse conduit à deux ou plusieurs résultats
possibles, un menu contextuel s'ouvre et liste toutes les possibilités.

Le résultat de la traduction inverse est également copié dans le
presse-papiers si l'[option correspondante](#settingScopyReverseTranslation)
est activée, ce qui est la valeur par défaut.

<a id="settings"></a>
## Paramètres

Certaines fonctionnalités de l'extension peuvent nécessiter une configuration spécifique.
Un panneau de configuration permet de les activer ou de contrôler leur fonctionnement.
Pour afficher et modifier ces paramètres, allez dans le menu NVDA -> Préférences et sélectionnez la catégorie NVDA Dev & Test Toolbox.
Cette boîte de dialogue de paramètres est également accessible directement à partir de la boîte de dialogue Gestionnaire de journaux.

Ces paramètres sont globaux et ne peuvent être configurés que lorsque le
profil par défaut est actif.

<a id="settingsOpenCommand"></a>
### Commande pour ouvrir un fichier dans votre éditeur préféré

Certaines fonctionnalités permettent de voir le contenu dans votre éditeur
préféré. Cela inclut les commandes pour afficher le fichier source [à partir
d'un journal](#logReaderOpenSourceFile), [d'un objet dans la
console](#pythonConsoleOpenCodeFile) ou [d'un geste exécuté](#scriptOpener),
ainsi que le bouton Ouvrir du [gestionnaire de journaux](#oldLogsBackup).

Pour les utiliser, vous devez d'abord configurer la commande qui sera appelée pour ouvrir le fichier dans votre éditeur préféré.
La commande doit être de la forme :  
`"C:\path\to\my\editor\editor.exe" "{path}":{line}`  
Vous devez bien sûr modifier cette ligne en fonction du vrai nom et de l'emplacement de votre éditeur et de la syntaxe utilisée par celui-ci pour ouvrir les fichiers.
`{path}` sera remplacé par le chemin complet du fichier à ouvrir et `{line}` par le numéro de ligne où vous souhaitez placer le curseur.
Pour Notepad++ par exemple la commande à taper dans la console serait :  
`"C:\Program Files\Notepad++
otepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Chemin du code source de NVDA

Lors de l'utilisation d'une commande pour [afficher le fichier source à partir d'un journal](#logReaderOpenSourceFile), [d'un objet dans la console](#pythonConsoleOpenCodeFile) ou [d'un geste exécuté](#scriptOpener), le fichier peut appartenir à NVDA lui-même.
Si vous n'exécutez pas NVDA à partir des sources, votre NVDA ne contient que des fichiers compilés.
Ainsi, vous pouvez spécifier ici un emplacement alternatif où le fichier source correspondant sera trouvé, par ex. l'endroit où vous avez cloné les fichiers source NVDA, afin qu'un fichier source puisse être ouvert malgré tout.
Le chemin doit être de la forme :  
`C:\exemplechemin\GIT\\nvda\source`  
Bien sûr, remplacez le chemin de la source NVDA par le chemin correct.

Assurez-vous, cependant, que la version de votre fichier source (par
exemple, Git commit) est la même que celle de l'instance de NVDA en
exécution.

<a id="settingsLogsBackup"></a>
### Sauvegarde des anciens journaux

La liste déroulante Sauvegarde des anciens journaux permet d'activer ou de
désactiver la [fonctionnalité](#oldLogsBackup). Si elle est activée, vous
pouvez également spécifier ci-dessous dans "Limiter le nombre de
sauvegardes" le nombre maximum de sauvegardes que vous souhaitez
conserver. Ces paramètres ne prennent effet qu'au prochain démarrage de NVDA
lorsque la sauvegarde a lieu.

<a id="settingsCopyReverseTranslation"></a>
### Copier la traduction inverse dans le presse-papiers

Cette option permet de choisir si le résultat de la [Commande de traduction
inverse](#ReverseTranslationCommand) est également copié dans le
presse-papiers.

## Journal des modifications

### Version 7.0

* Les commandes séquentielles ont été introduites; Le point d'entrée est
  `NVDA+X`.
  Les commandes existantes ont été modifiées en conséquence.  
* Une nouvelle commande (`NVDA+X, R`) pour effectuer une traduction inverse
  du dernier message annoncé.
* Une nouvelle commande (`NVDA+X, C`) pour ouvrir le code source du script
  associé au geste suivant exécuté.
* Ajout de la prise en charge de la parole à la demande.
* Le gestionnaire de journaux permet désormais plus d'actions, soit à l'aide
  des boutons dédiés dans la boîtes de dialogue, soit avec des raccourcis
  clavier dans la liste: `entrée` pour ouvrir le fichier
  journal,`contrôle+C` pour copier le fichier et `suppr` pour supprimer un
  fichier.
* L'ordre de tri dans le gestionnaire de journaux a été inversé (fichier de
  journal le plus récent en haut).
* Correction d'un problème lorsqu'on tente d'ouvrir un module Python avec la
  fonction `openCodeFile`.

### Version 6.3

* Compatibilité avec NVDA 2024.1.

### Version 6.2

* Restaure l'ouverture de la console pour NVDA < 2021.1.
* Résout des problèmes de sécurité potentiels liés à
  [GHSA-xg6w-23rw-39r8][5] lors de l'utilisation du module complémentaire
  avec des versions plus anciennes de NVDA. Cependant, il est recommandé
  d'utiliser NVDA 2023.3.3 ou supérieur.

### Version 6.1

* L'ouverture du fichier source d'un objet situé dans le sous-module d'un
  package fonctionne désormais.
* Correctif : la boîte de dialogue de redémarrage améliorée peut désormais
  être rouverte et utilisée comme prévu après avoir été
  fermée. (contribution de Łukasz Golonka)

### Version 6.0

* Lors de l'utilisation des commandes de navigation par objet, une propriété
  spécifique des objets peut être annoncée au lieu de l'annonce des objets
  habituel de NVDA.
* En mode lecture du journal, la touche "C" pour ouvrir un fichier de code à
  partir du journal fonctionne désormais également sur un message d'aide à
  la saisie.
* Correctif : l'extension peut désormais démarrer avec succès lorsque le
  nombre de journaux à sauvegarder est défini sur sa valeur maximale.
* Correctif : la sortie du script de démarrage de la console Python
  n'empêche plus de passer au premier résultat dans la console lors de
  l'utilisation des commandes de navigation dans les résultats.
* Remarque : À partir de maintenant, les mises à jour de localisation
  n'apparaîtront plus dans le journal des modifications.

### Version 5.0

* Si l'extension Instant Translate est installée, il est désormais possible
  de traduire des messages de parole à la volée lors de l'utilisation des
  commandes de lecture du journal.
* Pendant que vous êtes dans le Mode lecture du journal, appuyer sur E ou
  Maj+E passe maintenant aux messages d'erreur CRITICAL ainsi qu'aux
  messages ERROR normaux.
* De nouvelles commandes de navigation rapide dans le journal ont été
  ajoutées pour passer aux messages d'entrée et de parole.
* Une nouvelle commande permet de placer un marqueur dans le journal; et des
  commandes de navigation rapide spécifiques en mode lecture du journal
  permettent de s'y rendre.
  Crédit: L'idée initiale de cette fonctionnalité provient de l'extension Debug Helper par Luke Davis.  
* Correctif : La mémorisation de la dernière erreur n'échoue plus dans
  certains cas.
* Correctif : l'extension peut s'initialiser à nouveau avec NVDA 2019.2.1.
* Correctif : la fonctionnalité de sauvegarde des journaux n'échouera plus
  avec les journaux non-ASCII.

### Version 4.2

* Correction d'une erreur avec les versions de NVDA avant la 2021.3.
* Correction du formatage de la journalisation de la trace de pile.
* Premières traductions.

### Version 4.1

* Correction d'un bogue se produisant dans certaines situations lors de la
  journalisation d'une erreur.
* Ces paramètres sont globaux et ne peuvent être configurés que lorsque le
  profil par défaut est actif.

### Version 4.0

* Possibilité de sauvegarder les anciens journaux et introduction d'un
  gestionnaire de journaux.
* Ajout d'un script pour annoncer la dernière erreur enregistrée.
* Correction d'un bogue empêchant la lecture du dernier message du journal
  dans les anciennes versions de NVDA.

### Version 3.2

* Compatibilité avec NVDA 2023.1.

### Version 3.1

* Correction d'une erreur survenant lors de la demande d'une informations
  non disponibles sur un objet.

### Version 3.0

* Dans un journal, vous pouvez maintenant appuyer sur le C dans une ligne
  d'en-tête de message pour ouvrir le module ou la fonction qui l'a émis.
* Dans la console, la fonction `openCodeFile` peut désormais recevoir comme
  paramètre l'objet ou une chaîne contenant son nom.
* Nouvelle fonctionnalité : fichier de démarrage de la console NVDA : s'il
  existe, le fichier YourNVDAConfigFolder\ndtt\consoleStartup.py sera
  exécuté lorsque la console NVDA est ouverte pour la première fois ou
  lorsque les extensions sont rechargées.
* Divers correctifs mineurs pour la fonction de la console Python
  `openCodeFile` et la commande pour ouvrir le fichier source correspondant
  à une ligne du journal.
* Correction d'un problème lorsque vous essayez d'annoncer les rôles / états
  de l'Explorateur d'objets dans une version ancienne de NVDA.
* L'extension ne cause plus de problème avec le tree interceptor lors de
  l'utilisation d'UIA dans Edge.

### Version 2.1

* Divers correctifs et refactorisation et nettoyage du code pour prendre en
  compte tous les cas d'utilisation : toutes les versions prises en charge,
  installées vs. exécutées à partir du code source, etc. (contribution de
  Łukasz Golonka)
* Réécriture du module compa (contribution de Łukasz Golonka)
* Le dialogue pour redémarrer peut désormais être ouvert qu'une seule fois.
* Les raccourcis de l'Explorateur d'objets ne sont désormais pas assignées
  par défaut et doivent être mappés par l'utilisateur.
* Avec l'Explorateur d'objets, un double appui pour appeler le script pour
  annoncer la propriété de l'objet actuel affichant désormais les
  informations annoncées dans un message navigable.

### Version 2.0

* Nouvelle fonctionnalité : dialogue pour redémarrer amélioré afin de
  spécifier quelques options supplémentaires lors du redémarrage de NVDA.
* Nouvelle fonctionnalité : mode de description étendu.
* Fonction pour jouer des sons d'erreur harmonisés entre les versions avant
  et après la 2021.3 de NVDA.
* Nouvelle fonctionnalité : Des commandes de lecture du journal sont
  désormais disponibles dans la visionneuse du journal et, éventuellement,
  dans n'importe quelle champ d'édition et sur les pages Web.
* Nouvelle fonctionnalité : dans la console Python, une fonction
  `openCodeFile` est disponible pour afficher le code source d'un objet.
* Certaines fonctionnalités sont désormais désactivées en mode sécurisé pour
  des raisons de sécurité.
* La plage de compatibilité de l'extension a été étendue (de 2019.2 à
  2021.1).
* Les versions sont désormais effectuées avec GitHub action au lieu de
  appVeyor.

### Version 1.0

* Première version.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
