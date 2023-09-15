# Caja de herramientas de desarrollo y pruebas para NVDA #

* Autor: Cyrille Bougot
* Compatibilidad con NVDA: de 2019.2 en adelante
* Descargar [versión estable][1]

Este complemento reúne diversas funciones para depuración y pruebas en NVDA.

## Características

* Un diálogo mejorado para reiniciar que permite indicar algunas opciones
  extra cuando se reinicia NVDA.
* Diversas funciones relacionadas con errores registrados.
* Un explorador de propiedades de los objetos.
* Un modo de descripción extendida para los scripts: cuando está activado,
  el modo ayuda de entrada anuncia información de los scripts que no tienen
  descripción.
* Órdenes para ayudar con la lectura y el análisis del registro.
* Copias de seguridad de registros antiguos
* En el espacio de trabajo de la consola Python, una función para abrir el
  código fuente de un objeto.
* Un script personalizado de inicio para la consola Python
* Una orden para registrar la pila de llamadas de la función speech.speak.

## Diálogo reiniciar mejorado

La orden NVDA+shift+q abre un diálogo para indicar algunas opciones extra
antes de reiniciar NVDA. Las opciones que pueden especificarse corresponden
a las [opciones de línea de órdenes][2] que se pueden usar con `nvda.exe`,
como `-c` para la ruta de configuración, `--disable-addons` para
deshabilitar los complementos, etc.

## Funciones relacionadas con errores registrados

### Anunciar último error registrado

Pulsar NVDA+shift+alt+E permite anunciar el último error registrado sin
necesidad de abrir el registro. Una segunda pulsación elimina el último
error memorizado.

### Reproducir un sonido para los errores registrados

La [opción "Reproducir un sonido para los errores registrados"][4] se
introdujo en NVDA 2021.3 y permite especificar si NVDA reproducirá un sonido
de error en caso de que se registre un error.

Este complemento proporciona una orden adicional (NVDA+control+alt+e) para
conmutar este ajuste. Puedes elegir:

* "Sólo en versiones de prueba de NVDA" (por defecto) para que NVDA
  reproduzca sonidos de error sólo si la versión actual de NVDA es una
  versión de prueba (alfa, beta o ejecutada desde el código fuente).
* "Sí" para habilitar los sonidos de error sea cual sea tu versión de NVDA.

En versiones de NVDA anteriores a la 2021.3, este complemento proporciona el
backport de esta característica y la posibilidad de controlarla con la orden
de teclado. La casilla de verificación del panel de opciones avanzadas, sin
embargo, no se incluye.

## Explorador de propiedades de los objetos

Esta función permite anunciar algunas propiedades del objeto actual en el
navegador de objetos sin abrir el visualizador del registro.

Para enumerar las propiedades de un objeto, mueve el navegador de objetos
hacia él y usa las siguientes órdenes:

* Selecciona la propiedad anterior y la anuncia para el navegador de
  objetos.
* Selecciona la siguiente propiedad y la anuncia para el navegador de
  objetos.
* Anuncia la propiedad seleccionada actualmente para el navegador de
  objetos; al pulsar dos veces rápidamente, muestra esta información en un
  mensaje explorable.

Estas tres órdenes vienen sin asignar por defecto; tendrás que asignarlas
desde el diálogo Gestos de entrada para poder usarlas.

La lista de propiedades soportadas es la siguiente: nombre, rol, estado,
valor, nombre de clase de la ventana, id de control de la ventana, manejador
de la ventana, ubicación, clase Python, orden de resolución de métodos de la
clase Python.

Esta función es una mejora de un ejemplo de la [guía de desarrollo de
NVDA][5].


## Modo de descripción extendida de scripts

Cuando el modo de descripción extendida de scripts está activado, el modo de
ayuda de entrada (NVDA+1) se modifica de la siguiente manera. Si un script
no tiene descripción, se anuncian su nombre y su clase. Si un script tiene
descripción, esta se anuncia como siempre. El gesto para activar o
desactivar esta función es NVDA+control+alt+d.

