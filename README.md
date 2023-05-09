# DCCruz vs Zombies :zombie::seedling::sunflower:
La aplicación se inicia desde el módulo `executable.py` (no dejarse engañar por el nombre. Este archivo no es un ejecutable). Todo el código y juego fue redactado completamente en **Inglés**. 
Para la lectura de los módulos, se recomienda revisarlos en el orden que aparecen en el apartado **Librerías propias**, esto facilitará la comprensión de cómo están estructurados los objetos.

La separación Front-End/Back-End es fuerte, tal que la construcción de todos los elementos del juego, tienen una parte en cada uno de estos ejes. Así, por ejemplo, existe una clase `ZombieVisual`, encargada de todo el aspecto visual de los zombies, y la clase `ZombieLogic`, encargada, naturalmente, de la lógica de los zombies.

**Tip**: Se puede mutear la *música* en la ventana de juego pulsando la **m** (después de mucho abrir el programa para corregir, imagino que ha de ser agobiante escuchar sin parar la música).

## Consideraciones generales :octocat:
Pese a grandes esfuerzos para reducir las líneas de código, en ocasiones los archivos que manejaban tanto el *fron-end* como el *back-end*, superaban con creces las 400 líneas. Por ello, se dividieron las clases correspondientes en módulos separados de los cuales las versiones finales *heredan* la clase que contiene la información. Así, se tiene la siguiente relación entre los módulos:
- Módulo `game_gui.py`, prepara la estructura de la **ventana** de juego, establecido a través de la clase `GameGui(QWidget)`. Esta clase nunca es instanciada, sino que en el módulo `game_ft.py`, está la clase `GameWindow(GameGui)` que hereda y sí es instanciada. Esta última se encarga de todo el aspecto funcional del fron-end.
- Módulo `game_1_bk.py` establece la clase `GameLogicLoad`, que es heredada por `GameLogic(GameLogicLoad)` en el módulo `game_bk.py`. Esta última encargada de todo el aspecto funcional del back-end.

La abreviación **ft** hace referencia a *front-end*, y la abreviación **bk**, hace referencia a *back-end*.

Para la realización de la tarea, he creado **QWidgets** personalizados, incluyendo funcionalidades que normalmente no están disponibles. En particular quiero mencionar a la clase `PausableTimer(QTimer)`, que consiste, como su nombre insinúa, en un `QTimer` que tiene la posibilidad de ser pausado para volver a iniciarse **justo en el instante de tiempo donde fue pausado**, esta posibilidad no existe de forma predefinida en un `QTimer`, ya que al utilizar el método `stop()` de la clase, y volver a iniciar el *timer*, comienza a contar desde 0. (Así, si los soles eran generados cada 20 segundos, y uno pausaba en 19 segundos, iba a tener que volver a esperar 20 segundos porque el `QTimer` no es pausable, solo *detenible* y luego *reiniciado*). Este es el problema que soluciona la clase `PausableTimer(QTimer)`. Todas las clases personalizadas se encuentran en `custom_elements.py`.

## Librerías :books:
### Librerías externas utilizadas
La lista de librerías externas que utilicé fue la siguiente:

1. `PyQt5`: en todos los módulos.
2. `random`: en módulos `elements_1_bk.py`, `elements_2_bk.py`, `game_bk.py` y `elements_ft.py`.
3. `math`: en módulo `elements_2_bk.py`.
4. `sys`: en módulo `executable.py`
5. `os`: en módulo `parameters.py`

### Librerías propias
Como se mencionó anteriormente, se recomienda leer el código en el orden aquí presentado. Todo el juego está dividido fuertemente, por lo que toda clase de Front, tiene su complemento Back. Los módulos que fueron creados son los siguientes:

1. `elements_ft`: Contiene las clases
    - `PlantVisual`: Encargada de preparar el aspecto visual que tienen en común todas las plantas. (Esta se asemeja a una clase abstracta).
    - `SunFlowerVisual`: Prepara las imagénes y propiedades relacionadas a los girasoles.
    - `PeaShooterVisual`: Prepara las imagénes y propiedades relacionadas a los lanzaguisantes.
    - `IcePeaShooterVisual`: Prepara las imagénes y propiedades relacionadas a los lanzaguistantes de hielo.
    - `NutVisual`: Prepara las imagénes y propiedades relacionadas a las nueces.
    - `CrazyCruz`: El personaje que acompaña durante el juego, prepara su interacción de diálogos y sonidos
    - `SunVisual`: Prepara las imagénes y propiedades relacionadas a los soles.
    - `Shovel`: Prepara las imagénes y propiedades relacionadas a la interacción de la pala en la ventana de juego.
    - `PeaVisual`: Prepara las imagénes y propiedades relacionadas a los guisantes en el juego.
    - `ZombieVisual`: Prepara las imagénes y propiedades relacionadas a los zombies, ya sean de tipo *Hernán* o normal.
2. `elements_1_bk`: Contiene las clases para la lógica de las plantas (complementando las clases de la librería anterior);
    - `PlantLogic`: Prepara el funcionamiento general de las plantas, incluyendo sus propiedades y atributos locales. Funciona como clase abstracta.
    - `SunFlowerLogic`: Incluye las propiedades, métodos, y timers relacionados a los girasoles y sus mecánicas.
    - `ShooterLogic`: Incluye las propiedades, métodos, y timers relacionados a los lanzaguisantes y sus mecánicas. Funciona como clase abstracta.
    - `PeaShooterLogic`: Incluye las propiedades, métodos, y timers relacionados a los lanzaguisantes normales y sus mecánicas.
    - `IcePeaShooterLogic`: Incluye las propiedades, métodos, y timers relacionados a los lanzaguisantes de hielo y sus mecánicas.
    - `NutLogic`: Incluye las propiedades, métodos, y timers relacionados a las nueces y sus mecánicas.
