# NVDA Dev & Test Toolbox #

* Autor: Cyrille Bougot
* Compatibilidade com NVDA: 2019.2 e posterior
* Download [versão estável][1]

Esse complemento reúne vários recursos para depuração e teste do NVDA.

## Recursos

* Uma caixa de diálogo de reinicialização aprimorada para especificar
  algumas opções adicionais ao reiniciar o NVDA.
* Vários recursos relacionados a erros registrados.
* Um explorador de propriedades de objetos.
* Script tools: an extended script description mode and a script opener.
* Comandos para ajudar na leitura e análise de registros.
* Backups de registros antigos
* No espaço de trabalho do console do Python, uma função para abrir o
  código-fonte de um objeto.
* Um script de inicialização personalizado para o console Python
* Um comando para registrar o rastreamento de pilha da função speech.speak.
* A command to reverse translate the items of the interface.

## Commands

This add-on uses layered commands for all of the new commands it adds.  The
entry point for these commands is `NVDA+X`; thus all the commands should be
executed by `NVDA+X` followed by another single letter or gesture.  You can
list all the available layered commands pressing `NVDA+X, H`.

For the commands that you use more frequently, you can also define a direct
gesture in the input gesture dialog.

## Diálogo de reinicialização aprimorado

The `NVDA+X, Q` command opens a dialog to specify some extra options before
restarting NVDA.  The options that can be specified correspond to the
[command line options][2] that can be used with `nvda.exe`, e.g. `-c` for
config path, `--disable-addons` to disable add-ons, etc.

## Recursos relacionados a erros registrados

### Relatar o último erro registrado

Pressing `NVDA+X, E` allows to report the last error logged without needing
to open the log. A second press clears the memorized last error.

### Reproduzir um som para erros registrados

A configuração [“Reproduzir um som para erros registrados”][4] foi
introduzida no NVDA 2021.3 e permite especificar se o NVDA reproduzirá um
som de erro caso um erro seja registrado.

This add-on provides an additional command (`NVDA+X, shift+E`) to toggle
this setting.  You can choose:

* “Somente em versões de teste” (padrão) para fazer o NVDA reproduzir sons
  de erro somente se a versão atual do NVDA for uma versão de teste (alfa,
  beta ou executada a partir da fonte).
* “Sim” para ativar os sons de erro, independentemente da versão atual do
  NVDA.

Para o NVDA anterior à versão 2021.3, este complemento fornece o backport
desse recurso e a possibilidade de controlá-lo com o comando do teclado.  No
entanto, a caixa de seleção no painel Configurações avançadas não é
suportada.

## Explorador de propriedades de objetos

Esse recurso permite relatar algumas propriedades do objeto do navegador
atual sem abrir o visualizador de registros.

Para listar as propriedades de um objeto, mova o objeto do navegador até ele
e use os seguintes comandos:

* `NVDA+X, upArrow`: Selects the previous property and reports it for the
  navigator object.
* `NVDA+X, downArrow`: Selects the next property and reports it for the
  navigator object.
* `NVDA+X, N`: Reports the currently selected property for the navigator
  object
* `NVDA+X, shift+N`: Displays the currently selected property for the
  navigator object in a browseable message

A lista das propriedades compatíveis é a seguinte: name, role, state, value,
windowClassName, windowControlID, windowHandle, location, Python class,
Python class mro.

When using object navigation commands, you can also choose to have the
currently selected property reported instead of NVDA usual object
reporting.  A toggle command, `NVDA+X, control+N`, allows to switch between
this custom reporting of objects and NVDA usual reporting.

Por exemplo, você pode selecionar a propriedade “windowClassName” e ativar o
relatório de objeto personalizado.  Então, ao mover o objeto do navegador
para o objeto seguinte ou anterior, você ouvirá o windowClassName do objeto
em vez do relatório normal.

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

### Modo de descrição de script estendido

The extended script description mode allows to have reported information on
scripts without description in input help mode.

When the Extended script description mode is active, the input help mode
(NVDA+1) is modified as follows.  If a script has no description, the
script's name and class are reported.  If a script has a description, its
description is reported as usual.  The gesture to activate or deactivate
this feature is `NVDA+X, D`.