Ejecutar un gesto asociado a un script sin descripción en el modo ayuda de
entrada también crea una entrada para este script en el diálogo de
administración de gestos. Esta entrada se ubica en una categoría dedicada
llamada "Scripts sin descripción (¡Modifica bajo tu responsabilidad!)". Esto
permite añadir, eliminar o cambiar fácilmente los gestos nativos de NVDA
para estos scripts. Ten en cuenta, sin embargo, que el script puede no tener
una descripción intencionadamente para que el usuario no pueda
modificarlo. El script puede estar pensado para coincidir con un atajo de
una aplicación concreta. Por ejemplo, el script script_toggleItalic en
NVDAObjects.window.winword.WordDocument está asignado a control+k, y no
debería modificarse, ya que el gesto se pasa a la aplicación para ejecutar
realmente ese atajo de teclado.

### Ejemplo de uso

Control+shift+k también conmuta la cursiva en Word, incluso si NVDA no lo
anuncia de forma nativa. Para que el resultado de pulsar control+shift+k se
anuncie como control+k, deberías seguir los siguientes pasos:

* Abre un documento de Word.
* Activa el modo de descripción extendida de scripts con NVDA+control+alt+d.
* Entra en el modo ayuda de entrada con NVDA+1.
* Pulsa control+K para anunciar el script de cursiva y añadirlo al diálogo
  de gestos.
* Sal del modo ayuda de entrada con NVDA+1.
* Abre el diálogo Gestos de entrada.
* En la categoría "Scripts sin descripción (¡Modifícalos bajo tu
  responsabilidad!)", selecciona la orden "toggleItalic en
  NVDAObjects.window.winword.WordDocument".
* Añade el atajo control+shift+k y valida.
* Si quieres, sal del modo de descripción extendida de scripts con
  NVDA+control+alt+d.

Fallo conocido: Un script añadido para una clase concreta es visible incluso
si el administrador de gestos se abre en otro contexto.

## Funciones de lectura y análisis del registro

<a id="logPlaceMarkers"></a>
### Marcadores de posición en el registro

Al trabajar o hacer pruebas, puedes querer marcar un momento concreto en el registro, de tal manera que puedas regresar a él después al leer el registro.
Para añadir un mensaje de marcador al registro, pulsa NVDA+control+k.
Se registrará un mensaje como el siguiente en el nivel info:
`-- NDTT marker 0 --`  
Puedes añadir tantos marcadores como quieras en el registro. El número del
marcador se incrementará cada vez que sitúes un marcador en el registro;
sólo se restablecerá al reiniciar NVDA.

### Modo lector del registro

El modo lector del registro proporciona órdenes facilitar la lectura y el
análisis del registro. En la ventana del visualizador del registro, el
lector del registro está habilitado por defecto, por lo que los comandos de
lectura del registro están disponibles de inmediato. En otras áreas de
lectura de texto, tales como un editor (por ejemplo, Notepad++) o una página
web (por ejemplo, una incidencia de GitHub), es necesario pulsar
NVDA+control+alt+l para activar el modo de lectura del registro y usar sus
órdenes. Cuando acabes con las tareas de análisis y lectura del registro,
puedes desactivar de nuevo el modo lector del registro con
NVDA+control+alt+l.

Las órdenes disponibles en el modo de lectura del registro se describen a
continuación.

<a id="logReaderQuickNavigationCommands"></a>
#### Órdenes de navegación rápida

Existen órdenes de navegación de una sola letra, similares a las usadas en
modo exploración, que permiten moverse por distintos tipos de mensajes en el
registro:

