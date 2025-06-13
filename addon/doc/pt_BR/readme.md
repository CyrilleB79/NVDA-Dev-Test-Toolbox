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
* Ferramentas de script: um modo de descrição de script estendido e um
  abridor de script.
* Comandos para ajudar na leitura e análise de registros.
* Backups de registros antigos
* No espaço de trabalho do console do Python, uma função para abrir o
  código-fonte de um objeto.
* Um script de inicialização personalizado para o console Python
* Um comando para registrar o rastreamento de pilha da função speech.speak.
* Um comando para reverter a tradução dos itens da interface.

## Comandos

Esse complemento utiliza comandos em camadas para todos os novos comandos
que adiciona.  O ponto de entrada para esses comandos é `NVDA+X`; portanto,
todos os comandos devem ser executados por `NVDA+X` seguido de outra letra
ou gesto.  Você pode listar todos os comandos em camadas disponíveis
pressionando `NVDA+X, H`.

Para os comandos que você usa com mais frequência, também é possível definir
um gesto direto na caixa de diálogo de gestos de entrada.

## Diálogo de reinicialização aprimorado

O comando `NVDA+X, Q` abre uma caixa de diálogo para especificar algumas
opções extras antes de reiniciar o NVDA.  As opções que podem ser
especificadas correspondem às [opções de linha de comando][2] que podem ser
usadas com o `nvda.exe`, por exemplo, `-c` para o caminho de configuração,
`--disable-addons` para desativar complementos etc.

## Recursos relacionados a erros registrados

### Relatar o último erro registrado

Pressionar `NVDA+X, E` permite relatar o último erro registrado sem a
necessidade de abrir o registro. Um segundo pressionamento apaga o último
erro memorizado.

### Reproduzir um som para erros registrados

A configuração [“Reproduzir um som para erros registrados”][4] foi
introduzida no NVDA 2021.3 e permite especificar se o NVDA reproduzirá um
som de erro caso um erro seja registrado.

Esse complemento fornece um comando adicional (`NVDA+X, shift+E`) para
alternar essa configuração.  Você pode escolher:

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

* `NVDA+X, setaParaCima`: Seleciona a propriedade anterior e a informa para
  o objeto do navegador.
* `NVDA+X, setaParaBaixo`: Seleciona a próxima propriedade e a informa para
  o objeto do navegador.
* `NVDA+X, N`: Informa a propriedade selecionada no momento para o objeto do
  navegador
* `NVDA+X, shift+N`: Exibe a propriedade selecionada no momento para o
  objeto do navegador em uma mensagem navegável

A lista das propriedades compatíveis é a seguinte: name, role, state, value,
windowClassName, windowControlID, windowHandle, location, Python class,
Python class mro.

Quando usar os comandos de navegação de objetos, você também pode optar por
ter a propriedade selecionada no momento relatada em vez do relatório de
objetos usual do NVDA.  Um comando de alternância, `NVDA+X, control+N`,
permite alternar entre esse relatório personalizado de objetos e o relatório
normal do NVDA.

Por exemplo, você pode selecionar a propriedade “windowClassName” e ativar o
relatório de objeto personalizado.  Então, ao mover o objeto do navegador
para o objeto seguinte ou anterior, você ouvirá o windowClassName do objeto
em vez do relatório normal.

## Ferramentas de script

<a id=“scriptOpener”></a>
<a id=“settings”></a>
### Abertura do script

O comando de abertura de script permite abrir o código de um script
conhecendo seu gesto.

Para utilizá-lo, pressione `NVDA+x, C` e, em seguida, o gesto do script cujo
código você deseja visualizar.  Por exemplo, para ver o código do script que
informa o título da janela em primeiro plano, pressione `NVDA+X, C` e, em
seguida, `NVDA+T`.

