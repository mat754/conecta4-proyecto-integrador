# logica.py
# Lógica del juego Conecta 4 (no usa ventanas, solo la parte del "cerebro").
# Aquí están la pila, la cola, la matriz T de 6x7 y el guardado en historial.csv

import os
from datetime import datetime

FILAS = 6
COLUMNAS = 7

# El historial.csv está en la misma carpeta que este archivo
RUTA_HISTORIAL = os.path.join(os.path.dirname(os.path.abspath(__file__)), "historial.csv")

# Matriz D de direcciones (cambio en fila, cambio en columna)
# horizontal, vertical, diagonal descendente, diagonal ascendente
D = [(0, 1), (1, 0), (1, 1), (-1, 1)]


# ---------------------------------------------------------------
# PILA (LIFO) con nodos enlazados: guarda las jugadas (fila, columna)
# ---------------------------------------------------------------
class NodoPila:
    def __init__(self, fila, columna):
        self.fila = fila
        self.columna = columna
        self.abajo = None          # puntero al nodo que está debajo


class Pila:
    def __init__(self):
        self.tope = None           # vale None cuando la pila está vacía
        self.tamano = 0            # cuántos nodos tiene la pila

    def esta_vacia(self):
        return self.tope is None

    def push(self, fila, columna):
        nuevo = NodoPila(fila, columna)
        nuevo.abajo = self.tope    # el nuevo apunta al que era el tope
        self.tope = nuevo          # ahora el nuevo es el tope
        self.tamano = self.tamano + 1

    def pop(self):
        if self.esta_vacia():
            return None
        nodo = self.tope
        self.tope = nodo.abajo     # el tope baja un nodo
        self.tamano = self.tamano - 1
        return (nodo.fila, nodo.columna)

    def top(self):
        if self.esta_vacia():
            return None
        return (self.tope.fila, self.tope.columna)


# ---------------------------------------------------------------
# COLA (FIFO) con nodos enlazados: guarda el orden de los turnos
# ---------------------------------------------------------------
class NodoCola:
    def __init__(self, jugador):
        self.jugador = jugador     # 1 o 2
        self.siguiente = None


class Cola:
    def __init__(self):
        self.frente = None
        self.final = None

    def esta_vacia(self):
        return self.frente is None

    def encolar(self, jugador):
        nuevo = NodoCola(jugador)
        if self.esta_vacia():
            self.frente = nuevo
        else:
            self.final.siguiente = nuevo
        self.final = nuevo

    def desencolar(self):
        if self.esta_vacia():
            return None
        nodo = self.frente
        self.frente = nodo.siguiente
        if self.frente is None:
            self.final = None
        return nodo.jugador

    def ver_frente(self):
        if self.esta_vacia():
            return None
        return self.frente.jugador


# ---------------------------------------------------------------
# JUEGO: la matriz T, los turnos y las reglas
# ---------------------------------------------------------------
class Juego:
    def __init__(self, nombre1, nombre2):
        self.nombre1 = nombre1
        self.nombre2 = nombre2
        self.nueva_partida()

    def nueva_partida(self):
        # Matriz T de 6 filas y 7 columnas: 0 = vacío, 1 = jugador 1, 2 = jugador 2
        self.T = []
        for i in range(FILAS):
            fila = []
            for j in range(COLUMNAS):
                fila.append(0)
            self.T.append(fila)

        self.pila = Pila()
        self.turnos = Cola()
        self.turnos.encolar(1)
        self.turnos.encolar(2)
        self.terminada = False
        self.resultado = ""        # luego será "gana_1", "gana_2" o "empate"

    def turno_actual(self):
        return self.turnos.ver_frente()

    def cambiar_turno(self):
        # Saca al jugador del frente y lo vuelve a poner al final
        jugador = self.turnos.desencolar()
        self.turnos.encolar(jugador)

    def colocar_ficha(self, columna):
        # Devuelve la fila donde cayó la ficha, o -1 si la jugada no es válida
        if self.terminada:
            return -1
        if columna < 0 or columna >= COLUMNAS:
            return -1
        if self.T[0][columna] != 0:    # columna llena
            return -1

        # La ficha cae hasta la fila libre más baja (la de mayor índice)
        fila = FILAS - 1
        while self.T[fila][columna] != 0:
            fila = fila - 1

        jugador = self.turno_actual()
        self.T[fila][columna] = jugador
        self.pila.push(fila, columna)

        if self.hay_victoria(fila, columna, jugador):
            self.terminada = True
            self.resultado = "gana_" + str(jugador)
        elif self.pila.tamano == FILAS * COLUMNAS:     # 42 fichas: tablero lleno
            self.terminada = True
            self.resultado = "empate"
        else:
            self.cambiar_turno()
        return fila

    def contar(self, fila, columna, d_fila, d_col, jugador):
        # Cuenta fichas seguidas del jugador en una dirección (máximo 3)
        total = 0
        for k in range(1, 4):
            f = fila + k * d_fila
            c = columna + k * d_col
            if f < 0 or f >= FILAS or c < 0 or c >= COLUMNAS:
                break                   # se salió del tablero
            if self.T[f][c] != jugador:
                break                   # encontró otra casilla
            total = total + 1
        return total

    def hay_victoria(self, fila, columna, jugador):
        # Revisa las 4 direcciones a partir de la última ficha
        for d in D:
            d_fila = d[0]
            d_col = d[1]
            positivo = self.contar(fila, columna, d_fila, d_col, jugador)
            negativo = self.contar(fila, columna, -d_fila, -d_col, jugador)
            total = 1 + positivo + negativo      # 1 es la ficha recién puesta
            if total >= 4:
                return True
        return False

    def deshacer(self):
        # Devuelve True si se pudo deshacer y False si no
        if self.terminada or self.pila.esta_vacia():
            return False
        jugada = self.pila.pop()
        fila = jugada[0]
        columna = jugada[1]
        self.T[fila][columna] = 0
        self.cambiar_turno()           # vuelve a jugar quien había movido
        return True

    def guardar_resultado(self):
        # Escribe una línea en historial.csv (modo append)
        ganador = "ninguno"
        if self.resultado == "gana_1":
            ganador = self.nombre1
        elif self.resultado == "gana_2":
            ganador = self.nombre2

        fecha = datetime.now().strftime("%Y-%m-%d %H:%M")
        linea = (fecha + "," + self.nombre1 + "," + self.nombre2 + "," +
                 self.resultado + "," + ganador + "," + str(self.pila.tamano))

        # Si el archivo no existe (o está vacío) se crea con su encabezado
        hace_falta_encabezado = (not os.path.exists(RUTA_HISTORIAL)
                                 or os.path.getsize(RUTA_HISTORIAL) == 0)

        archivo = open(RUTA_HISTORIAL, "a", encoding="utf-8")
        if hace_falta_encabezado:
            archivo.write("fecha_hora,jugador1,jugador2,resultado,ganador,total_jugadas\n")
        archivo.write(linea + "\n")
        archivo.close()


# ---------------------------------------------------------------
# Limpieza de nombres
# ---------------------------------------------------------------
def limpiar_nombre(nombre, por_defecto):
    # Quita comas y espacios sobrantes y pone mayúscula a cada palabra
    if nombre is None:
        return por_defecto
    nombre = nombre.replace(",", " ")
    palabras = nombre.split()          # split() ya elimina los espacios sobrantes
    if len(palabras) == 0:
        return por_defecto
    resultado = ""
    for palabra in palabras:
        resultado = resultado + palabra.capitalize() + " "
    return resultado.strip()