* m: cualquier mensaje
* e: mensajes de error (`ERROR` y `CRITICAL`)
* w: mensajes de advertencia (`WARNING`)
* f: mensajes informativos (`INFO`)
* k: marcadores previamente [situados en el registro](#logPlaceMarkers)
* g: mensajes de aviso de depuración (`DEBUGWARNING`)
* i: mensajes de entrada/salida (`IO`)
* n: mensajes entrantes
* s: mensajes hablados
* d: mensajes de depuración (`DEBUG`)

Pulsando la letra te moverás a la siguiente coincidencia de ese mensaje. Al
combinar la letra con la tecla shift, te desplazarás a la coincidencia
anterior.

#### Traducción de mensajes hablados

A veces, puedes tener que mirar un registro tomado en un sistema con un
idioma extranjero que no entiendes. Por ejemplo, el registro se tomó en un
sistema / NVDA en chino, pero sólo entiendes francés. Si tienes instalado el
complemento [Instant Translate][3], puedes usarlo junto con las [órdenes de
navegación rápida por el registro](#logReaderQuickNavigationCommands) para
traducir los mensajes hablados.

* Primero, configura los idiomas de Instant Translate. El idioma de origen
  debería ser el idioma del sistema del que se tomó el registro (por
  ejemplo, chino). El idioma de destino debería ser tu idioma (por ejemplo,
  francés).
* Abre el registro
* Pulsa la T para activar la traducción automática del habla en el registro
* Usa las órdenes de navegación rápida en el registro, por ejemplo S, I,
  etc. Cada vez que se encuentre un mensaje hablado, se verbalizará en
  nuestro idioma (francés en el ejemplo anterior)

Si quieres desactivar la traducción del habla, pulsa la T de nuevo.



<a id="logReaderOpenSourceFile"></a>
#### Abrir el archivo del código fuente en tu editor

En el registro, alguna línea puede hacer referencia al código fuente:

* Una línea relacionada con una traza contiene la ruta y la línea en el
  archivo, por ejemplo:
  `  File "virtualBuffers\__init__.pyc", line 226, in _getStoryLength`
* La línea de cabecera de un mensaje registrado contiene la función que ha
  registrado el mensaje, p.ej.:
  `INFO - config.ConfigManager._loadConfig (22:45:26.145) - MainThread (16580):`

Puedes querer que se abra el archivo que contiene el código para comprender
el contexto de la traza o el mensaje registrado. Pulsa la C para abrir el
archivo.

Para que esta característica funcione, necesitas configurar el [comando de
tu editor favorito](#settingsOpenCommand) en las opciones del
complemento. Si no estás ejecutando NVDA desde el código fuente, la
[ubicación del código fuente de NVDA](#settingsNvdaSourcePath) también
debería estar configurada.

<a id="oldLogsBackup"></a>
## Copia de seguridad de registros antiguos

NVDA ya proporciona una copia de seguridad del registro de la sesión
anterior de NVDA; el archivo se llama `nvda-old.log`. A veces, sin embargo,
puedes querer acceder a registros más antiguos, por ejemplo porque tuviste
que reiniciar NVDA otra vez antes de mirar `nvda-old.log`. Este complemento
permite configurar si quieres hacer copia de seguridad de los registros
antiguos y cuántos se guardan; esto se hace en las [opciones del
complemento](#settingsLogsBackup).

Un diálogo del gestor de registros permite visualizar los registros respaldados.
Se puede abrir yendo al menú NVDA -> Herramientas -> Gestor de registros.
En este diálogo, se puede ver la lista con los registros respaldados, abrirlos y borrarlos.
Para poder abrir un registro, deberías haber configurado primero el [comando para abrir un archivo en tu editor favorito](#settingsOpenCommand).

## Extensión de la consola Python

<a id="pythonConsoleOpenCodeFile"></a>
### Función `openCodeFile`

En la consola, puedes llamar a la siguiente función para ver el código fuente que define la variable `myVar`:
`openCodeFile(myVar)`  

Para que esta característica funcione, necesitas configurar el [comando de
tu editor favorito](#settingsOpenCommand) en las opciones del
complemento. Si no estás ejecutando NVDA desde el código fuente, la
[ubicación del código fuente de NVDA](#settingsNvdaSourcePath) también
debería estar configurada.

Se puede llamar a la función `openCodeFile` en objetos definidos en el
código de NVDA o en objetos definidos por los complementos. No se puede
llamar en objetos cuyo código fuente no está disponible, tales como los
incorporados en Python.

Si todavía no has importado el objeto en la consola, también puedes pasar su
nombre como parámetro a la función `openCodeFile`.

A continuación hay ejemplos de llamadas al código de NVDA:

* Ver la definición de la función `speech.speech.speak`:
  `openCodeFile(speech.speech.speak)`  
  o con el nombre pasado como parámetro:  
  `openCodeFile("speech.speech.speak")`  
* Ver la definición de la clase `TextInfo`:
  `openCodeFile(textInfos.TextInfo)`  
* Ver la definición del método `copyToClipboard` de la clase `TextInfo`:
  `openCodeFile(textInfos.TextInfo.copyToClipboard)`  
* Ver la definición de la clase del objeto con el foco:
  `openCodeFile(focus)`  
* Abrir el archivo `api.py` que define el módulo `api`:
  `openCodeFile(api)`

### Script de inicio de la consola Python

Puedes definir un script personalizado, que se ejecutará en el espacio de
nombres de la consola Python al abrirla por primera vez, o si se recarga el
complemento (NVDA+control+f3) después de haber abierto ya la consola.

Por ejemplo, el script te permite ejecutar importaciones y definir alias que podrás usar directamente en la consola, como se muestra a continuación:

    # Various import that I want in the console.
    import globalVars as gv
    import core
    import ui
    # Aliases
    ocf = openCodeFile

El script de la consola Python debería encontrarse en la siguiente ubicación: `RutaConfiguraciónNVDA\ndtt\consoleStartup.py`  
Por ejemplo:
`C:\Users\myUserName\AppData\Roaming\nvda\ndtt\consoleStartup.py`

## Registrar la pila de llamadas de la función de voz

A veces, puedes querer saber qué parte del código es responsable de
verbalizar algo. Para ello, puedes habilitar el registro de traza de pila de
la función de voz pulsando NVDA+control+alt+s. Cada vez que NVDA hable, se
grabará una traza de pila en el registro.

Nota: puedes modificar directamente el archivo del script para parchear otra
función. Consulta las instrucciones en el propio archivo para más detalles.

<a id="settings"></a>
## Opciones

Algunas características de este complemento pueden requerir una configuración concreta.
Un panel de opciones permite habilitarlas o controlar cómo funcionan.
Para ver y modificar estas opciones, ve al menú NVDA -> Preferencias y selecciona la categoría Caja de herramientas de desarrollo y pruebas de NVDA.

Se puede acceder también a este diálogo de opciones desde el diálogo del gestor de registros.

Estas opciones son globales y sólo se pueden configurar cuando está activado
el perfil predeterminado.

<a id="settingsOpenCommand"></a>
### Comando para abrir un archivo en tu editor favorito

Algunas funciones permiten visualizar contenido en tu editor favorito. Esto
incluye los comandos para ver el archivo de código fuente [desde un
registro](#logReaderOpenSourceFile) o [desde un objeto en la
consola](#pythonConsoleOpenCodeFile), así como el botón abrir del [gestor de
registros](#oldLogsBackup).

Para usarlas, primero debes configurar el comando que se ejecutará para abrir el archivo en tu editor favorito.
Dicho comando debería seguir el formato:
`"C:uta\a\mi\editor\editor.exe" "{path}":{line}`  
Por supuesto, deberías modificar esta línea en función del nombre real y ubicación del editor, y la sintaxis usada por él para abrir archivos.
`{path}` se sustituirá por por la ruta completa del archivo a abrir, y `{line}` por el número de línea donde quieres que se encuentre el cursor.
Por ejemplo, para Notepad++, el comando a escribir en la consola sería:
`"C:\Program Files\Notepad++\notepad++.exe" "{path}" -n{line}`

<a id="settingsNvdaSourcePath"></a>
### Ruta al código fuente de NVDA

Al usar un comando para [ver el archivo de código fuente desde un registro](#logReaderOpenSourceFile) o [desde un objeto en la consola](#pythonConsoleOpenCodeFile), el archivo debe pertenecer al propio NVDA.
Si no ejecutas NVDA desde el código fuente, tu copia de NVDA sólo contiene archivos compilados.
Por tanto, puedes configurar aquí una ubicación específica donde se encontrará el archivo de código fuente correspondiente, por ejemplo, el lugar donde has clonado los archivos de código fuente de NVDA, de tal forma que se pueda abrir un archivo de código fuente.
La ruta podría ser como:
`C:\EjemploRuta\GIT\nvda\source`  
Por supuesto, reemplaza la ruta del código fuente de NVDA con la correcta.

Asegúrate, no obstante, de que la versión de tu archivo fuente (por ejemplo,
commit de Git) es la misma que la de la instancia de NVDA en ejecución.

<a id="settingsLogsBackup"></a>
### Copia de seguridad de registros antiguos

El cuadro combinado de copia de seguridad de registros antiguos permite
activar o desactivar la [característica](#oldLogsBackup).  Si está activada,
se puede indicar debajo en "limitar la cantidad de copias de seguridad" la
cantidad máxima de copias de seguridad que quieres conservar. Estas opciones
sólo tienen efecto la próxima vez que se inicia NVDA al hacer la copia de
seguridad.

## Registro de cambios

### Versión 5.0

* Si el complemento Instant Translate está instalado, ahora es posible tener
  los mensajes hablados traducidos al vuelo al utilizar las órdenes de
  lectura del registro.
* Mientras estás en el modo de lectura del registro, pulsar E y shift+E
  ahora salta a mensajes de error críticos, tal y como hacía con los
  mensajes de error normales.
* Se han añadido nuevas órdenes de navegación rápida por el registro para
  saltar a los mensajes de entrada y hablados.
* Una nueva orden permite situar un marcador en el registro; y otras órdenes
  concretas de navegación rápida permiten saltar a marcadores en el
  registro.
  Créditos: la idea inicial de esta función viene del complemento Debug Helper de Luke Davis.

* Corrección de fallo: la memorización del último error ya no falla en
  algunos casos.
* Corrección de fallo: el complemento se inicializa de nuevo en NVDA
  2019.2.1.
* Corrección de fallo: la función de guardar el registro ya no fallará en
  registros no ASCII.

### Versión 4.2

* Corregido un error con versiones de NVDA anteriores a la 2021.3.
* Corregido el formateado del registro de pila de trazas.
* Primeras traducciones.

### Versión 4.1

* Corregido un fallo que ocurría en algunas situaciones al registrar un
  error.
* Ahora sólo pueden modificarse las opciones del complemento sólo cuando el
  perfil normal está activo para evitar problemas de configuración.

### Versión 4.0

* Posibilidad de hacer copia de seguridad de registros antiguos e
  introducción de un gestor de registros.
* Se ha añadido un script para anunciar el último error registrado.
* Corregido un error que impedía leer el último mensaje del registro en
  versiones antiguas de NVDA.

### Versión 3.2

* Compatibilidad con NVDA 2023.1.

### Versión 3.1

* Corregido un error que ocurría al solicitar información no disponible en
  un objeto.

### Versión 3.0

* En un registro, ahora se puede pulsar la C en una línea de cabecera de
  mensaje para abrir el módulo o función que lo emitió.
* En la consola, la función `openCodeFile` puede recibir como parámetro el
  objeto o una cadena que contenga su nombre.
* Nueva función: archivo de inicio de la consola de NVDA: si existe, el
  archivo tuCarpetaDeConfiguraciónDeNVDA\ndtt\consoleStartup.py se ejecutará
  al abrir la consola Python por primera vez o cuando se recarguen los
  complementos.
* Diversas correcciones menores para la función de la consola Python
  `openCodeFile` y la orden para abrir el archivo de código fuente
  correspondiente a una línea del registro.
* Corregido un problema al intentar anunciar roles y estados en el
  explorador de objetos en versiones antiguas de NVDA.
* El complemento ya no causa problemas con el interceptor de árbol al usar
  UIA en Edge.

### Versión 2.1

* Diversas correcciones de fallos y refactorización y limpieza del código
  para tener en cuenta todos los casos de uso: todas las versiones
  soportadas, instalado vs. ejecutado desde el código fuente,
  etc. (colaboración de Łukasz Golonka)
* Reescritura del módulo compa (colaboración de Łukasz Golonka)
* Ahora, el diálogo para reiniciar se puede abrir sólo una vez.
* Los atajos del explorador de objetos ahora vienen por defecto sin asignar
  y deben ser asignados por el usuario.
* En el explorador de objetos, una pulsación doble para llamar al script que
  indica la propiedad del objeto ahora muestra la información indicada en un
  mensaje explorable.

### Versión 2.0

* Nueva función: diálogo de reiniciar mejorado para indicar algunas opciones
  extra al reiniciar NVDA.
* Nueva función: modo de descripción extendida.
* Función para reproducir sonidos de error armonizada entre las versiones
  anterior y posterior a la 2021.3 de NVDA.
* Nueva función: las órdenes del lector del registro ahora están disponibles
  en el visualizador del registro y, opcionalmente, en cualquier cuadro de
  edición y en páginas web.
* Nueva función: en la consola Python, está disponible una función
  `openCodeFile` para ver el código fuente de un objeto.
* Algunas funciones están ahora deshabilitadas en modo seguro por motivos de
  seguridad.
* Se ha extendido el rango de compatibilidad del complemento (de 2019.2 a
  2021.1).
* Las liberaciones ahora se llevan a cabo con una acción de GitHub en lugar
  de AppVeyor.

### Versión 1.0

* Versión inicial.

[[!tag dev stable]]

[1]: https://www.nvaccess.org/addonStore/legacy?file=nvdaDevTestToolbox

[2]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#CommandLineOptions

[3]: https://addons.nvda-project.org/addons/instantTranslate.en.html

[4]:
https://www.nvaccess.org/files/nvda/documentation/userGuide.html#PlayErrorSound

[5]:
https://www.nvaccess.org/files/nvda/documentation/developerGuide.html#toc22
