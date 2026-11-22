# Conecta 4 – Proyecto Integrador (Fase 3)

**Universidad Internacional del Ecuador (UIDE)**
Carrera: Ingeniería en Inteligencia Artificial – Semestre 1
Equipo nro. 8

**Integrantes**
- Dary Matias Campaña Caicedo
- Martin Alejandro Recalde Rivera
- Mateo Nicolay Taez Taez

---

## Descripción

Juego de **Conecta 4** para dos jugadores, formado por dos programas independientes que se comunican únicamente mediante el archivo compartido `historial.csv`:

1. **Módulo Python (`python_juego/`)**: lógica del juego, interfaz gráfica con Tkinter y registro del resultado de cada partida. Usa una **pila (LIFO)** para deshacer jugadas, una **cola (FIFO)** para los turnos y la **matriz T de 6x7** para el tablero.
2. **Módulo C/C++ (`cpp_datos/`)**: lee `historial.csv`, carga las partidas en una **lista enlazada**, calcula las estadísticas de cada jugador en una segunda lista enlazada, las ordena con **burbuja** y muestra el ranking.

El módulo de Python solo escribe en `historial.csv` y el módulo de C/C++ solo lo lee.

## Estructura del proyecto

```
ProyectoJuego/
├── python_juego/
│   ├── juego.py          (programa principal: pide los nombres y abre el juego)
│   ├── interfaz.py       (ventana y eventos con Tkinter)
│   ├── logica.py         (pila, cola, matriz T, reglas y guardado del resultado)
│   └── historial.csv     (archivo compartido entre los dos módulos)
├── cpp_datos/
│   ├── main.cpp          (programa principal del ranking)
│   ├── ranking.cpp       (lectura del CSV, listas enlazadas, burbuja y ranking)
│   └── nodo.h            (struct de los nodos y lista de funciones)
├── docs/
│   └── diagramas/        (diagramas de la Fase 2)
├── LICENSE
└── README.md
```

## Formato de `historial.csv`

Una partida por línea, con encabezado:

```
fecha_hora,jugador1,jugador2,resultado,ganador,total_jugadas
2026-10-30 18:45,Matias,Martin,gana_1,Matias,23
2026-10-30 19:10,Mateo,Matias,empate,ninguno,42
```

- `resultado` puede ser `gana_1`, `gana_2` o `empate`.
- `ganador` es el nombre del ganador, o `ninguno` si hubo empate.
- `total_jugadas` es la cantidad de fichas que quedaron en el tablero.

## Requisitos

- Python 3 con Tkinter (viene incluido en las instalaciones normales de Python para Windows y macOS).
- Un compilador de C++, por ejemplo GCC (`g++`).

## Cómo ejecutarlo

**Juego (Python)** – desde la carpeta `python_juego`:

```
python juego.py
```

**Ranking (C++)** – desde la carpeta `cpp_datos`:

```
g++ main.cpp ranking.cpp -o ranking
./ranking
```

En Windows el ejecutable se llama `ranking.exe`. Primero hay que jugar al menos una partida completa para que `historial.csv` tenga datos.

## Cómo se juega

1. Al iniciar se piden los nombres de los dos jugadores (si se dejan vacíos se usan "Jugador 1" y "Jugador 2").
2. Se hace clic en una columna para dejar caer una ficha (amarillo = jugador 1, rojo = jugador 2).
3. Gana quien junte cuatro fichas seguidas en horizontal, vertical o diagonal.
4. El botón **Deshacer** quita la última jugada mientras la partida siga en curso.
5. Al terminar la partida, el resultado se guarda en `historial.csv`.

---

## Licencia

Este proyecto se distribuye bajo la **licencia MIT**.

## Declaración de Autoría y Créditos

### Autoría
El diseño del proyecto (requisitos, diagramas de flujo, arquitectura, modelo matemático de la matriz y estructuras de datos) fue desarrollado por el grupo en las Fases 1 y 2. El código de esta fase implementa ese diseño.

### Uso de inteligencia artificial
Se utilizó la herramienta **Claude (Anthropic)** como apoyo. El uso fue el siguiente:

| Fase | Para qué se usó | Qué hizo el grupo |
|------|-----------------|-------------------|
| Fase 2 | Apoyo para elaborar los diagramas y esquemas | Aportó las ideas, el diseño y la estructura de los diagramas |
| Fase 3 | Generar una versión inicial del código (Python y C++) a partir del diseño del grupo, y guiar el uso de Git y GitHub | Definió el diseño que el código implementa, revisó el código, lo ejecutó, pidió corregirlo cuando no coincidía con el diseño y lo simplificó para poder explicarlo |
| Fase 3 | Apoyo para redactar este README y la bitácora | Verificó que el contenido corresponda a lo ocurrido en el proyecto |

Los integrantes del equipo son responsables de explicar, defender y modificar el código entregado. La estructura, las decisiones de diseño y el desarrollo conceptual son del grupo.

### Librerías y herramientas utilizadas
Todas son de código abierto o forman parte de la biblioteca estándar:
- Python 3 y su biblioteca estándar: `tkinter` (interfaz), `os` y `datetime`.
- C++ y su biblioteca estándar: `iostream`, `fstream`, `sstream`, `iomanip`, `cstdlib` y `string`.
- Compilador GCC (`g++`).
- Git y GitHub para el control de versiones.

### Código de terceros y recursos visuales
No se copió código de otros proyectos. El tablero y las fichas se dibujan con las formas básicas de Tkinter, por lo que no se usan imágenes, íconos ni otros recursos visuales de terceros. Los diagramas de la carpeta `docs/diagramas/` fueron elaborados con apoyo de IA, como se declara arriba.


## Bitácora de Gestión de Conflictos

Durante el desarrollo se presentaron conflictos, casi todos relacionados con el código. A continuación se documentan dos aplicando la **Fórmula Asertiva** (Hechos, Sentimientos, Necesidades y Petición).

### Conflicto 1: el código inicial no coincidía con el diseño de la Fase 2

**Hechos.** La primera versión del código inicial guardaba el historial con las columnas `fecha,jugador1,jugador2,ganador`, mientras que la Fase 2 define `fecha_hora,jugador1,jugador2,resultado,ganador,total_jugadas`. Esa versión ordenaba el ranking por inserción y no por burbuja, que es el algoritmo documentado. Además, el archivo `historial.csv` estaba en una carpeta `datos/`, y la estructura que pide el profesor lo ubica dentro de `python_juego/`. Como los dos módulos solo se comunican por ese archivo, un formato distinto en cada lado habría hecho fallar la lectura del ranking.

**Sentimientos.** Preocupación y presión de tiempo: el diseño ya había sido aprobado con comentarios positivos y el código no lo respetaba, lo que ponía en riesgo la coherencia entre las fases y la entrega.

**Necesidades.** Que el código fuera fiel al diseño aprobado, que los dos módulos usaran exactamente el mismo formato de archivo y que la estructura de carpetas coincidiera con la solicitada.

**Petición.** Reescribir el código tomando como única referencia el documento de la Fase 2 y la estructura del profesor, y acordar una regla para el resto del proyecto: cualquier cambio de formato del CSV o de algoritmo se verifica primero contra la Fase 2 y se avisa a quienes trabajan en el otro módulo. **Resultado:** el código se reescribió con el formato de seis columnas, el ordenamiento por burbuja y `historial.csv` dentro de `python_juego/`. Se probó con el ejemplo de la Figura 8 (gana el jugador 1 con 11 jugadas) y con un historial de ejemplo que incluía líneas dañadas, que el módulo de C++ ignoró sin detenerse.