A execução de um gesto vinculado a um script sem descrição no modo de ajuda
de entrada também cria uma entrada para esse script na caixa de diálogo de
gerenciamento de gestos.  Essa entrada está localizada em uma categoria
dedicada chamada “Scripts sem descrição (modifique por sua própria conta e
risco!)”.  Isso permite adicionar, excluir ou alterar facilmente os gestos
nativos do NVDA para esses scripts.  No entanto, esteja ciente de que muitas
vezes esses scripts não têm nenhuma descrição para evitar que o usuário
modifique o gesto associado.  De fato, o gesto pode ser definido para
corresponder a uma tecla de atalho do aplicativo.  Por exemplo, o script
script_toggleItalic em NVDAObjects.window.winword.WordDocument está
vinculado a control+I e não deve ser modificado, pois o gesto é passado ao
aplicativo para executar a tecla de atalho.

### Exemplo de uso

Control+shift+I também alterna o itálico no Word, mesmo que não seja
relatado nativamente pelo NVDA.  Para que o resultado de control+shift+I
seja relatado pelo NVDA como control+I, execute as seguintes etapas:

* Abra um documento do Word.
* Enable the extended script description mode with `NVDA+X, D`.
* Entre no modo de ajuda de entrada com o NVDA+1.
* Pressione control+I para relatar o script em itálico e adicioná-lo à caixa
  de diálogo de gestos.
* Sair do modo de ajuda de entrada com o NVDA+1.
* Abra a caixa de diálogo de gestos de entrada.
* Na categoria “Scripts sem descrição (modifique por sua própria conta e
  risco!)”, selecione o comando “toggleItalic on
  NVDAObjects.window.winword.WordDocument”.
* Adicione o atalho control+shift+I e valide.
* If you want, exit the extended script description mode with `NVDA+X, D`.

Erro conhecido: Um script adicionado a uma classe específica fica visível
mesmo que o gerenciador de gestos seja aberto em outro contexto.

## Recursos de leitura e análise de registros

<a id="logPlaceMarkers"></a>
### Colocar marcadores no registro

While testing or working, you may want to mark a specific moment in the log, so that you can turn to it easily later when reading the log.
To add a marker message in the log, press `NVDA+X, K`.
A message as follows will be logged at INFO level:  
Marcador NDTT 0 --`  
Você pode adicionar quantos marcadores quiser no registro.  O número do
marcador será incrementado sempre que você colocar um marcador no registro;
ele só será redefinido quando o NVDA for reiniciado.

### Modo de leitura de registros

A log reader mode provides commands to ease log reading and analyzing.  In
the log viewer window the log reader is enabled by default, thus log reading
commands are available immediately.  In another text reading area such as an
editor (e.g. Notepad++) or a webpage (e.g. GitHub issue), you need to press
`NVDA+X, L` to enable log reader mode and use its commands.  When you are
done with log reading and analyzing tasks, you can disable again `NVDA+X, L`
to disable the log reader mode.

Os comandos disponíveis no modo de leitura de registros são descritos a
seguir.

<a id=“logReaderQuickNavigationCommands”></a>
#### Comandos de navegação rápida

O comando de uma única letra, semelhante às teclas de navegação rápida do
modo de navegação, permite ir para vários tipos de mensagens de registro:

* m: qualquer mensagem
* e: mensagens de erro (`ERROR` e `CRITICAL`)
* w: mensagens de aviso (`AVISO`)
* f: mensagens informativas (`INFO`)
* k: marcadores previamente [colocados no registro] (#logPlaceMarkers)
* g: mensagens de aviso de depuração (`DEBUGWARNING`)
* i: mensagens de entrada/saída (`IO`)
* n: mensagens de entrada
* s: mensagens de fala
* d: mensagens de depuração (`DEBUG`)

Pressionar uma única letra leva à próxima ocorrência dessa mensagem. A
combinação da letra com a tecla shift leva à ocorrência anterior dessa
mensagem.

#### Tradução da mensagem de fala

Às vezes, pode ser necessário examinar um registro feito em um sistema em um
idioma estrangeiro que você não entende. Por exemplo, o registro foi feito
em um sistema chinês / NVDA, enquanto você só entende francês.  Se você
tiver o complemento [Instant Translate][3] instalado, poderá usá-lo em
conjunto com [quick log navigation commands]
(#logReaderQuickNavigationCommands) para que as mensagens de fala sejam
traduzidas.

* Primeiro, configure os idiomas do Instant Translate. O idioma de origem
  deve ser o idioma do sistema em que o registro foi feito (por exemplo,
  chinês). O idioma de destino deve ser o seu idioma (por exemplo, francês).
* Abra o registro
* Pressione T para ativar a tradução automática de fala no registro
* Use os comandos de navegação rápida no registro, por exemplo, S, I,
  etc. Sempre que uma mensagem de voz for encontrada, ela será falada em seu
  idioma (francês em nosso exemplo anterior)

Se quiser desativar a tradução de fala, pressione T novamente.



<a id=“logReaderOpenSourceFile”></a>
#### Abra o arquivo do código-fonte em seu editor

No registro, algumas linhas podem se referir ao código-fonte:

* Uma linha pertencente a um traceback contém o caminho e a linha em um
  arquivo, por exemplo:
  Arquivo “virtualBuffers\__init__.pyc”, linha 226, em _getStoryLength`  