Para que esse recurso funcione, você precisa ter configurado seu [comando do
editor favorito] (#settingsOpenCommand) nas configurações do complemento.
Se não estiver executando o NVDA a partir da fonte, o [local do código-fonte
do NVDA] (#settingsNvdaSourcePath) também deverá ter sido configurado.

### Modo de descrição de script estendido

O modo de descrição de script estendido permite ter informações relatadas
sobre scripts sem descrição no modo de ajuda de entrada.

Quando o modo de descrição de script estendido está ativo, o modo de ajuda
de entrada (NVDA+1) é modificado da seguinte forma.  Se um script não tiver
descrição, o nome e a classe do script serão informados.  Se um script tiver
uma descrição, sua descrição será informada como de costume.  O gesto para
ativar ou desativar esse recurso é `NVDA+X, D`.

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
* Habilite o modo de descrição de script estendido com `NVDA+X, D`.
* Entre no modo de ajuda de entrada com o NVDA+1.
* Pressione control+I para relatar o script em itálico e adicioná-lo à caixa
  de diálogo de gestos.
* Sair do modo de ajuda de entrada com o NVDA+1.
* Abra a caixa de diálogo de gestos de entrada.
* Na categoria “Scripts sem descrição (modifique por sua própria conta e
  risco!)”, selecione o comando “toggleItalic on
  NVDAObjects.window.winword.WordDocument”.
* Adicione o atalho control+shift+I e valide.
* Se desejar, saia do modo de descrição de script estendido com `NVDA+X, D`.

Erro conhecido: Um script adicionado a uma classe específica fica visível
mesmo que o gerenciador de gestos seja aberto em outro contexto.

## Recursos de leitura e análise de registros

<a id="logPlaceMarkers"></a>
### Colocar marcadores no registro

Durante o teste ou o trabalho, talvez você queira marcar um momento específico no registro, para que possa acessá-lo facilmente mais tarde ao ler o registro.
Para adicionar uma mensagem de marcador no registro, pressione `NVDA+X, K`.
Uma mensagem como a seguinte será registrada no nível INFO:  
Marcador NDTT 0 --`  
Você pode adicionar quantos marcadores quiser no registro.  O número do
marcador será incrementado sempre que você colocar um marcador no registro;
ele só será redefinido quando o NVDA for reiniciado.

### Modo de leitura de registros

Um modo de leitor de log fornece comandos para facilitar a leitura e a
análise do log.  Na janela do visualizador de logs, o leitor de logs está
ativado por padrão e, portanto, os comandos de leitura de logs estão
disponíveis imediatamente.  Em outra área de leitura de texto, como um
editor (por exemplo, Notepad++) ou uma página da Web (por exemplo, um
problema no GitHub), é necessário pressionar `NVDA+X, L` para ativar o modo
de leitura de log e usar seus comandos.  Quando terminar as tarefas de
leitura e análise de logs, desative novamente `NVDA+X, L` para desativar o
modo de leitor de logs.

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
  `Ajuda de entrada: gesto kb(desktop):NVDA+t, vinculado ao título do script em globalCommands.GlobalCommands`  
  Ajuda de entrada: gesto kb(desktop):NVDA+t, vinculado ao título do script em globalCommands.GlobalCommands`  

Talvez você queira abrir o arquivo que contém esse código para entender o
contexto do traceback ou da mensagem registrada.  Basta pressionar C para
abrir esse arquivo.

Para que esse recurso funcione, você precisa ter configurado seu [comando do
editor favorito] (#settingsOpenCommand) nas configurações do complemento.
Se não estiver executando o NVDA a partir da fonte, o [local do código-fonte
do NVDA] (#settingsNvdaSourcePath) também deverá ter sido configurado.

<a id="oldLogsBackup"></a>
## Backup de registros antigos

O NVDA já fornece um backup do seu registro  da sessão anterior; o arquivo é
chamado `nvda-old.log`.  No entanto, às vezes você pode querer acessar os
registros mais antigos, por exemplo, porque teve que reiniciá-lo novamente
antes de consultar o `nvda-old.log`.  Esse complemento permite que você
configure se deseja fazer backup de logs antigos e quantos deles; isso é
feito nas [configurações do complemento] (#settingsLogsBackup).

Uma caixa de diálogo do gerenciador de registros permite visualizar os registros de backup.
Ela pode ser aberta no menu NVDA -> Ferramentas -> Logs manager
Nessa caixa de diálogo, é possível ver a lista de todos os logs de backup e executar várias ações no log selecionado:

* abra-o (pressione `Enter`)
* exclua-o (pressione `Delete`)
* copie o arquivo de registro (pressione `control+C`)

Também é possível selecionar vários registros para executar uma ação em
todos eles.

Para poder abrir um registro, primeiro você deve ter configurado o [Comando
para abrir um arquivo no seu editor favorito] (#settingsOpenCommand).

## Extensão do console Python

<a id=“pythonConsoleOpenCodeFile”></a>
### Função `openCodeFile

No console, você pode chamar a seguinte função para exibir o código-fonte que define a variável `myVar`:  
`openCodeFile(myVar)`  

Para que esse recurso funcione, você precisa ter configurado seu [comando do
editor favorito] (#settingsOpenCommand) nas configurações do complemento.
Se não estiver executando o NVDA a partir da fonte, o [local do código-fonte
do NVDA] (#settingsNvdaSourcePath) também deverá ter sido configurado.

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

Às vezes, você pode querer ver qual parte do código é responsável por falar
algo.  Para isso, você pode ativar o registro de rastreamento de pilha da
função de fala pressionando `NVDA+X, S`.  Cada vez que o NVDA falar, um
rastreamento de pilha correspondente será registrado no log.

Observação: Você pode modificar o arquivo do script diretamente para
corrigir outra função.  Consulte todas as instruções no arquivo para obter
detalhes sobre o uso.

<a id=“reverseTranslationCommand”></a>
## Comando de conversão reversa

Muitos testadores usam o NVDA em outro idioma que não o inglês.  Porém, ao
relatar os resultados do teste no GitHub, a descrição das opções modificadas
ou as mensagens relatadas pelo NVDA devem ser escritas em inglês.  É muito
frustrante e demorado ter que reiniciar o NVDA em inglês para verificar o
texto exato das opções ou mensagens.

Para evitar isso, o complemento fornece um comando de tradução reversa
(`NVDA+X, R`) que permite a tradução reversa da interface do NVDA, como
mensagens, rótulos de controle na GUI, etc.  Esse comando usa a tradução
gettext do NVDA para tentar traduzir a última fala.  Mais especificamente, a
primeira cadeia de caracteres da última sequência de fala é traduzida de
forma reversa.

Por exemplo, no NVDA francês, se eu apontar a seta para baixo até o menu
Ferramentas chamado “Outils”, o NVDA dirá “Outils sous-Menu o”, que
significa “Tools subMenu o”.  Se eu pressionar o comando de tradução reversa
logo em seguida, o NVDA fará a tradução reversa de “Outils” para “Tools”.

Observando o registro depois, podemos encontrar as seguintes linhas:
```
IO - speech.speech.speak (23:38:24.450) - MainThread (2044):
Falando ['Outils', 'sous-Menu', CharacterModeCommand(True), 'o', CharacterModeCommand(False), CancellableSpeech (ainda válido)]
```
Isso confirma que “Outils foi a primeira string na sequência de fala.

Caso a tradução reversa leve a dois ou mais resultados possíveis, um menu de
contexto é aberto listando todas as possibilidades.

O resultado da tradução reversa também é copiado para a área de
transferência se a [opção](#settingsCopyReverseTranslation) correspondente
estiver ativada, que é o valor padrão.

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

Alguns recursos permitem ver o conteúdo em seu editor favorito.  Isso inclui
os comandos para visualizar o arquivo de origem [de um
log](#logReaderOpenSourceFile), [de um objeto no
console](#pythonConsoleOpenCodeFile) ou [de um gesto
digitado](#scriptOpener), bem como o botão Abrir do [gerenciador de
logs](#oldLogsBackup).

Para usá-los, primeiro você precisa configurar o comando que será chamado para abrir o arquivo em seu editor favorito.
O comando deve ter o formato:  
`“C:\path\to\my\editor\editor.exe” “{path}”:{line}`  
É claro que você deve modificar essa linha de acordo com o nome e o local reais do seu editor e com a sintaxe usada por ele para abrir arquivos.
`{path}` será substituído pelo caminho completo do arquivo a ser aberto e `{line}` pelo número da linha em que você deseja que o cursor seja definido.
Para o Notepad++, por exemplo, o comando a ser digitado no console seria:  
`“C:\Program Files\Notepad++\notepad++.exe” “{path}” -n{line}`

<a id=“settingsNvdaSourcePath”></a>
### Caminho do código-fonte do NVDA

Quando usar um comando para exibir o arquivo de origem [de um log] (#logReaderOpenSourceFile), [de um objeto no console] (#pythonConsoleOpenCodeFile) ou [de um gesto digitado] (#scriptOpener), o arquivo pode pertencer ao próprio NVDA.
Se você não estiver executando o NVDA a partir do código-fonte, o NVDA conterá apenas arquivos compilados.
Portanto, você pode especificar aqui um local alternativo onde o arquivo de origem correspondente será encontrado, por exemplo, o local onde você clonou os arquivos de origem do NVDA, de modo que um arquivo de origem possa ser aberto de qualquer forma.
O caminho deve ser tal como:  
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
### Copiar a tradução reversa para a área de transferência

Essa opção permite escolher se o [comando de tradução reversa]
(#reverseTranslationCommand) também copia o resultado para a área de
transferência.

## Registro de alterações

### Versão 7.0

* Layered commands have been introduced; the entry point is `NVDA+X`.
  The existing commands have been modified accordingly.  
* Um novo comando (`NVDA+X, R`) para reverter a tradução da última mensagem
  falada.
* Um novo comando (`NVDA+X, C`) para abrir o código-fonte do script
  associado ao próximo gesto pressionado.
* Adicionado suporte a fala sob demanda.
* O gerenciador de registros agora permite mais ações, seja com os botões
  dedicados nas caixas de diálogo ou usando atalhos de teclado na lista:
  `enter` para abrir o registro, `control+C` para copiar o arquivo de
  registro e `delete` para excluir um arquivo de registro.
* A ordem de classificação no gerenciador de registros foi invertida
  (registro mais recente no topo).
* Foi corrigido um problema ao tentar abrir um módulo Python com a função
  openCodeFile.

### Versão 6.3

* Compatibilidade com o NVDA 2024.1.

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
* Correção: A memorização do último erro não falha mais em alguns casos.
* Correção de bug: o complemento pode ser inicializado novamente com o NVDA
  2019.2.1.
* Correção de bug: O recurso de salvamento de registros não falhará mais com
  registros não ASCII.

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