3. `elements_2_bk`: Contiene las clases para la lógica de los elementos móviles, distintos de las plantas. Complemetando su contraparte *front*:
    - `SunLogic`: Incluye las propiedades relacionadas a la generación y movimiento de los soles, su intervalo de aparición, la ganancia que se tiene al recogerlos, etc.
    - `PeaLogic`: Incluye las propiedades relacionadas a la generación y movimiento de los guisantes, su intervalo de aparición, el daño que producen, etc.
    - `ZombieLogic`: Incluye las propiedades relacionadas a la generación y movimiento de los zombies, su intervalo de aparición, el daño que realizan, etc.
4. `welcome_ft`: Contiene la clase `WelcomeWindow`, que establece el aspecto visual de la ventana de inicio. Instancia elementos decorativos del juego (Un girasol y un lanzaguisante).
5. `welcome_bk`: Contiene la clase `WelcomeLogic`, encargada de la verificación de usuario, de instanciar la lógica de las plantas asociadas al inicio y señalizar la entrada a la ventana principal.
6. `rank_ft`: Contiene la clase `RankingWindow`, que establece el aspecto visual de la ventana de ranking.
7. `rank_bk`: Contiene la clase `RankingLogic`, encargada de la lectura de los puntajes y su preparación para ser presentada en el front.
8. `main_ft`: Contiene la clase `MainWindow`, que establece el aspecto visual de la ventana principal. Presenta las opciones de escensario.
9. `main_bk`: Contiene la clase `MainLogic`, encargada de la lectura de selección y de señaliza el paso al juego.
10. `game_ft`: Contiene la clase `GameWindow`. Aquí se presentan todos los elementos visuales del juego, se crean contenedores para los elementos generados, se crean los eventos para la sensibilidad de los clicks y de los drags. Establece además aspectos estéticos coherentes con el resto del juego. La música, también está incluída aquí.
11. `game_bk`: Contiene la clase `GameLogic`. Toda la magia ocurre aquí, tiene las señales que indican movimiento, muerte, colisión, y efectos generales de juego. Interpreta el input del usuario, instancia la lógica de los elementos, guarda en sus propiedades las estadísticas de la ronda, etc.
12. `post_ft`: Contiene la clase `PostWindow`: Que prepara el aspecto visual de las estadísticas post-ronda.
13. `post_bk`: Contiene la clase `PostLogic`: Encargada de la interpretación de las estadísticas.
14. `game`: Contiene la clase `DCCruzVsZombies`. Clase aplicación que instancia todas las ventanas y sus lógicas. Crea las conexiones de todas las señales.
15. `custom_elements`: Contiene las clases
    - `PausableTimer`: Hereda de `QTimer` con la posibilidad de ser pausado y retornar exactamente donde quedó.
    - `SelectableLabel`: Hereda de `QLabel`, tiene una señal para reconocer cuando es clickeado.
    - `SensibleLabel`: Hereda de `QLabel`, tiene funcionalidad para reconocer clicks, y eventos de tipo Drop.
**Las siguientes librerías también fueron creadas, pero no es necesario leerlas ya que son puramente visual, ó bien, solo contiene atributos que se utilizan en la clase que les hereda**
15. `game_1_bk`: Contiene la clase `GameLogicLoad`, clase con señales y atributos. Creada para ser heredada por `GameLogic`, y no sobrepasar el límite de líneas (de aquí su poca relevancia como clase única).
16. `game_gui`: Contiene la clase `GameGui`, con señales y la preparación visual de los frames en la ventana de juego.

## Supuestos y consideraciones finales :thinking:
Se informan los siguientes supuestos, decisiones, etc:

1. Se ha implementando tanto Drag & Drop, como compra por clic. De este modo, el jugador puede comprar y plantar de ambas formas.
2. CrazyCruz hablará durante todo el juego, con mensajes acordes a los eventos. Esto es para mantener más viva la experiencia del usuario.
3. El botón *Salir* de la ventana de juego, efectivamente sale del juego, en lugar de redireccionar a la ventana post-juego. Esto porque no encontré la parte del enunciado que decía, que debe dirigir al post juego, es más natural "salir" al presionar salir. A pesar de esto, es posible llegar a la ventana post juego de cualquiera de las otras formas: ganando, perdiendo, skippeando al pagar con soles, y con cheat `KIL`.
4. De acuerdo a lo mencionado en un issue, la velocidad de los zombies está configurada para ser 5 px/s para un zombie normal no ralentizado. El número que aparece en `parametros.py` en referencia a este valor, está ajustado para que sea, efectivamente, esa la velocidad del zombie.
5. Bug identificado: Cuando se inicia una ronda posterior a la primera, y en aquella ronda, se paga para esquivar la ronda (con los soles suficientes), y luego en la ventana de post ronda, se decide salir en lugar de ir a la siguiente ronda, el juego vuelve a la ventana de inicio, pero, vuelve a abrir la ventana post ronda una vez. De modo que ambas ventanas quedan abiertas. El juego se puede iniciar normalmente tras esto. Solo es necesario cerrar la ventana post ronda.

## Referencias de código externo :book:

Se han utilizado las siguiente fuentes como inspiración para código especial:
1. [Publicación de @Jie-Jenn](https://learndataanalysis.org/create-label-to-label-drag-and-drop-effect-pyqt5-tutorial/): para efectos de Drag & Drop.