* A linha de cabeçalho de uma mensagem registrada contém a função que
  registrou essa mensagem, por exemplo:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`  
* O conteúdo de uma mensagem registrada no modo de ajuda de entrada
  (registrada no nível de informação):
  `Input help: gesture kb(desktop):NVDA+t, bound to script title on globalCommands.GlobalCommands`  

Talvez você queira abrir o arquivo que contém esse código para entender o
contexto do traceback ou da mensagem registrada.  Basta pressionar C para
abrir esse arquivo.

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source and want to open NVDA's code, the [location
of NVDA source code](#settingsNvdaSourcePath) should also have been
configured.

<a id="oldLogsBackup"></a>
## Backup de registros antigos

O NVDA já fornece um backup do seu registro  da sessão anterior; o arquivo é
chamado `nvda-old.log`.  No entanto, às vezes você pode querer acessar os
registros mais antigos, por exemplo, porque teve que reiniciá-lo novamente
antes de consultar o `nvda-old.log`.  Esse complemento permite que você
configure se deseja fazer backup de logs antigos e quantos deles; isso é
feito nas [configurações do complemento] (#settingsLogsBackup).

A log manager dialog allows to view the backed up logs.
It can be opened going to NVDA menu -> Tools -> Logs manager
In this dialog, you can see the list of all the backup logs and perform various actions on the selected log:

* open it (press `Enter`)
* delete it (press `Delete`)
* copy the log file (press `control+C`)

You can also select multiple logs to perform an actions on all of them.

To be able to open a log, you should first have configured the [Command to
open a file in your favorite editor](#settingsOpenCommand).

## Extensão do console Python

<a id=“pythonConsoleOpenCodeFile”></a>
### Função `openCodeFile

No console, você pode chamar a seguinte função para exibir o código-fonte que define a variável `myVar`:  
`openCodeFile(myVar)`  

For this feature to work, you need to have configured your [favorite
editor's command](#settingsOpenCommand) in the add-on's settings.  If you
are not running NVDA from source and want to open NVDA's code, the [location
of NVDA source code](#settingsNvdaSourcePath) should also have been
configured.

As funções `openCodeFile` podem ser chamadas em objetos definidos no código
do NVDA ou em objetos definidos por complementos.  Elas não podem ser
chamadas em objetos cujo código-fonte não esteja disponível, como os
incorporados em python.

Se ainda não tiver importado o objeto no console, também poderá passar o
nome dele como parâmetro para a função `openCodeFile`.

Abaixo estão exemplos de chamadas no código do NVDA:

* Veja a definição da função `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`  
  ou com o nome passado como parâmetro:  
  `openCodeFile(“speech.speech.speak”)`  
* Veja a definição da classe `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`  
* Veja a definição do método `área de transferência` da classe `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Visualizar a definição da classe do objeto focalizado:
  `openCodeFile(focus)`  
* Abra o arquivo `api.py` que define o módulo `api`:
  `openCodeFile(api)`  

### Script de inicialização do console Python

Você pode definir um script personalizado que será executado no namespace do
console Python quando ele for aberto pela primeira vez ou se o complemento
for recarregado (NVDA+F3) depois que o console já tiver sido aberto.

Por exemplo, o script permite executar novas importações e definir aliases que poderão ser usados diretamente no console, conforme mostrado abaixo:  

    # Várias importações que eu quero no console.
    importar globalVars como gv
    importar núcleo
    import ui
    # Aliases
    ocf = openCodeFile

O script do console Python deve ser colocado no seguinte local: `pathToNVDAConfig\ndtt\consoleStartup.py`  
Por exemplo:
`C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Registre o rastreamento de pilha da função de fala

Sometimes, you may want to see which part of the code is responsible for
speaking something.  For this, you can enable the stack trace logging of the
speech function pressing `NVDA+X, S`.  Each time NVDA speaks, a
corresponding stack trace will be logged in the log.

Observação: Você pode modificar o arquivo do script diretamente para
corrigir outra função.  Consulte todas as instruções no arquivo para obter
detalhes sobre o uso.

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

<a id=“settings”></a>
## Configurações

Alguns recursos do complemento podem exigir uma configuração específica.
Um painel de configurações permite ativá-los ou controlar como eles funcionam.
Para exibir e modificar essas configurações, acesse o menu NVDA -> Preferências e selecione a categoria NVDA Dev & Test Toolbox.
Essa caixa de diálogo de configurações também pode ser acessada diretamente na caixa de diálogo Logs Manager.

Essas configurações são globais e só podem ser definidas quando o perfil
padrão estiver ativo.

<a id=“settingsOpenCommand”></a>
### Comando para abrir um arquivo em seu editor favorito

Some features allow to see content in your favorite editor.  This includes
the commands to view the source file [from a log](#logReaderOpenSourceFile),
[from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed
gesture](#scriptOpener), as well as the [log manager](#oldLogsBackup)'s Open
button.

Para usá-los, primeiro você precisa configurar o comando que será chamado para abrir o arquivo em seu editor favorito.
O comando deve ter o formato:  
`“C:\path\to\my\editor\editor.exe” “{path}”:{line}`  
É claro que você deve modificar essa linha de acordo com o nome e o local reais do seu editor e com a sintaxe usada por ele para abrir arquivos.
`{path}` será substituído pelo caminho completo do arquivo a ser aberto e `{line}` pelo número da linha em que você deseja que o cursor seja definido.
Para o Notepad++, por exemplo, o comando a ser digitado no console seria:  
`“C:\Program Files\Notepad++\notepad++.exe” “{path}” -n{line}`

<a id=“settingsNvdaSourcePath”></a>
### Caminho do código-fonte do NVDA

When using a command to view the source file [from a log](#logReaderOpenSourceFile), [from an object in the console](#pythonConsoleOpenCodeFile) or [from a typed gesture](#scriptOpener), the file may belong to NVDA itself.
If you are not running NVDA from source, your NVDA only contains compiled files.
Thus you may specify here an alternate location where the corresponding source file will be found, e.g. the place where you have cloned NVDA source files, so that a source file can be opened anyway.
The path should be such as:  
`C:\pathExample\GIT\nvda\source`  
Claro, substitua o caminho da fonte do NVDA pelo caminho correto.

No entanto, certifique-se de que a versão do seu arquivo de origem (por
exemplo, confirmação do GIT) seja a mesma da instância em execução do NVDA.

<a id=“settingsLogsBackup”></a>
### Backup de registros antigos

A caixa de combinação Backup de registros antigos permite ativar ou
desativar o [recurso](#oldLogsBackup).  Se ele estiver ativado, você também
poderá especificar abaixo, em “Limitar o número de backups”, o número máximo
de backups que deseja manter.  Essas configurações só entram em vigor na
próxima inicialização do NVDA, quando o backup for realizado.

<a id="settingsCopyReverseTranslation"></a>
### Copy reverse translation to clipboard

This option allows to choose if the [reverse translation
command](#reverseTranslationCommand) also copies its result to the
clipboard.

## Registro de alterações

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

### Versão 6.2

* Restaura a abertura do console para o NVDA < 2021.1.
* Resolve possíveis problemas de segurança relacionados ao
  [GHSA-xg6w-23rw-39r8][5] ao usar o complemento com versões mais antigas do
  NVDA. No entanto, é recomendável usar o NVDA 2023.3.3 ou superior.

### Versão 6.1

* A abertura do arquivo de origem de um objeto localizado no submódulo de um
  pacote agora está funcionando.
* Correção de bug: A caixa de diálogo de saída aprimorada agora pode ser
  reaberta e usada como esperado depois de ter sido fechada. (contribuição
  de Łukasz Golonka)

### Versão 6.0

* Quando usar comandos de navegação de objetos, uma propriedade específica
  do objeto pode ser relatada em vez do relatório de objetos usual do NVDA.
* No modo de leitura de registro, a tecla “C” para abrir um arquivo de
  código do registro agora também funciona em uma mensagem de ajuda de
  entrada.
* Correção de bug: o complemento agora pode ser iniciado com êxito quando o
  número de registros a serem salvos é definido com o valor máximo.
* Correção de bug: A saída do script de inicialização do console Python não
  impede mais que se pule para o primeiro resultado no console ao usar
  comandos de navegação de resultados.
* Nota: De agora em diante, as atualizações de localização não aparecerão
  mais no registro de alterações.

### Versão 5.0

* Se o complemento Instant Translate estiver instalado, agora é possível ter
  mensagens de fala traduzidas em tempo real ao usar comandos de leitura de
  registro.
* No modo de leitura de registro, pressionar E ou shift+E agora salta para
  as mensagens de ERRO CRÍTICO, bem como para as mensagens de ERRO normais.
* Novos comandos de navegação rápida de registro foram adicionados para
  saltar para a entrada e para as mensagens de fala.
* A new command allow to place a marker in the log; and specific quick
  navigation commands in log reading mode allow to jump to them.
  Credit: the initial idea for this feature comes from Debug Helper add-on by Luke Davis.
* Bubfix: The memorization of the last error do not fail anymore in some cases.
* Bugfix: The add-on can initialize again with NVDA 2019.2.1.
* Bugfix: Log saving feature will not fail anymore with non-ASCII logs.

### Versão 4.2

* Corrigido um erro com a versão do NVDA abaixo de 2021.3.
* Correção da formatação do registro de rastreamento de pilha.
* Primeiras localizações.

### Versão 4.1

* Correção de um bug que ocorria em algumas situações durante o registro de
  um erro.
* As configurações do complemento agora podem ser modificadas somente quando
  o perfil padrão estiver ativo para evitar problemas de configuração.

### Versão 4.0

* Possibilidade de fazer backup de registros antigos e introdução de um
  gerenciador de registros.
* Adicionado um script para relatar o último erro registrado.
* Foi corrigido um erro que impedia a leitura da última mensagem de registro
  em versões mais antigas do NVDA.

### Versão 3.2

* Compatibilidade com o NVDA 2023.1.

### Versão 3.1

* Foi corrigido um erro que ocorria ao solicitar informações indisponíveis
  sobre um objeto.

### Versão 3.0

* Em um registro, agora é possível pressionar C na linha de cabeçalho de uma
  mensagem para abrir a função/módulo que a emitiu.
* No console, a função `openCodeFile` agora pode receber como parâmetro o
  objeto ou uma string contendo seu nome.
* Novo recurso: Arquivo de inicialização do console NVDA: Se existir, o
  arquivo YourNVDAConfigFolder\ndtt\consoleStartup.py será executado quando
  o console NVDA for aberto pela primeira vez ou quando os complementos
  forem recarregados.
* Várias pequenas correções para a função do console Python `openCodeFile` e
  o comando para abrir o arquivo de origem correspondente a uma linha no
  registro.
* Corrigido um problema ao tentar relatar funções/estados para o explorador
  de objetos em uma versão mais antiga do NVDA.
* O complemento não causa mais problemas com o interceptor de árvore ao usar
  o UIA no Edge.

### Versão 2.1

* Várias correções de bugs e refatoração/limpeza de código para atender a
  todos os casos de uso: todas as versões suportadas, instaladas versus
  executadas a partir da fonte etc. (contribuição de Łukasz Golonka)
* Reescrita do módulo compa (contribuição de Łukasz Golonka)
* A caixa de diálogo de reinicialização agora pode ser aberta apenas uma
  vez.
* Os atalhos do explorador de objetos agora não são atribuídos por padrão e
  precisam ser mapeados pelo usuário.
* Com o explorador de objetos, pressionar duas vezes para chamar o script
  para relatar a propriedade do objeto atual agora exibe as informações
  relatadas em uma mensagem navegável.

### Versão 2.0

* Novo recurso: Diálogo de reinicialização aprimorado para especificar
  algumas opções extras ao reiniciar o NVDA.
* Novo recurso: modo de descrição estendida.
* Recurso de som de erro de reprodução harmonizado entre as versões pré e
  pós 2021.3 do NVDA.
* Novo recurso: Os comandos do leitor de registros agora estão disponíveis
  no visualizador de registros e também, opcionalmente, em campos de edição
  ou páginas da Web.
* O comando NVDA+shift+Q abre uma caixa de diálogo para especificar algumas
  opções extras antes de reiniciar o NVDA.  As opções que podem ser
  especificadas correspondem às [opções de linha de comando][2] que podem
  ser usadas com o `nvda.exe`, por exemplo, `-c` para o caminho de
  configuração, `--disable-addons` para desativar complementos etc.
  O comando NVDA+shift+Q abre uma caixa de diálogo para especificar algumas
  opções extras antes de reiniciar o NVDA.  As opções que podem ser
  especificadas correspondem às [opções de linha de comando][2] que podem
  ser usadas com o `nvda.exe`, por exemplo, `-c` para o caminho de
  configuração, `--disable-addons` para desativar complementos etc.
* Alguns recursos agora estão desativados no modo seguro por motivos de
  segurança.
* O intervalo de compatibilidade do complemento foi ampliado (de 2019.2 para
  2021.1).
* Os lançamentos agora são realizados com a ação do GitHub em vez do
  appVeyor.

### Versão 1.0

* Lançamento inicial.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://github.com/nvaccess/nvda/security/advisories/GHSA-xg6w-23rw-39r8#event-132994
